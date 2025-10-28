// Main JavaScript for ToolHub

// Global variables
let currentTaskId = null;
let pollInterval = null;

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add loading states to buttons
    document.querySelectorAll('button[type="submit"], .submit-btn').forEach(button => {
        button.addEventListener('click', function() {
            if (!this.disabled) {
                this.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Processing...';
                this.disabled = true;
            }
        });
    });

    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined') {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // Add copy-to-clipboard functionality
    document.querySelectorAll('.copy-btn').forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                copyToClipboard(targetElement.textContent || targetElement.value);
                showNotification('Copied to clipboard!', 'success');
            }
        });
    });
}

// File upload handling
function handleFileUpload(files, inputElement) {
    const fileList = Array.from(files);
    const maxSize = 100 * 1024 * 1024; // 100MB
    const validFiles = [];
    
    fileList.forEach(file => {
        if (file.size > maxSize) {
            showNotification(`File "${file.name}" is too large. Maximum size is 100MB.`, 'error');
        } else {
            validFiles.push(file);
        }
    });
    
    if (validFiles.length > 0) {
        displaySelectedFiles(validFiles);
        return validFiles;
    }
    
    return [];
}

function displaySelectedFiles(files) {
    const container = document.getElementById('selectedFiles');
    if (!container) return;
    
    container.innerHTML = '';
    
    files.forEach((file, index) => {
        const fileElement = document.createElement('div');
        fileElement.className = 'flex items-center justify-between p-2 bg-gray-50 rounded mb-2';
        
        fileElement.innerHTML = `
            <div class="flex items-center">
                <i class="fas fa-file text-gray-400 mr-2"></i>
                <span class="text-sm font-medium">${file.name}</span>
                <span class="text-xs text-gray-500 ml-2">(${formatFileSize(file.size)})</span>
            </div>
            <button onclick="removeFile(${index})" class="text-red-500 hover:text-red-700">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        container.appendChild(fileElement);
    });
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Progress tracking
function updateProgressBar(progress, taskId = null) {
    const progressBar = document.getElementById('progressBar');
    const progressPercent = document.getElementById('progressPercent');
    
    if (progressBar) {
        progressBar.style.width = progress + '%';
        progressBar.setAttribute('aria-valuenow', progress);
    }
    
    if (progressPercent) {
        progressPercent.textContent = Math.round(progress) + '%';
    }
    
    // Update progress ring if exists
    const progressRing = document.querySelector('.progress-ring circle');
    if (progressRing) {
        const circumference = 2 * Math.PI * progressRing.r.baseVal.value;
        const offset = circumference - (progress / 100) * circumference;
        progressRing.style.strokeDashoffset = offset;
    }
}

function startProgressPolling(taskId, onComplete) {
    if (pollInterval) {
        clearInterval(pollInterval);
    }
    
    currentTaskId = taskId;
    
    pollInterval = setInterval(async () => {
        try {
            const response = await fetch(`/api/status/${taskId}`);
            const status = await response.json();
            
            updateProgressBar(status.progress);
            updateProcessingStatus(status);
            
            if (status.status === 'completed') {
                clearInterval(pollInterval);
                pollInterval = null;
                if (onComplete) onComplete(status);
            } else if (status.status === 'failed') {
                clearInterval(pollInterval);
                pollInterval = null;
                showNotification('Processing failed: ' + (status.error || 'Unknown error'), 'error');
            }
        } catch (error) {
            console.error('Error polling status:', error);
            clearInterval(pollInterval);
            pollInterval = null;
            showNotification('Error checking processing status', 'error');
        }
    }, 1000);
}

function updateProcessingStatus(status) {
    const statusElement = document.getElementById('processingStatus');
    const timeElement = document.getElementById('timeRemaining');
    
    if (statusElement) {
        const statusMessages = {
            0: 'Initializing...',
            10: 'Preparing files...',
            25: 'Reading input data...',
            50: 'Processing content...',
            75: 'Generating output...',
            90: 'Finalizing results...',
            100: 'Complete!'
        };
        
        const nearestProgress = Math.floor(status.progress / 25) * 25;
        const message = statusMessages[nearestProgress] || 'Processing...';
        statusElement.textContent = message;
    }
    
    if (timeElement && status.estimated_time && status.elapsed_time) {
        const remaining = Math.max(0, status.estimated_time - status.elapsed_time);
        timeElement.textContent = remaining > 0 ? `${remaining}s remaining` : 'Almost done...';
    }
}

// Modal handling
function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    }
}

function hideModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('hidden');
        document.body.style.overflow = 'auto';
    }
}

function showProcessingModal(toolName) {
    const toolNameElement = document.getElementById('processingToolName');
    if (toolNameElement) {
        toolNameElement.textContent = toolName;
    }
    
    // Reset progress
    updateProgressBar(0);
    
    // Reset status
    const statusElement = document.getElementById('processingStatus');
    if (statusElement) {
        statusElement.textContent = 'Initializing...';
    }
    
    showModal('processingModal');
}

function showSuccessModal(taskId) {
    hideModal('processingModal');
    
    // Set up download button
    const downloadBtn = document.getElementById('downloadBtn');
    if (downloadBtn) {
        downloadBtn.onclick = () => downloadResult(taskId);
    }
    
    showModal('successModal');
}

// Download handling
function downloadResult(taskId) {
    const downloadUrl = `/api/download/${taskId}`;
    
    // Create temporary link and trigger download
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = '';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    hideModal('successModal');
    showNotification('Download started successfully!', 'success');
}

// Notification system
function showNotification(message, type = 'info', duration = 5000) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type} show`;
    
    const icon = {
        'success': 'fas fa-check-circle',
        'error': 'fas fa-exclamation-circle',
        'warning': 'fas fa-exclamation-triangle',
        'info': 'fas fa-info-circle'
    }[type] || 'fas fa-info-circle';
    
    notification.innerHTML = `
        <div class="flex items-center">
            <i class="${icon} mr-2"></i>
            <span>${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" class="ml-4 text-gray-500 hover:text-gray-700">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after duration
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, duration);
}

// Utility functions
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text);
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
    }
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let lastFunc;
    let lastRan;
    return function() {
        const context = this;
        const args = arguments;
        if (!lastRan) {
            func.apply(context, args);
            lastRan = Date.now();
        } else {
            clearTimeout(lastFunc);
            lastFunc = setTimeout(function() {
                if ((Date.now() - lastRan) >= limit) {
                    func.apply(context, args);
                    lastRan = Date.now();
                }
            }, limit - (Date.now() - lastRan));
        }
    }
}

// API helpers
async function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData
    });
    
    if (!response.ok) {
        throw new Error(`Upload failed: ${response.statusText}`);
    }
    
    return await response.json();
}

async function processFiles(toolName, files, additionalData = {}) {
    try {
        // Upload files first
        const uploadPromises = files.map(file => uploadFile(file));
        const uploadResults = await Promise.all(uploadPromises);
        
        // Start processing
        const response = await fetch('/api/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                tool_name: toolName,
                files: uploadResults,
                ...additionalData
            })
        });
        
        if (!response.ok) {
            throw new Error(`Processing failed: ${response.statusText}`);
        }
        
        const result = await response.json();
        return result;
        
    } catch (error) {
        console.error('Error processing files:', error);
        throw error;
    }
}

// Form validation
function validateForm(formElement) {
    const requiredFields = formElement.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            isValid = false;
            field.classList.add('border-red-500');
            
            // Show error message
            let errorMessage = field.parentElement.querySelector('.error-message');
            if (!errorMessage) {
                errorMessage = document.createElement('span');
                errorMessage.className = 'error-message text-red-500 text-sm mt-1';
                field.parentElement.appendChild(errorMessage);
            }
            errorMessage.textContent = 'This field is required';
        } else {
            field.classList.remove('border-red-500');
            const errorMessage = field.parentElement.querySelector('.error-message');
            if (errorMessage) {
                errorMessage.remove();
            }
        }
    });
    
    return isValid;
}

// Close modal when clicking outside
document.addEventListener('click', function(event) {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        if (event.target === modal) {
            hideModal(modal.id);
        }
    });
});

// Close modal with Escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        const visibleModals = document.querySelectorAll('.modal:not(.hidden)');
        visibleModals.forEach(modal => {
            hideModal(modal.id);
        });
    }
});

// Handle browser back button
window.addEventListener('popstate', function(event) {
    const visibleModals = document.querySelectorAll('.modal:not(.hidden)');
    if (visibleModals.length > 0) {
        visibleModals.forEach(modal => {
            hideModal(modal.id);
        });
        history.pushState(null, null, location.pathname);
    }
});

// Performance monitoring
function measurePerformance(name, fn) {
    const start = performance.now();
    const result = fn();
    const end = performance.now();
    console.log(`${name} took ${end - start} milliseconds`);
    return result;
}

// Error handling
window.addEventListener('error', function(event) {
    console.error('Global error:', event.error);
    showNotification('An unexpected error occurred. Please try again.', 'error');
});

window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled promise rejection:', event.reason);
    showNotification('An error occurred while processing your request.', 'error');
});

// Export functions for global use
window.ToolHub = {
    showModal,
    hideModal,
    showNotification,
    uploadFile,
    processFiles,
    updateProgressBar,
    startProgressPolling,
    downloadResult,
    formatFileSize,
    copyToClipboard,
    validateForm
};