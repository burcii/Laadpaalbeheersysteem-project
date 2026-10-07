const API_BASE_MODAL = window.API_BASE || 'http://127.0.0.1:8001';

// Modal functionality
function openEVBoxModal(evboxId) {
    const modal = document.getElementById('evboxModal');
    modal.style.display = 'block';
    showLoading();
    loadEVBoxData(evboxId);
}

function closeModal() {
    const modal = document.getElementById('evboxModal');
    modal.style.display = 'none';
}

function showLoading() {
    document.getElementById('modalLoading').style.display = 'block';
    document.getElementById('modalError').style.display = 'none';
    document.getElementById('evboxInfo').style.display = 'none';
    document.getElementById('activeSession').style.display = 'none';
    document.getElementById('noActiveSession').style.display = 'none';
    document.getElementById('historicalSessions').style.display = 'none';
    document.getElementById('sessionDetail').style.display = 'none';
}

function showError() {
    document.getElementById('modalLoading').style.display = 'none';
    document.getElementById('modalError').style.display = 'block';
}

async function loadEVBoxData(evboxId) {
    try {
        const [infoRes, activeRes, historyRes] = await Promise.all([
            fetch(`${API_BASE_MODAL}/laadpaal/${evboxId}/info`),
            fetch(`${API_BASE_MODAL}/laadpaal/${evboxId}/active-session`),
            fetch(`${API_BASE_MODAL}/laadpaal/${evboxId}/history`)
        ]);

        const info = await infoRes.json();
        displayEVBoxInfo(info);

        const activeSession = await activeRes.json();
        if (activeSession && !activeSession.message) displayActiveSession(activeSession);

        const history = await historyRes.json();
        displayHistory(history);

        document.getElementById('modalLoading').style.display = 'none';
    } catch (error) {
        console.error(error);
        showError();
    }
}

function displayEVBoxInfo(info) {
    document.getElementById('modalTitle').textContent = `Laadpaal ${info.EVBOXID.toString().padStart(3, '0')}`;
    document.getElementById('infoLocation').textContent = info.locationName;
    document.getElementById('infoAddress').textContent = `${info.address}, ${info.city}`;
    document.getElementById('infoVersion').textContent = info.softwareVersion;
    document.getElementById('evboxInfo').style.display = 'block';
}

function displayActiveSession(session) {
    // Format date
    const startDate = new Date(session.sessionStart);
    const formattedStart = startDate.toLocaleString('nl-NL', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });

    // Calculate duration
    const hours = Math.floor(session.durationMinutes / 60);
    const minutes = session.durationMinutes % 60;
    const durationText = `${hours}u ${minutes}m`;
    //TODO: fix timezone miscalculation

    document.getElementById('activeUser').textContent = session.userName;
    document.getElementById('activeStart').textContent = formattedStart;
    document.getElementById('activeDuration').textContent = durationText;
    document.getElementById('activeEnergy').textContent = session.energyUsage || 'Nog niet beschikbaar'; //TODO: calculate based on power and duration
    document.getElementById('activeCost').textContent = session.totalCost || '0.00'; //TODO: calculate based on energy usage
    document.getElementById('activeSession').style.display = 'block';
}

function displayHistory(sessions) {
    const sessionsList = document.getElementById('sessionsList');
    
    if (sessions.length === 0) {
        sessionsList.innerHTML = '<div class="empty-history">Geen laadgeschiedenis beschikbaar</div>';
    } else {
        sessionsList.innerHTML = '';
        
        sessions.forEach(session => {
            const sessionItem = document.createElement('div');
            sessionItem.className = 'session-item';
            sessionItem.onclick = () => showSessionDetail(session);
            
            const startDate = new Date(session.sessionStart);
            const endDate = new Date(session.sessionEnd);
            
            const formattedStart = startDate.toLocaleDateString('nl-NL', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric'
            });
            
            const hours = Math.floor(session.durationMinutes / 60);
            const minutes = session.durationMinutes % 60;
            
            sessionItem.innerHTML = `
                <div class="session-item-header">
                    <span>${formattedStart}</span>
                    <span>€${session.totalCost}</span>
                </div>
                <div class="session-item-details">
                    ${session.userName} • ${session.energyUsage} kWh • ${hours}u ${minutes}m
                </div>
            `;
            
            sessionsList.appendChild(sessionItem);
        });
    }
    
    document.getElementById('historicalSessions').style.display = 'block';
}

function showSessionDetail(session) {
    // Hide list, show detail
    document.getElementById('historicalSessions').style.display = 'none';
    
    // Format dates
    const startDate = new Date(session.sessionStart);
    const endDate = new Date(session.sessionEnd);
    
    const formattedStart = startDate.toLocaleString('nl-NL', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
    
    const formattedEnd = endDate.toLocaleString('nl-NL', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
    
    const hours = Math.floor(session.durationMinutes / 60);
    const minutes = session.durationMinutes % 60;
    const durationText = `${hours}u ${minutes}m`;
    
    // Populate detail view
    document.getElementById('detailUser').textContent = session.userName;
    document.getElementById('detailStart').textContent = formattedStart;
    document.getElementById('detailEnd').textContent = formattedEnd;
    document.getElementById('detailDuration').textContent = durationText;
    document.getElementById('detailEnergy').textContent = session.energyUsage;
    document.getElementById('detailCost').textContent = session.totalCost;
    
    document.getElementById('sessionDetail').style.display = 'block';
}

function backToList() {
    document.getElementById('sessionDetail').style.display = 'none';
    document.getElementById('historicalSessions').style.display = 'block';
}

// Event listeners
window.addEventListener("DOMContentLoaded", () => {
    fetchLaadpalen();
    
    // Modal close handlers
    const modal = document.getElementById('evboxModal');
    const closeBtn = document.querySelector('.close');
    const backBtn = document.getElementById('backToList');
    
    closeBtn.onclick = closeModal;
    backBtn.onclick = backToList;
    
    // Close when clicking outside modal
    window.onclick = (event) => {
        if (event.target === modal) {
            closeModal();
        }
    };
    
    setInterval(fetchLaadpalen, 30000);
});

