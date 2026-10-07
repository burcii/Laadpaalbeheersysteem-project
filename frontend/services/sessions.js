window.API_BASE = window.API_BASE || 'http://127.0.0.1:8001';
const API_BASE = window.API_BASE;

document.addEventListener('DOMContentLoaded', function() {

    // Initial fetch
    fetchSessions();

});

const token = localStorage.getItem('user_token');

// Redirect if no token found
if (!token) {
    window.location.href = '/auth';
}

// Helper to decode JWT
function parseJwt(token) {
    try {
        return JSON.parse(atob(token.split('.')[1]));
    } catch (e) {
        return null;
    }
}

const decoded = parseJwt(token);

if (!decoded || !decoded.user_id) {
    localStorage.removeItem('user_token');
    window.location.href = '/auth';
}

function applyDateFilter() {
    // Implement date filter logic if needed

    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;

    fetchSessions(startDate, endDate);

}

function resetDateFilter() {
    
    // Set start date to first day of current month
    const now = new Date();
    const firstDay = new Date(now.getFullYear(), now.getMonth(), 1).toISOString().split('T')[0];

    document.getElementById('start-date').value = firstDay;
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('end-date').value = new Date(today).toISOString().split('T')[0];
    fetchSessions();
}

function fetchSessions(startDate = null, endDate = null) {
    const sessionsBody = document.getElementById('sessionsBody');
    let url = API_BASE + '/laadpaal/get-sessions?user_id=' + decoded.user_id;
    if (startDate && endDate) {
        url += `&start_date=${startDate}&end_date=${endDate}`;
    }

    console.log(`User ID from token: ${decoded.user_id}`);

    fetch(url)
    .then(response => response.json())
    .then(data => {

        sessionsBody.innerHTML = '';

        if (data.length > 0) {

            data.forEach(session => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${session.sessionID}</td>
                    <td>${session.EVBOXID}</td>
                    <td>${session.locationName}</td>
                    <td>${session.userName}</td>
                    <td>${session.sessionStart}</td>
                    <td>${session.sessionEnd}</td>
                    <td>${session.energyUsage}</td>
                    <td>${session.status}</td>
                `;
                sessionsBody.appendChild(row);
            });

        } else {
            sessionsBody.innerHTML = `
                <tr>
                    <td colspan="7" style="text-align:center;">
                        Nog geen laadsessies beschikbaar.
                    </td>
                </tr>
            `;
        }

    })
    .catch(error => console.error('Error fetching sessions:', error));
}