/*
	Hyperspace by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
*/

(function($) {

	var	$window = $(window),
		$body = $('body'),
		$sidebar = $('#sidebar');

	// Breakpoints.
		breakpoints({
			xlarge:   [ '1281px',  '1680px' ],
			large:    [ '981px',   '1280px' ],
			medium:   [ '737px',   '980px'  ],
			small:    [ '481px',   '736px'  ],
			xsmall:   [ null,      '480px'  ]
		});

	// Hack: Enable IE flexbox workarounds.
		if (browser.name == 'ie')
			$body.addClass('is-ie');

	// Play initial animations on page load.
		$window.on('load', function() {
			window.setTimeout(function() {
				$body.removeClass('is-preload');
			}, 100);
		});

	// Forms.

		// Hack: Activate non-input submits.
			$('form').on('click', '.submit', function(event) {

				// Stop propagation, default.
					event.stopPropagation();
					event.preventDefault();

				// Submit form.
					$(this).parents('form').submit();

			});

	// Sidebar.
		if ($sidebar.length > 0) {

			var $sidebar_a = $sidebar.find('a');

			$sidebar_a
				.addClass('scrolly')
				.on('click', function() {

					var $this = $(this);

					// External link? Bail.
						if ($this.attr('href').charAt(0) != '#')
							return;

					// Deactivate all links.
						$sidebar_a.removeClass('active');

					// Activate link *and* lock it (so Scrollex doesn't try to activate other links as we're scrolling to this one's section).
						$this
							.addClass('active')
							.addClass('active-locked');

				})
				.each(function() {

					var	$this = $(this),
						id = $this.attr('href'),
						$section = $(id);

					// No section for this link? Bail.
						if ($section.length < 1)
							return;

					// Scrollex.
						$section.scrollex({
							mode: 'middle',
							top: '-20vh',
							bottom: '-20vh',
							initialize: function() {

								// Deactivate section.
									$section.addClass('inactive');

							},
							enter: function() {

								// Activate section.
									$section.removeClass('inactive');

								// No locked links? Deactivate all links and activate this section's one.
									if ($sidebar_a.filter('.active-locked').length == 0) {

										$sidebar_a.removeClass('active');
										$this.addClass('active');

									}

								// Otherwise, if this section's link is the one that's locked, unlock it.
									else if ($this.hasClass('active-locked'))
										$this.removeClass('active-locked');

							}
						});

				});

		}

	// Scrolly.
		$('.scrolly').scrolly({
			speed: 1000,
			offset: function() {

				// If <=large, >small, and sidebar is present, use its height as the offset.
					if (breakpoints.active('<=large')
					&&	!breakpoints.active('<=small')
					&&	$sidebar.length > 0)
						return $sidebar.height();

				return 0;

			}
		});

	// Spotlights.
		$('.spotlights > section')
			.scrollex({
				mode: 'middle',
				top: '-10vh',
				bottom: '-10vh',
				initialize: function() {

					// Deactivate section.
						$(this).addClass('inactive');

				},
				enter: function() {

					// Activate section.
						$(this).removeClass('inactive');

				}
			})
			.each(function() {

				var	$this = $(this),
					$image = $this.find('.image'),
					$img = $image.find('img'),
					x;

				// Assign image.
					$image.css('background-image', 'url(' + $img.attr('src') + ')');

				// Set background position.
					if (x = $img.data('position'))
						$image.css('background-position', x);

				// Hide <img>.
					$img.hide();

			});

	// Features.
		$('.features')
			.scrollex({
				mode: 'middle',
				top: '-20vh',
				bottom: '-20vh',
				initialize: function() {

					// Deactivate section.
						$(this).addClass('inactive');

				},
				enter: function() {

					// Activate section.
						$(this).removeClass('inactive');

				}
			});

})(jQuery);

