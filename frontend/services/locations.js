document.addEventListener('DOMContentLoaded', function() {
    loadLocations();
});

function loadLocations() {
    fetch('http://localhost:8001/locaties')
    .then(response => response.json())
    .then(data => {
        const locationsBody = document.getElementById('locationsBody');
        locationsBody.innerHTML = ''; // Clear existing rows

        data.forEach(location => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${location.locationID}</td>
                <td>${location.locationName}</td>
                <td>${location.address}</td>
                <td>${location.city}</td>
                <td>
                    <div class="actions-cell">
                        <button class="action-btn" title="Locatie bewerken" ">✎</button>
                    </div>
                </td>
            `;
            locationsBody.appendChild(row);
        });

    })
    .catch(error => console.error('Error fetching locations:', error));
}