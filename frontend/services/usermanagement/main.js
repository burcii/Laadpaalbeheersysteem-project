// main.js
import { apiAddUser, apiUpdateUser, apiToggleBlockUser, apiDeleteUser, apiGetUsers } from './api.js';
import { initSearch } from './search.js';

// ---- DOM ELEMENTS ----
const addUserForm = document.getElementById('addUserForm');
const editUserForm = document.getElementById('editUserForm');
const searchInput = document.getElementById('searchInput');
const clickableHeaders = document.querySelectorAll('.clickable-header');
const statusFilterSelect = document.getElementById('statusFilterSelect');
const userTableBody = document.getElementById('userTableBody');
const addUserModal = document.getElementById('addUserModal');
const closeModalBtn = document.getElementById('closeModalBtn');
const cancelBtn = document.getElementById('cancelBtn');
const userDetailsModal = document.getElementById('userDetailsModal');
const closeDetailsBtn = document.getElementById('closeDetailsBtn');
const editUserModal = document.getElementById('editUserModal');
const closeEditModalBtn = document.getElementById('closeEditModalBtn');
const cancelEditBtn = document.getElementById('cancelEditBtn');
const openAddUserBtn = document.getElementById('openAddUserBtn');
const defaultPlaceholder = "zoeken op naam, e-mailadres of pasnummer";

// --- HELPER FUNCTIONS ---

// Prevent Enter from submitting forms
function preventEnterSubmit(e) {
    if (e.key === 'Enter' || e.keyCode === 13) e.preventDefault();
}
searchInput.addEventListener('keydown', preventEnterSubmit);
addUserForm.addEventListener('keydown', preventEnterSubmit);
editUserForm.addEventListener('keydown', preventEnterSubmit);

// --- TABLE / UI FUNCTIONS ---

function appendUserToTable(user) {
    const row = document.createElement('tr');
    row.dataset.userId = user.id;
    row.dataset.name = user.name.toLowerCase();
    row.dataset.email = user.email.toLowerCase();
    row.dataset.pass = (user.pass_number || '').toLowerCase();
    row.dataset.phone = (user.phone || '').toLowerCase();
    row.dataset.status = (user.status || 'inactief').toLowerCase();

    const isActive = user.status === 'Actief';
    const isBlocked = user.status === 'Geblokkeerd';

    row.innerHTML = `
        <td>${user.name}</td>
        <td>${user.email}</td>
        <td>${user.phone || '-'}</td>
        <td>${user.pass_number}</td>
        <td>
            <span class="status ${isActive ? 'active' : 'blocked'}">
                <i class='bx ${isActive ? 'bx-check-circle' : 'bx-x-circle'}'></i>
                ${user.status}
            </span>
        </td>
        <td class="actions">
            <i class="bx bx-show view-icon"></i>
            <i class="bx bx-edit edit-icon"></i>
            <i class="bx ${isBlocked ? 'bx-lock-open' : 'bx-lock'} block-icon"></i>
            <i class="bx bx-trash delete-icon"></i>
        </td>
    `;
    userTableBody.appendChild(row);

    row.querySelector('.view-icon').addEventListener('click', () => showUserDetails(user));
    row.querySelector('.edit-icon').addEventListener('click', () => showEditUserModal(user));
    row.querySelector('.block-icon').addEventListener('click', () => handleBlockUser(user));
    row.querySelector('.delete-icon').addEventListener('click', () => handleDeleteUser(user, row));
}

function updateUserInTable(user) {
    const rows = userTableBody.querySelectorAll('tr');
    rows.forEach(row => {
        if (row.dataset.userId == user.id) {
            row.dataset.name = user.name.toLowerCase();
            row.dataset.email = user.email.toLowerCase();
            row.dataset.pass = (user.pass_number || '').toLowerCase();
            row.dataset.phone = (user.phone || '').toLowerCase();
            row.dataset.status = (user.status || 'inactief').toLowerCase();

            const cells = row.cells;
            cells[0].textContent = user.name;
            cells[1].textContent = user.email;
            cells[2].textContent = user.phone || '-';
            cells[3].textContent = user.pass_number;

            const isActive = user.status === 'Actief';
            cells[4].innerHTML = `
                <span class="status ${isActive ? 'active' : 'blocked'}">
                    <i class='bx ${isActive ? 'bx-check-circle' : 'bx-x-circle'}'></i>
                    ${user.status}
                </span>
            `;

            const blockIcon = row.querySelector('.block-icon');
            blockIcon.className = user.status === 'Geblokkeerd' ? 'bx bx-lock-open block-icon' : 'bx bx-lock block-icon';
            blockIcon.title = user.status === 'Geblokkeerd' ? 'Deblokkeren' : 'Blokkeren';
        }
    });
}

