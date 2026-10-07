<!-- Modal Overlay -->
<div id="evboxModal" class="modal">
    <div class="modal-content">
        <div class="modal-header">
            <h2 id="modalTitle">Laadpaal Details</h2>
            <span class="close">&times;</span>
        </div>
        <div class="modal-body">
            <!-- Loading State -->
            <div id="modalLoading" class="modal-loading">
                <p>Laden...</p>
            </div>

            <!-- Error State -->
            <div id="modalError" class="modal-error" style="display: none;">
                <p>Er is een fout opgetreden bij het laden van de gegevens.</p>
            </div>

            <!-- EVBox Info -->
            <div id="evboxInfo" style="display: none;">
                <div class="info-section">
                    <h3>Informatie</h3>
                    <p><strong>Locatie:</strong> <span id="infoLocation"></span></p>
                    <p><strong>Adres:</strong> <span id="infoAddress"></span></p>
                    <p><strong>Software versie:</strong> <span id="infoVersion"></span></p>
                </div>
            </div>

            <!-- Active Session -->
            <div id="activeSession" style="display: none;">
                <div class="info-section active-session">
                    <h3>Actieve Sessie</h3>
                    <p><strong>Gebruiker:</strong> <span id="activeUser"></span></p>
                    <p><strong>Gestart:</strong> <span id="activeStart"></span></p>
                    <p><strong>Duur:</strong> <span id="activeDuration"></span></p>
                    <p><strong>Energieverbruik:</strong> <span id="activeEnergy"></span> kWh</p>
                    <p><strong>Huidige kosten:</strong> €<span id="activeCost"></span></p>
                </div>
            </div>

            <!-- No Active Session -->
            <div id="noActiveSession" style="display: none;">
                <div class="info-section">
                    <p><em>Geen actieve sessie op dit moment</em></p>
                </div>
            </div>

            <!-- Historical Sessions -->
            <div id="historicalSessions" style="display: none;">
                <div class="info-section">
                    <h3>Laadgeschiedenis</h3>
                    <div id="sessionsList"></div>
                </div>
            </div>

            <!-- Session Detail View -->
            <div id="sessionDetail" style="display: none;">
                <button id="backToList" class="back-button">← Terug naar overzicht</button>
                <div class="info-section">
                    <h3>Sessie Details</h3>
                    <p><strong>Gebruiker:</strong> <span id="detailUser"></span></p>
                    <p><strong>Start:</strong> <span id="detailStart"></span></p>
                    <p><strong>Einde:</strong> <span id="detailEnd"></span></p>
                    <p><strong>Duur:</strong> <span id="detailDuration"></span></p>
                    <p><strong>Energieverbruik:</strong> <span id="detailEnergy"></span> kWh</p>
                    <p><strong>Totale kosten:</strong> €<span id="detailCost"></span></p>
                </div>
            </div>
        </div>
    </div>
</div>