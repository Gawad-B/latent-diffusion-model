"""
Medical Image Generation using Latent Diffusion Model
Loads the trained model and generates synthetic chest X-ray images
"""

import torch
import torch.nn.functional as F
from PIL import Image
import numpy as np
from pathlib import Path
from diffusers import AutoencoderKL, DDPMScheduler, UNet2DModel
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')


class Config:
    """Configuration for the latent diffusion model"""
    # Model Parameters
    VAE_MODEL = "stabilityai/sd-vae-ft-mse"
    VAE_SCALE_FACTOR = 0.18215
    LATENT_SIZE = 32  # 256 // 8
    LATENT_CHANNELS = 4
    IMAGE_SIZE = 256
    
    # Inference Parameters
    TIMESTEPS = 1000
    NUM_INFERENCE_STEPS = 50  # Fewer steps for faster generation
    
    # Paths
    CHECKPOINT_DIR = Path("./checkpoints")
    OUTPUT_DIR = Path("./static/generated")
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class MedicalImageGenerator:
    """Generates synthetic medical images using trained latent diffusion model"""
    
    def __init__(self, model_path=None, device=None):
        """
        Initialize the generator
        
        Args:
            model_path: Path to the trained model checkpoint (.pth file)
            device: torch device (cuda/cpu). Auto-detects if None
        """
        self.config = Config()
        
        # Set device
        if device is None:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = device
            
        print(f"Using device: {self.device}")
        
        # Load VAE (pre-trained encoder/decoder)
        print("Loading VAE...")
        self.vae = AutoencoderKL.from_pretrained(
            self.config.VAE_MODEL,
            torch_dtype=torch.float32
        ).to(self.device)
        self.vae.eval()
        
        # Create U-Net model
        print("Creating U-Net model...")
        self.model = self._create_unet()
        
        # Load trained weights if provided
        if model_path:
            self.load_checkpoint(model_path)
        
        # Initialize noise scheduler
        self.noise_scheduler = DDPMScheduler(
            num_train_timesteps=self.config.TIMESTEPS
        )
        
        print("Model initialized successfully!")
    
    def _create_unet(self):
        """Create the U-Net architecture"""
        model = UNet2DModel(
            sample_size=self.config.LATENT_SIZE,
            in_channels=self.config.LATENT_CHANNELS,
            out_channels=self.config.LATENT_CHANNELS,
            layers_per_block=2,
            block_out_channels=(128, 256, 512, 512),
            down_block_types=(
                "DownBlock2D",
                "DownBlock2D",
                "AttnDownBlock2D",
                "DownBlock2D",
            ),
            up_block_types=(
                "UpBlock2D",
                "AttnUpBlock2D",
                "UpBlock2D",
                "UpBlock2D",
            ),
        )
        return model.to(self.device)
    
    def load_checkpoint(self, checkpoint_path):
        """Load trained model weights"""
        print(f"Loading checkpoint from: {checkpoint_path}")
        checkpoint_path = Path(checkpoint_path)
        
        if not checkpoint_path.exists():
            raise FileNotFoundError(f"Checkpoint not found: {checkpoint_path}")
        
        state_dict = torch.load(checkpoint_path, map_location=self.device)
        self.model.load_state_dict(state_dict)
        self.model.eval()
        print("Checkpoint loaded successfully!")
    
    def generate_images(self, num_images=1, disease_type="NORMAL", save_path=None):
        """
        Generate synthetic medical images
        
        Args:
            num_images: Number of images to generate
            disease_type: Type of disease (for naming purposes)
            save_path: Directory to save generated images. If None, returns PIL images
            
        Returns:
            List of PIL Image objects or list of saved file paths
        """
        print(f"Generating {num_images} {disease_type} images...")
        
        self.model.eval()
        self.vae.eval()
        
        # Generate in batches to avoid memory issues
        batch_size = min(4, num_images)
        all_images = []
        
        with torch.no_grad():
            for batch_idx in range(0, num_images, batch_size):
                current_batch_size = min(batch_size, num_images - batch_idx)
                
                # 1. Start with random noise in latent space
                latents = torch.randn(
                    (current_batch_size, self.config.LATENT_CHANNELS, 
                     self.config.LATENT_SIZE, self.config.LATENT_SIZE),
                    device=self.device
                )
                
                # 2. Denoising loop
                self.noise_scheduler.set_timesteps(self.config.NUM_INFERENCE_STEPS)
                
                for t in tqdm(self.noise_scheduler.timesteps, 
                            desc=f"Batch {batch_idx//batch_size + 1}", 
                            leave=False):
                    # Predict noise
                    noise_pred = self.model(latents, t).sample
                    
                    # Remove predicted noise
                    latents = self.noise_scheduler.step(
                        noise_pred, t, latents
                    ).prev_sample
                
                # 3. Decode latents to images
                latents = latents / self.config.VAE_SCALE_FACTOR
                images = self.vae.decode(latents).sample
                
                # 4. Denormalize from [-1, 1] to [0, 1]
                images = (images / 2 + 0.5).clamp(0, 1)
                
                # 5. Convert to PIL Images
                for i in range(current_batch_size):
                    # Convert tensor to numpy
                    img_array = images[i].cpu().permute(1, 2, 0).numpy()
                    
                    # Convert RGB to grayscale (medical images are typically grayscale)
                    img_array = np.mean(img_array, axis=2)
                    
                    # Convert to 8-bit
                    img_array = (img_array * 255).astype(np.uint8)
                    
                    # Create PIL Image
                    pil_image = Image.fromarray(img_array, mode='L')
                    all_images.append(pil_image)
        
        # Save or return images
        if save_path:
            save_path = Path(save_path)
            save_path.mkdir(parents=True, exist_ok=True)
            
            saved_paths = []
            for idx, img in enumerate(all_images):
                filename = f"{disease_type.lower()}_{idx+1}.png"
                full_path = save_path / filename
                img.save(full_path)
                saved_paths.append(str(full_path))
            
            print(f"✓ Saved {len(saved_paths)} images to {save_path}")
            return saved_paths
        else:
            return all_images
    
    def generate_single_sample(self, disease_type="NORMAL"):
        """
        Quick method to generate a single image
        
        Args:
            disease_type: Disease type for naming
            
        Returns:
            PIL Image object
        """
        images = self.generate_images(num_images=1, disease_type=disease_type)
        return images[0]