// Custom functionality for chat and image generation
(function() {
	
	// Wait for DOM to be ready
	document.addEventListener('DOMContentLoaded', function() {
		
		// Chat functionality
		const chatForm = document.getElementById('chat-form');
		if (chatForm) {
			chatForm.addEventListener('submit', async function(e) {
				e.preventDefault();
				
				const userInput = document.getElementById('user-input');
				const message = userInput.value.trim();
				
				if (message === '') return;
				
				// Add user message to chat
				addMessage(message, 'user');
				userInput.value = '';
				
				// Show typing indicator
				showTypingIndicator();
				
				try {
					// Send message to backend
					const response = await fetch('/chat', {
						method: 'POST',
						headers: {
							'Content-Type': 'application/json',
						},
						body: JSON.stringify({ message: message })
					});
					
					const data = await response.json();
					
					// Remove typing indicator
					removeTypingIndicator();
					
					// Add AI response to chat
					addMessage(data.response, 'ai');
				} catch (error) {
					removeTypingIndicator();
					addMessage('Sorry, I encountered an error. Please try again.', 'ai');
				}
			});
		}
		
		function addMessage(text, sender) {
			const chatMessages = document.getElementById('chat-messages');
			const messageDiv = document.createElement('div');
			messageDiv.className = 'message ' + sender + '-message';
			
			const contentDiv = document.createElement('div');
			contentDiv.className = 'message-content';
			
			// First, handle bold text
			text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
			
			// Split by lines and process
			let lines = text.split('\n');
			let processedLines = [];
			let currentParagraph = [];
			
			for (let line of lines) {
				line = line.trim();
				
				// Empty line = end of paragraph
				if (!line) {
					if (currentParagraph.length > 0) {
						processedLines.push(currentParagraph.join(' '));
						currentParagraph = [];
					}
					continue;
				}
				
				// Bullet point or header - add as separate item
				if (line.match(/^[\*•-]\s+/) || line.match(/:$/)) {
					// Flush current paragraph first
					if (currentParagraph.length > 0) {
						processedLines.push(currentParagraph.join(' '));
						currentParagraph = [];
					}
					processedLines.push(line);
				}
				// Regular text - add to current paragraph
				else {
					currentParagraph.push(line);
				}
			}
			
			// Flush remaining paragraph
			if (currentParagraph.length > 0) {
				processedLines.push(currentParagraph.join(' '));
			}
			
			// Now format the processed lines
			let html = '';
			for (let line of processedLines) {
				// Header (ends with colon)
				if (line.match(/:$/) && !line.match(/^[\*•-]/)) {
					html += '<div style="margin-top: 1.2em; margin-bottom: 0.5em;"><strong>' + line + '</strong></div>';
				}
				// Bullet point
				else if (line.match(/^[\*•-]\s+/)) {
					line = line.replace(/^[\*•-]\s+/, '');
					html += '<div style="margin-left: 0.5em; margin-top: 0.4em;">• ' + line + '</div>';
				}
				// Regular paragraph
				else {
					html += '<div style="margin-top: 0.8em;">' + line + '</div>';
				}
			}
			
			if (sender === 'ai') {
				contentDiv.innerHTML = '<div style="line-height: 1.8;"><strong style="color: #A855D8;">AI Assistant:</strong>' + html + '</div>';
			} else {
				contentDiv.innerHTML = '<div style="line-height: 1.8;">' + html + '</div>';
			}
			
			messageDiv.appendChild(contentDiv);
			chatMessages.appendChild(messageDiv);
			
			// Scroll to bottom
			chatMessages.scrollTop = chatMessages.scrollHeight;
		}
		
		function showTypingIndicator() {
			const chatMessages = document.getElementById('chat-messages');
			const typingDiv = document.createElement('div');
			typingDiv.className = 'message ai-message typing-indicator';
			typingDiv.id = 'typing-indicator';
			typingDiv.innerHTML = '<div class="message-content"><strong>AI Assistant:</strong> <span class="typing-dots"><span>.</span><span>.</span><span>.</span></span></div>';
			chatMessages.appendChild(typingDiv);
			chatMessages.scrollTop = chatMessages.scrollHeight;
		}
		
		function removeTypingIndicator() {
			const typingIndicator = document.getElementById('typing-indicator');
			if (typingIndicator) {
				typingIndicator.remove();
			}
		}
		
		// Image generation functionality
		const generateForm = document.getElementById('generate-form');
		if (generateForm) {
			generateForm.addEventListener('submit', async function(e) {
				e.preventDefault();
				
				const diseaseSelect = document.getElementById('disease-select');
				const numImages = document.getElementById('num-images');
				const disease = diseaseSelect.value;
				const count = numImages.value;
				
				if (!disease) {
					alert('Please select a disease');
					return;
				}
				
				// Show loading
				document.getElementById('generation-loading').style.display = 'block';
				document.getElementById('generation-result').style.display = 'none';
				
				try {
					// Send generate request to backend
					const response = await fetch('/generate', {
						method: 'POST',
						headers: {
							'Content-Type': 'application/json',
						},
						body: JSON.stringify({ 
							disease: disease,
							count: parseInt(count)
						})
					});
					
					const data = await response.json();
					
					// Hide loading
					document.getElementById('generation-loading').style.display = 'none';
					
					if (data.success) {
						// Log the received image paths for debugging
						console.log('Received images:', data.images);
						console.log('Session ID:', data.session_id);
						// Display generated images with preview and download options
						displayGeneratedImagesWithPreview(data.images, data.session_id, disease);
					} else {
						alert('Error generating images: ' + (data.error || 'Unknown error'));
					}
				} catch (error) {
					document.getElementById('generation-loading').style.display = 'none';
					alert('Error: ' + error.message);
				}
			});
		}
		
		// Upload button functionality
		const uploadBtn = document.getElementById('upload-btn');
		const imageUpload = document.getElementById('image-upload');
		
		if (uploadBtn && imageUpload) {
			uploadBtn.addEventListener('click', function() {
				imageUpload.click();
			});
			
			imageUpload.addEventListener('change', function(e) {
				const file = e.target.files[0];
				if (file) {
					const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'application/pdf'];
					const fileExtension = file.name.split('.').pop().toLowerCase();
					const allowedExtensions = ['jpg', 'jpeg', 'png', 'pdf'];
					
					if (!allowedTypes.includes(file.type) && !allowedExtensions.includes(fileExtension)) {
						alert('Please select a valid file (PDF, JPG, JPEG, or PNG)');
						imageUpload.value = '';
						return;
					}
					
					const reader = new FileReader();
					reader.onload = function(event) {
						const previewImage = document.getElementById('preview-image');
						const uploadPreview = document.getElementById('upload-preview');
						
						// Only show preview for image files, not PDF
						if (file.type.startsWith('image/')) {
							previewImage.src = event.target.result;
							uploadPreview.style.display = 'block';
						} else {
							uploadPreview.style.display = 'none';
							alert('PDF uploaded successfully: ' + file.name);
						}
					};
					reader.readAsDataURL(file);
				}
			});
		}
		
		function displayGeneratedImagesWithPreview(images, sessionId, disease) {
			const container = document.getElementById('generated-images');
			const resultSection = document.getElementById('generation-result');
			container.innerHTML = '';
			
			// Create preview header
			const header = document.createElement('div');
			header.style.marginBottom = '30px';
			header.style.textAlign = 'center';
			header.innerHTML = `
				<h3>Preview of Generated ${disease.charAt(0).toUpperCase() + disease.slice(1)} Images</h3>
				<p>Review the generated images below. If you're satisfied, click "Download All" to save them.</p>
			`;
			container.appendChild(header);
			
			// Create sample image display (show first image only)
			const sampleWrapper = document.createElement('div');
			sampleWrapper.style.textAlign = 'center';
			sampleWrapper.style.marginBottom = '40px';
			
			const sampleImg = document.createElement('img');
			sampleImg.src = images[0];
			console.log('Setting image src to:', images[0]);
			sampleImg.alt = 'Generated sample image';
			sampleImg.style.maxWidth = '500px';
			sampleImg.style.width = '100%';
			sampleImg.style.height = 'auto';
			sampleImg.style.borderRadius = '8px';
			sampleImg.style.border = '3px solid #5e42a6';
			sampleImg.style.boxShadow = '0 4px 20px rgba(0,0,0,0.3)';
			
			// Add error handling for image loading
			sampleImg.onerror = function() {
				console.error('Failed to load image:', images[0]);
				sampleImg.alt = 'Error loading image';
				sampleImg.style.display = 'none';
				const errorMsg = document.createElement('p');
				errorMsg.textContent = 'Error loading image. Path: ' + images[0];
				errorMsg.style.color = 'red';
				sampleWrapper.appendChild(errorMsg);
			};
			
			const sampleLabel = document.createElement('p');
			sampleLabel.textContent = `Sample Image (1 of ${images.length})`;
			sampleLabel.style.marginTop = '15px';
			sampleLabel.style.fontSize = '16px';
			sampleLabel.style.fontWeight = 'bold';
			sampleLabel.style.color = '#5e42a6';
			
			sampleWrapper.appendChild(sampleImg);
			sampleWrapper.appendChild(sampleLabel);
			container.appendChild(sampleWrapper);
			
			// Activate the existing download button
			const downloadAllBtn = document.getElementById('download-all-btn');
			if (downloadAllBtn) {
				// Enable the button
				downloadAllBtn.disabled = false;
				downloadAllBtn.style.opacity = '1';
				downloadAllBtn.style.cursor = 'pointer';
				
				// Remove any existing event listeners by cloning the button
				const newDownloadBtn = downloadAllBtn.cloneNode(true);
				downloadAllBtn.parentNode.replaceChild(newDownloadBtn, downloadAllBtn);
				
				// Add new event listener
				newDownloadBtn.addEventListener('click', async function() {
					try {
						newDownloadBtn.disabled = true;
						newDownloadBtn.innerHTML = '<i class="fa fa-spinner fa-spin"></i> Preparing...';
						
						const response = await fetch('/download-batch', {
							method: 'POST',
							headers: {
								'Content-Type': 'application/json',
							},
							body: JSON.stringify({ session_id: sessionId })
						});
						
						if (response.ok) {
							const blob = await response.blob();
							const url = window.URL.createObjectURL(blob);
							const a = document.createElement('a');
							a.href = url;
							a.download = `${disease}_images.zip`;
							document.body.appendChild(a);
							a.click();
							window.URL.revokeObjectURL(url);
							document.body.removeChild(a);
							
							newDownloadBtn.disabled = false;
							newDownloadBtn.innerHTML = '<i class="fa fa-check"></i> Downloaded!';
							
							setTimeout(function() {
								newDownloadBtn.innerHTML = '<i class="fa fa-download"></i> Download All as ZIP';
							}, 3000);
						} else {
							throw new Error('Download failed');
						}
					} catch (error) {
						alert('Error downloading images: ' + error.message);
						newDownloadBtn.disabled = false;
						newDownloadBtn.innerHTML = '<i class="fa fa-download"></i> Download All as ZIP';
					}
				});
			}
			
			resultSection.style.display = 'block';
			
			// Scroll to results
			resultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
		}
		
		// Fallback function (kept for compatibility)
		function displayGeneratedImages(images) {
			displayGeneratedImagesWithPreview(images, 'default', 'medical');
		}
		
	});
	
})();
