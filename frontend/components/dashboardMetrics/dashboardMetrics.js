// Get today's date and format as YYYY-MM-DD
function getTodayDate() {
    const today = new Date();
    return today.toISOString().split('T')[0];
}

// Get first day of current month
function getFirstDayOfMonth() {
    const today = new Date();
    const firstDay = new Date(today.getFullYear(), today.getMonth(), 1);
    return firstDay.toISOString().split('T')[0];
}

// Format large numbers with commas
function formatNumber(num) {
    return Math.round(num).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

// Format energy value with 2 decimal places
function formatEnergy(num) {
    return parseFloat(num).toFixed(2).replace('.', ',');
}

// Safe parse to number (accepts number or string with comma/dot)
function safeNumber(v) {
    if (v === null || typeof v === 'undefined' || v === '') return 0;
    if (typeof v === 'number') return v;
    const n = parseFloat(String(v).replace(',', '.'));
    return Number.isFinite(n) ? n : 0;
}

// Sum numeric field from array
function sumField(arr, field) {
    return arr.reduce((s, it) => s + safeNumber(it[field]), 0);
}

// Fetch dashboard metrics from backend
async function fetchDashboardMetrics(startDate, endDate) {
    try {
        // Show loading state
        if (document.getElementById("energy-value").textContent !== undefined) {
            document.getElementById("energy-value").textContent = "Laden...";
            document.getElementById("cost-value").textContent = "Laden...";
            document.getElementById("sessions-value").textContent = "Laden...";
            document.getElementById("chargers-value").textContent = "Laden...";
        }

        const response = await fetch(`http://localhost:8001/dashboard/metrics?start_date=${startDate}&end_date=${endDate}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Check for errors in response
        if (data.error) {
            console.error("API Error:", data.error);
            document.getElementById("energy-value").textContent = "Fout";
            document.getElementById("cost-value").textContent = "Fout";
            document.getElementById("sessions-value").textContent = "Fout";
            document.getElementById("chargers-value").textContent = "Fout";
            return;
        }

        // Update DOM with fetched data
        // Fetch Energy kWh from response
        const totalEnergy = (safeNumber(data.totalEnergy));
        document.getElementById("energy-value").textContent = `${formatEnergy(totalEnergy)} kWh`;

        // Fetch Total cost from response
        const totalCost = (safeNumber(data.totalCost));
        document.getElementById("cost-value").textContent = `€ ${formatEnergy(totalCost)}`;
        
        // Fetch Total sessions from response
        const totalSessions = Number(data.totalSessions);
        document.getElementById("sessions-value").textContent = formatNumber(totalSessions);
        document.getElementById("chargers-value").textContent = formatNumber(data.activeChargers);

    } catch (error) {
        console.error("Error fetching dashboard metrics:", error);
        document.getElementById("energy-value").textContent = "Fout";
        document.getElementById("cost-value").textContent = "Fout";
        document.getElementById("sessions-value").textContent = "Fout";
        document.getElementById("chargers-value").textContent = "Fout";
    }
}

// Date filter functions
function applyDateFilter() {
    const startDate = document.getElementById("start-date").value;
    const endDate = document.getElementById("end-date").value;
    
    if (!startDate || !endDate) {
        alert("Selecteer beide datums");
        return;
    }
    
    if (startDate > endDate) {
        alert("Startdatum moet voor einddatum liggen");
        return;
    }
    
    fetchDashboardMetrics(startDate, endDate);
}

function resetDateFilter() {
    const startDate = getFirstDayOfMonth();
    const endDate = getTodayDate();
    
    document.getElementById("start-date").value = startDate;
    document.getElementById("end-date").value = endDate;
    
    fetchDashboardMetrics(startDate, endDate);
}

// Initialize dashboard metrics on page load
window.addEventListener("DOMContentLoaded", () => {
    const startDate = getFirstDayOfMonth();
    const endDate = getTodayDate();
    
    fetchDashboardMetrics(startDate, endDate);
    
    // Optional: Refresh every 60 seconds
    setInterval(() => {
        const currentStartDate = document.getElementById("start-date").value;
        const currentEndDate = document.getElementById("end-date").value;
        fetchDashboardMetrics(currentStartDate, currentEndDate);
    }, 60000);
});

// Export functions for use in date filter
window.updateDashboardMetrics = function(startDate, endDate) {
    fetchDashboardMetrics(startDate, endDate);
};