# Convenience function for Flask integration
def generate_medical_images(disease_type, count, model_path=None, output_dir=None):
    """
    Generate medical images for Flask endpoint
    
    Args:
        disease_type: Type of disease (NORMAL, PNEUMONIA, TUBERCULOSIS)
        count: Number of images to generate
        model_path: Path to model checkpoint
        output_dir: Where to save generated images
        
    Returns:
        List of relative paths to generated images
    """
    if output_dir is None:
        output_dir = Config.OUTPUT_DIR
    
    # Initialize generator (will cache this in production)
    generator = MedicalImageGenerator(model_path=model_path)
    
    # Generate images
    saved_paths = generator.generate_images(
        num_images=count,
        disease_type=disease_type,
        save_path=output_dir
    )
    
    # Convert absolute paths to relative web paths
    relative_paths = [
        '/' + str(Path(p).relative_to(Path.cwd()))
        for p in saved_paths
    ]
    
    return relative_paths


if __name__ == "__main__":
    # Test the generator
    print("Testing Medical Image Generator...")
    
    # Check for checkpoint
    checkpoint_path = Config.CHECKPOINT_DIR / "final_unet_model.pth"
    
    if checkpoint_path.exists():
        generator = MedicalImageGenerator(model_path=checkpoint_path)
        
        # Generate a test image
        test_images = generator.generate_images(
            num_images=2,
            disease_type="TEST",
            save_path=Config.OUTPUT_DIR
        )
        
        print(f"Generated {len(test_images)} test images!")
    else:
        print(f"No checkpoint found at {checkpoint_path}")
        print("Please train the model first or provide a valid checkpoint path.")