function showUserDetails(user) {
    document.getElementById('detailsUserName').textContent = user.name || 'N/A';
    document.getElementById('detailsUserEmail').textContent = user.email || 'N/A';
    document.getElementById('detailsUserPhone').textContent = user.phone || '-';
    const statusElement = document.getElementById('detailsUserStatus');
    const isActive = (user.status || 'Actief').toLowerCase() === 'actief';
    statusElement.className = isActive ? 'status active' : 'status blocked';
    statusElement.innerHTML = `<i class='bx ${isActive ? 'bx-check-circle' : 'bx-x-circle'}'></i> ${user.status || 'Actief'}`;
    document.getElementById('detailsJoinDate').textContent = user.join_date || user.created_at || '-';
    document.getElementById('detailsLastCharge').textContent = user.last_charge || '-';
    document.getElementById('detailsPassNumber').textContent = user.pass_number || '-';
    userDetailsModal.style.display = 'flex';
}

function showEditUserModal(user) {
    document.getElementById('editUserId').value = user.id || '';
    document.getElementById('editName').value = user.name || '';
    document.getElementById('editEmail').value = user.email || '';
    document.getElementById('editPhone').value = user.phone || '';
    document.getElementById('editPassNumber').value = user.pass_number || '';
    editUserForm.dataset.userId = user.id;
    editUserModal.style.display = 'flex';
}

// --- API HANDLERS ---
addUserForm.addEventListener('submit', async e => {
    e.preventDefault();
    const formData = new FormData(addUserForm);
    const data = await apiAddUser(formData);
    if (data.success) {
        appendUserToTable(data.user);
        addUserModal.style.display = 'none';
        addUserForm.reset();
        showPopupModel('Gebruiker succesvol toegevoegd!');
    } else {
        showPopupModel(data.error || 'Fout bij toevoegen.');
    }
});

editUserForm.addEventListener('submit', async e => {
    e.preventDefault();
    const formData = new FormData(editUserForm);
    const userId = document.getElementById('editUserId').value;
    const data = await apiUpdateUser(userId, formData);
    if (data.success) {
        updateUserInTable(data.user);
        editUserModal.style.display = 'none';
        showPopupModel('Gebruiker succesvol bijgewerkt!');
    } else {
        showPopupModel(data.error || 'Bijwerken mislukt.');
    }
});

async function handleBlockUser(user) {
    const confirmAction = await showConfirmation(`Weet je zeker dat je ${user.name} wilt ${user.status === 'Geblokkeerd' ? 'deblokkeren' : 'blokkeren'}?`);
    if (!confirmAction) return;
    const data = await apiToggleBlockUser(user.id);
    if (data.success) {
        updateUserInTable(data.user);
        showPopupModel(`Gebruiker succesvol gewijzigd!`);
        handleSearch();
    } else {
        showPopupModel(data.error || 'Actie mislukt.');
    }
}

async function handleDeleteUser(user, row) {
    const ok = await showConfirmation(`Weet je zeker dat je ${user.name} wilt verwijderen?`);
    if (!ok) return;
    const data = await apiDeleteUser(user.id);
    if (data.succes) {
        row.remove();
        showPopupModel('Gebruiker succesvol verwijderd!');
    } else {
        showPopupModel(data.error || 'Verwijderen mislukt.');
    }
}

// --- MODALS ---
openAddUserBtn.addEventListener('click', () => addUserModal.style.display = 'flex');
closeModalBtn.addEventListener('click', () => addUserModal.style.display = 'none');
cancelBtn.addEventListener('click', () => addUserModal.style.display = 'none');
closeDetailsBtn.addEventListener('click', () => userDetailsModal.style.display = 'none');
closeEditModalBtn.addEventListener('click', () => editUserModal.style.display = 'none');
cancelEditBtn.addEventListener('click', () => editUserModal.style.display = 'none');
window.addEventListener('click', e => {
    if (e.target === addUserModal) addUserModal.style.display = 'none';
    if (e.target === userDetailsModal) userDetailsModal.style.display = 'none';
    if (e.target === editUserModal) editUserModal.style.display = 'none';
});

// --- SEARCH ---
const { handleSearch: searchHandler } = initSearch(searchInput, clickableHeaders, statusFilterSelect, userTableBody, defaultPlaceholder);
const handleSearch = searchHandler;

// --- LOAD USERS ---
async function loadUsers() {
    const data = await apiGetUsers();
    if (data.success && data.users) {
        userTableBody.innerHTML = '';
        data.users.forEach(u => appendUserToTable(u));
        handleSearch();
    }
}
document.addEventListener('DOMContentLoaded', loadUsers);
