window.API_BASE = window.API_BASE || 'http://127.0.0.1:8001';
const API_BASE = window.API_BASE;

// ===== MODAL HANDLERS =====
function openModal() {
    document.getElementById('addChargerModal').style.display = 'flex';
}

function openEditModal() {
    document.getElementById('editChargerModal').style.display = 'flex';
}

function closeEditModal() {
    document.getElementById('editChargerModal').style.display = 'none';
    document.getElementById('editChargerForm').reset();
}

function closeModal() {
    document.getElementById('addChargerModal').style.display = 'none';
    document.getElementById('addChargerForm').reset();
}

// ===== FORM SUBMISSION =====
async function handleAddCharger(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    
    try {
        const response = await fetch(`${API_BASE}/add_charger`, {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const result = await response.json();
            alert('Laadpaal succesvol toegevoegd!');
            closeModal();
            fetchChargers(); // Refresh table
        } else {
            const error = await response.json();
            alert(`Fout: ${error.message || 'Kon laadpaal niet toevoegen'}`);
        }
    } catch (error) {
        console.error('Error adding charger:', error);
        alert('Fout bij het toevoegen van de laadpaal');
    }
}

function formatEnergy(num) {
    return parseFloat(num || 0).toFixed(2).replace(',', '.');
}

/**
 * Updates the status counter cards with current charger statistics
 * @param {Array} chargersData
 */
function updateStatusCounter(chargersData) {
    // Initialize counters for each status category
    let total = chargersData.length;
    let online = 0;
    let offline = 0;
    let maintenance = 0;

    // Iterate through each charger and categorize by status
    chargersData.forEach(charger => {
        const status = (charger.status || '').toLowerCase();

        // Categorize chargers based on their current status
        if (status === 'online' || status === 'available') {
            online++;
        } else if (status === 'onderhoud' || status === 'maintainance') {
            maintenance++;
        } else {
            offline++;
        }
    });

    // Update the counter display elements in the DOM
    document.getElementById('totalChargers').textContent = total;
    document.getElementById('onlineChargers').textContent = online;
    document.getElementById('offlineChargers').textContent = offline;
    document.getElementById('maintenanceChargers').textContent = maintenance;
}

// Fetch all chargers with their energy consumption data
async function fetchChargers() {
    const tbody = document.getElementById("chargersBody");

    try {
        const response = await fetch(`${API_BASE}/laadpalen`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        updateStatusCounter(data);

        if (!Array.isArray(data) || data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" style="text-align: center;">Geen laadpalen gevonden</td></tr>';
            return;
        }

        tbody.innerHTML = '';

        // Populate table with charger data
        for (const charger of data) {
            const row = createChargerRow(charger);
            tbody.appendChild(row);
        }
    } catch (error) {
        console.error('Error fetching chargers:', error);
        tbody.innerHTML = '<tr><td colspan="7" style="text-align: center; color: red;">Fout bij het laden van laadpalen</td></tr>';
    }
}

// Create table row for charger
function createChargerRow(charger) {
    const row = document.createElement('tr');
    row.dataset.evboxId = charger.EVBOXID;

    const chargerId = charger.EVBOXID.toString().padStart(2, '0');

    // Get energy consumption
    const energyConsumption = charger.total_energy || 0;
    const formattedEnergy = formatEnergy(energyConsumption);

    const statusClass = charger.status
      ? charger.status.toLowerCase() === "available"
        ? "status-available"
        : charger.status.toLowerCase() === "onderhoud" ||
          charger.status.toLowerCase() === "maintainance"
        ? "status-maintenance"
        : "status-offline"
      : "status-offline";
    const statusDisplay = charger.status || 'Offline';

    
    const power = charger.power || '0 kW';

    // Price per kWh
    const price = charger.price_per_kwh || '€0.00';

    row.innerHTML = `
        <td><strong>${chargerId}</strong> ${charger.name || 'Onbekend'}</td>
        <td>${charger.locationName || 'N/A'}</td>
        <td><span class="${statusClass}">${statusDisplay}</span></td>
        <td>${power}</td>
        <td>${price}</td>
        <td>${formattedEnergy} kWh</td>
        <td>
            <div class="actions-cell">
                <button class="toggle-btn ${charger.status === 'online' ? 'on' : ''}" 
                        title="Laadpaal aan/uit schakelen"
                        onclick="toggleCharger(${charger.EVBOXID}, '${charger.status}')"></button>
                <button class="action-btn" title="Laadpaal bewerken" onclick="editCharger(${charger.EVBOXID})">✎</button>
            </div>
        </td>
    `;

    return row;
}

// Toggle charger on/off (Placholder)
async function toggleCharger(evboxId, currentStatus) {
    const newStatus = currentStatus === 'online' ? 'off' : 'on';

    try {
        const response = await fetch(`${API_BASE}/chargers/${evboxId}/toggle`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ state: newStatus })
        });

        if (response.ok) {
            // Refresh the table after toggling
            fetchChargers();
        } else {
            console.error('Failed to toggle charger');
            alert('Fout bij het schakelen van de laadpaal');
        }
    } catch (error) {
        console.error('Error toggling charger:', error);
        alert('Fout bij het schakelen van de laadpaal');
    }
}

// Edit charger (placeholder)
function editCharger(evboxId) {
    // TODO: Implement edit functionality
    console.log(`Edit charger: ${evboxId}`);
    openEditModal();
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Load chargers on page load
    fetchChargers();
    
    // Refresh chargers every 5 seconds
    setInterval(fetchChargers, 5000);
    
    // Modal event listeners
    document.getElementById('addChargerBtn').addEventListener('click', openModal);
    document.getElementById('closeModalBtn').addEventListener('click', closeModal);
    document.getElementById('cancelBtn').addEventListener('click', closeModal);
    document.getElementById('addChargerForm').addEventListener('submit', handleAddCharger);
    document.getElementById('closeEditModalBtn').addEventListener('click', closeEditModal);
    document.getElementById('cancelEditBtn').addEventListener('click', closeEditModal);
    
    // Close modal when clicking outside the modal content
    window.addEventListener("click", function (event) {
      const addModal = document.getElementById("addChargerModal");
      const editModal = document.getElementById("editChargerModal");

      if (event.target === addModal) {
        closeModal();
      }

      if (event.target === editModal) {
        closeEditModal();
      }
    });
});

// Cleanup on page unload
window.addEventListener('beforeunload', function() {
});
