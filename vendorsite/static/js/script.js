// Profile Popup Functions
function toggleProfilePopup() {
    const popup = document.getElementById('userProfilePopup');
    const overlay = document.getElementById('popupOverlay');
    
    popup.classList.toggle('open');
    overlay.classList.toggle('open');
    
    document.body.style.overflow = popup.classList.contains('open') ? 'hidden' : 'auto';
}

function closeProfilePopup() {
    const popup = document.getElementById('userProfilePopup');
    const overlay = document.getElementById('popupOverlay');
    
    popup.classList.remove('open');
    overlay.classList.remove('open');
    document.body.style.overflow = 'auto';
}

// Close popup when pressing Escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeProfilePopup();
    }
});