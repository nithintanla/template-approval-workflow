// Common JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {
    // Initialize any global UI components
    
    // Handle status messages auto-hide
    const messages = document.querySelectorAll('.messages .alert');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 300);
        }, 3000);
    });
});
