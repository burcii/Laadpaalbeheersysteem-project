function showPopupModel(message) {
  const overlay = document.getElementById('popup-model-overlay');
  const msg = document.getElementById('popup-model-message');
  const closeBtn = document.getElementById('popup-model-close');

  if (!overlay || !msg || !closeBtn) {
    console.error('Popup Model component not found in DOM');
    return;
  }

  msg.textContent = message;
  overlay.style.display = 'flex';

  function closePopup() {
    overlay.style.display = 'none';
    closeBtn.removeEventListener('click', closePopup);
  }

  closeBtn.addEventListener('click', closePopup);
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) closePopup();
  });
}
