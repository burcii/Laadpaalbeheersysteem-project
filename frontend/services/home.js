window.API_BASE = window.API_BASE || 'http://127.0.0.1:8001';
const API_BASE = window.API_BASE;

document.addEventListener('DOMContentLoaded', function() {
    loadChargers();
    chargerWS.connect();
});

window.addEventListener('beforeunload', function() {
    chargerWS.disconnect();
});

let confirmUrl = "";
let confirmCallback = null;

function openConfirmDialog(message, callbackOrUrl) {
    document.getElementById("confirmMessage").textContent = message;
    document.getElementById("confirmModal").style.display = "flex";

    if (typeof callbackOrUrl === "string") {
        confirmUrl = callbackOrUrl;
        confirmCallback = null;
    } else if (typeof callbackOrUrl === "function") {
        confirmCallback = callbackOrUrl;
        confirmUrl = "";
    }
}

function closeConfirmDialog() {
    document.getElementById("confirmModal").style.display = "none";
}

document.getElementById("confirmYes").onclick = function () {
    if (confirmUrl) {
        window.location.href = confirmUrl;
    } else if (confirmCallback) {
        confirmCallback();
    }
    closeConfirmDialog();
};


function toggleChargers(state) {
    fetch(`services/toggle_chargers.php?state=${state}`)
        .then(response => response.json())
        .then(data => {
            alert(data.message); // Feedback naar de gebruiker
            // Eventueel: tabel opnieuw laden
        })
        .catch(err => {
            console.error("Fout bij toggle:", err);
        });
}


async function fetchLaadpalen() {
    const tbody = document.getElementById("chargersBody");

    try {
        const response = await fetch(`${API_BASE}/laadpalen`);
        const data = await response.json();

        if (!Array.isArray(data) || data.length === 0) {
            if (tbody.children.length === 0) {
                const emptyRow = document.createElement("tr");
                emptyRow.innerHTML = '<td colspan="4" style="text-align: center;">Geen laadpalen gevonden</td>';
                tbody.appendChild(emptyRow);
            }
            return;
        }

        for (const item of data) {
            const existing = tbody.querySelector(`tr[data-evbox-id="${item.EVBOXID}"]`);
            const id = item.EVBOXID.toString().padStart(3, '0');
            const lastSession = item.laatste_sessie_datum || 'Nog geen sessies';

            if (existing) {
                const cells = existing.querySelectorAll('td');
                if (cells[1].textContent !== item.locationName) cells[1].textContent = item.locationName;
                if (cells[2].textContent !== item.status) cells[2].textContent = item.status;
                if (cells[3].textContent !== lastSession) cells[3].textContent = lastSession;
            } else {
                const row = document.createElement("tr");
                row.dataset.evboxId = item.EVBOXID;
                row.innerHTML = `
                    <td>${id}</td>
                    <td>${item.locationName}</td>
                    <td>${item.status}</td>
                    <td>${lastSession}</td>
                `;
                row.addEventListener('click', () => openEVBoxModal(item.EVBOXID));
                tbody.appendChild(row);
            }
        }
    } catch (error) {
        console.error(error);
        tbody.innerHTML = '<tr><td colspan="4" style="text-align: center; color: red;">Fout bij het laden van gegevens</td></tr>';
    }
}




let refreshInterval;

window.addEventListener("DOMContentLoaded", () => {
    fetchLaadpalen();

    refreshInterval = setInterval(fetchLaadpalen, 3000);
});

window.addEventListener("beforeunload", () => {
    if (refreshInterval) {
        clearInterval(refreshInterval);
    }
});
