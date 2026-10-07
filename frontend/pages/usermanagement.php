<?php 
require __DIR__ . '/../components/popupModel/popupModel.php'; 
require __DIR__ . '/../components/confirmationModel/confirmationModel.php';
?>

<!DOCTYPE html>
<html lang="nl">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gebruikersbeheer</title>
    <link rel="stylesheet" href="styles/usermanagement.css">
    <link href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css' rel='stylesheet'>
</head>

<body>
    <?php include_once './components/nav.php'; ?>
    <div class="wrapper">
        <div class="page-header">
            <div class="header-text">
                <h1>Gebruikersbeheer</h1>
                <p>Beheer gebruikers van het oplaadsysteem en hun passen</p>
            </div>
            <button id="openAddUserBtn">+ Gebruiker Toevoegen</button>  
        </div>
        <i style="font-size: 15px;">*Je kunt op de Naam, Email en Pasnummer klikken om te zoeken op een van die categorien. Klik buiten het scherm om te de-selecteren.</i>
        <br>
        
        <form action="" class="search-form-wrapper">
            <div class="search">
                <i class='bx bx-search search-icon'></i>
                <input id="searchInput" class="search-input" type="search" placeholder="zoeken op naam, e-mailadres of pasnummer">
                
                <div class="status-dropdown-container">
                    <select id="statusFilterSelect">
                        <option value="alle">Alle Status</option>
                        <option value="actief">Actief</option>
                        <option value="inactief">Inactief</option>
                        <option value="geblokkeerd">Geblokkeerd</option>
                    </select>
                </div>
            </div>
        </form>
        
        <table>
            <thead>
                <tr>
                    <th id="headerName" class="clickable-header" data-search-field="naam">Naam</th>
                    <th id="headerEmail" class="clickable-header" data-search-field="e-mailadres">E-mail</th>
                    <th id="headerPhone" class="clickable-header" data-search-field="telefoon">Telefoon</th>
                    <th id="headerPassNumber" class="clickable-header" data-search-field="pasnummer">Pasnummer</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>
            </thead>

            <tbody id="userTableBody">
            </tbody>
         </table>
    </div>

    <div id="addUserModal" class="modal">
        <div class="modal-content">
            <span id="closeModalBtn">&times;</span>
            <h2>Voeg Gebruiker Toevoegen</h2>
            <form id="addUserForm" method="POST" action="add_user.php">
                <label for="name">Naam:</label>
                <input type="text" id="name" name="name" required>

                <label for="email">Email:</label>
                <input type="email" id="email" name="email" required>

                <label for="phone">Telefoonnummmer:</label>
                <input type="tel" id="phone" name="phone">

                <label for="pass_number">Pasnummer:</label>
                <input type="text" id="pass_number" name="pass_number" required>

                <div class="form-buttons">
                    <button type="submit">Voeg gebruiker</button>
                    <button type="button" id="cancelBtn">Cancel</button>
                </div>
            </form>
        </div>
    </div>
    
    <div id="userDetailsModal" class="modal">
        <div class="modal-content user-details-modal">
            <span id="closeDetailsBtn" class="close-btn">&times;</span>
            <h2>Gebruikersdetails</h2>
            <div class="user-details-content">
                <div class="user-header">
                    <h3 id="detailsUserName"></h3>
                    <p id="detailsUserEmail" class="user-email"></p>
                </div>

                <div class="details-grid">
                    <div class="details-row">
                        <span class="detail-label">Status</span>
                        <span id="detailsUserStatus" class="status active">
                            <i class="bx bx-check-circle"></i>
                            Actief
                        </span>
                    </div>

                    <div class="details-row">
                        <span class="detail-label">Telefoonnummer</span>
                        <span id="detailsUserPhone" class="detail-value"></span>
                    </div>
                    
                    <div class="details-row">
                        <span class="detail-label">
                            <i class="bx bx-calendar"></i>
                            Toevoegdatum
                        </span>
                        <span id="detailsJoinDate" class="detail-value"></span>
                    </div>

                    <div class="details-row">
                        <span class="detail-label">
                            <i class="bx bx-bolt-square"></i>
                            Laatste laadbeurt
                        </span>
                        <span id="detailsLastCharge" class="detail-value"></span>
                    </div>

                    <div class="details-row">
                        <h4>Pasnummers</h4>
                        <span id="detailsPassNumber" class="detail-value"></span>
                    </div>
                </div>
            </div>
            
        </div>
    </div>

    <div id="editUserModal" class="modal">
        <div class="modal-content">
            <span id="closeEditModalBtn" class="close-btn">&times;</span>
            <h2>Gebruiker Bewerken</h2>
            <form id="editUserForm">
                <input type="hidden" id="editUserId" name="id">
                
                <label for="editName">Naam:</label>
                <input type="text" id="editName" name="name" required>

                <label for="editEmail">Email:</label>
                <input type="email" id="editEmail" name="email" required>

                <label for="editPhone">Telefoonnummer:</label>
                <input type="tel" id="editPhone" name="phone">

                <label for="editPassNumber">Pasnummer:</label>
                <input type="text" id="editPassNumber" name="pass_number" required>

                <div class="form-buttons">
                    <button type="submit">Wijzigingen Opslaan</button>
                    <button type="button" id="cancelEditBtn">Annuleren</button>
                </div>
            </form>
        </div>
    </div>

    <script type="module" src="services/usermanagement/main.js?cache_kill=1234567890"></script>
</body>

</html>