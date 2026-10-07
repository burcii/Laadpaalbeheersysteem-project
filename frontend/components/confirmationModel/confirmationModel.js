/**
 * Displays a custom confirmation dialog using a modal and returns a Promise
 * that resolves to true (Yes) or false (No/Cancel).
 * @param {string} message The confirmation question to display.
 * @returns {Promise<boolean>} Resolves to true if confirmed, false otherwise.
 */
function showConfirmation(message) {
    const overlay = document.getElementById('confirmation-model-overlay');
    const msg = document.getElementById('confirmation-model-message');
    const yesBtn = document.getElementById('confirm-yes');
    const noBtn = document.getElementById('confirm-no');

    if (!overlay || !msg || !yesBtn || !noBtn) {
        console.error('Confirmation Model component not found in DOM');
        // Fallback to browser's native confirm if component is missing
        return Promise.resolve(confirm(message));
    }

    msg.textContent = message;
    overlay.style.display = 'flex';

    // The function returns a promise that resolves true (Ja) or false (Nee/Cancel)
    return new Promise(resolve => {
        // Helper to clean up listeners and close the popup
        function cleanupAndClose(result) {
            overlay.style.display = 'none';
            yesBtn.removeEventListener('click', onYes);
            noBtn.removeEventListener('click', onNo);
            overlay.removeEventListener('click', onOverlayClick);
            resolve(result);
        }

        // Action for "Ja"
        const onYes = () => {
            cleanupAndClose(true);
        };

        // Action for "Nee"
        const onNo = () => {
            cleanupAndClose(false);
        };
        
        // Action for clicking the overlay (Nee/Cancel)
        const onOverlayClick = (e) => {
            // Check if the click target is exactly the overlay (backdrop)
            if (e.target === overlay) {
                cleanupAndClose(false);
            }
        };

        yesBtn.addEventListener('click', onYes);
        noBtn.addEventListener('click', onNo);

        // FIX: Delay attaching the overlay listener by 50ms.
        // This prevents the instant-close bug caused by the click event that 
        // triggered this modal being interpreted as a click on the backdrop.
        setTimeout(() => {
            overlay.addEventListener('click', onOverlayClick);
        }, 50);
    });
}