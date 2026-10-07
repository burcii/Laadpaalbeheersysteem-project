<!-- <?php
        ?> -->
<!DOCTYPE html>
<html lang="nl">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Laadpaal Beheer</title>
    <link rel="stylesheet" href="styles/laadpaalbeheer.css">
</head>

<body>
    <?php include_once './components/nav.php'; ?>
    <div class="wrapper">
        <div id="heading">
            <div class="heading-text">
                <h1>Laadpaalbeheer</h1>
                <p>Configureer en beheer uw laadpaalen</p>
            </div>
            <button id="addChargerBtn">Laadpaal Toevoegen</button>
        </div>
        
        <!-- Status teller kaarten -->
        <div class="status-counters">
            <div class="counter-card">
                <div class="counter-icon total">🗲</div>
                <div class="counter-content">
                    <p class="counter-label">Totaal</p>
                    <p class="counter-value" id="totalChargers">0</p>
                </div>
            </div>

            <div class="counter-card">
                <div class="counter-icon online">✅</div>
                <div class="counter-content">
                    <p class="counter-label">Online</p>
                    <p class="counter-value online-text" id="onlineChargers">0</p>
                </div>
            </div>

            <div class="counter-card">
                <div class="counter-icon offline">❌</div>
                <div class="counter-content">
                    <p class="counter-label">Offline</p>
                    <p class="counter-value offline-text" id="offlineChargers">0</p>
                </div>
            </div> 

            <div class="counter-card">
                <div class="counter-icon maintenance">🛠️</div>
                <div class="counter-content">
                    <p class="counter-label">Onderhoud</p>
                    <p class="counter-value maintenance-text" id="maintenanceChargers">0</p>
                </div>
            </div>
        </div>

         <!-- Laadpaal Table -->
        <table id="chargersTable">
            <thead>
                <tr>
                    <th>Naam</th>
                    <th>Locatie</th>
                    <th>Status</th>
                    <th>Vermogen</th>
                    <th>Prijs/kWh</th>
                    <th>Totaal Verbruik (kWh)</th>
                    <th>Acties</th>
                </tr>
            </thead>
            <tbody id="chargersBody">
                <!-- Dynamisch geladen laadpalen komen hier -->
            </tbody>
        </table>

        <!-- Laadpaal Toevoegen Modal -->
        <div id="addChargerModal" class="modal">
            <div class="modal-content">
                <span id="closeModalBtn">&times;</span>
                <h2>Laadpaal Toevoegen</h2>
                <form id="addChargerForm">
                    <div class="form-group">
                        <label for="Cname">Naam *</label>
                        <input type="text" id="Cname" name="Cname" placeholder="Laadpaal naam" required>
                    </div>

                    <div class="form-group">
                        <label for="location">Locatie *</label>
                        <input type="text" id="location" name="location" placeholder="Locatienaam" required>
                    </div>

                    <div class="form-group full-width">
                        <label for="adres">Adres</label>
                        <input type="text" id="adres" name="adres" placeholder="Straatnaam en huisnummer">
                    </div>

                    <div class="form-group">
                        <label for="maxVermogen">Max Vermogen(kW)</label>
                        <select name="maxVermogen" id="maxVermogen">
                            <option value="11">11 kW</option>
                            <option value="22">22 kW</option>
                            <option value="50">50 kW</option>
                            <option value="150">150 kW</option>
                            <option value="350">350 kW</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="prijs">Prijs per kWh(€)</label>
                        <input type="number" id="prijs" name="prijs" value="0.35" step="0.01" min="0">
                    </div>

                    <div class="form-group full-width">
                        <label for="status">Status</label>
                        <select name="status" id="status">
                            <option value="on">Online</option>
                            <option value="off">Offline</option>
                            <option value="ond">Onderhoud</option>
                        </select>
                    </div>

                    <div class="buttons">
                        <button type="button" id="cancelBtn">Annuleren</button>
                        <button type="submit">Toevoegen</button>
                    </div>
                </form>
            </div>
        </div>

        <!-- Laadpaal bewerken modal -->
         <div id="editChargerModal" class="modal">
            <div class="modal-content">
                <span id="closeEditModalBtn">&times;</span>
                <h2>Laadpaal Bewerken</h2>
                <form id="editChargerForm">
                    <div class="form-group">
                        <label for="Cname">Naam *</label>
                        <input type="text" id="Cname" name="Cname" placeholder="Laadpaal naam" required>
                    </div>

                    <div class="form-group">
                        <label for="location">Locatie *</label>
                        <input type="text" id="location" name="location" placeholder="Locatienaam" required>
                    </div>

                    <div class="form-group full-width">
                        <label for="adres">Adres</label>
                        <input type="text" id="adres" name="adres" placeholder="Straatnaam en huisnummer">
                    </div>

                    <div class="form-group">
                        <label for="maxVermogen">Max Vermogen(kW)</label>
                        <select name="maxVermogen" id="maxVermogen">
                            <option value="11">11 kW</option>
                            <option value="22">22 kW</option>
                            <option value="50">50 kW</option>
                            <option value="150">150 kW</option>
                            <option value="350">350 kW</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="prijs">Prijs per kWh(€)</label>
                        <input type="number" id="prijs" name="prijs" value="0.35" step="0.01" min="0">
                    </div>

                    <div class="form-group full-width">
                        <label for="status">Status</label>
                        <select name="status" id="status">
                            <option value="on">Online</option>
                            <option value="off">Offline</option>
                            <option value="ond">Onderhoud</option>
                        </select>
                    </div>

                    <div class="buttons">
                        <button type="button" id="cancelEditBtn">Annuleren</button>
                        <button type="submit">Opslaan</button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <!-- Scripts -->
    <script src="../services/laadpaalbeheer/laadpaalbeheer.js"></script>
</body>

</html>