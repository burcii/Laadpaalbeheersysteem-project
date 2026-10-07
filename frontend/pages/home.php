<!DOCTYPE html>
<html lang="nl">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
    <link rel="stylesheet" href="styles/home.css">
    <link rel="stylesheet" href="components/dashboardMetrics/dashboardMetrics.css">
    <link rel="stylesheet" href="components/dateFilter/dateFilter.css">
</head>

<body>
    <?php include_once './components/nav.php'; ?>

    <!-- Main content -->
    <div class="main">
        <h1>Overzicht Laadpalen</h1>
        <?php include_once './components/dateFilter/dateFilter.php'; ?>
        <?php include_once './components/dashboardMetrics/dashBoardMetrics.php'; ?>
        <table id="chargersTable">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Locatie</th>
                    <th>Status</th>
                    <th>Laatste sessie</th>
                </tr>
            </thead>
            <tbody id="chargersBody">
                <!-- Dynamisch geladen laadpalen komen hier -->
            </tbody>
        </table>
        <div class="actions">
                <button onclick="openConfirmDialog('Weet je zeker dat je ALLE laadpalen wilt AAN zetten?', function(){ toggleChargers('on'); })">
                    Alle laadpalen AAN
                </button>
                <button onclick="openConfirmDialog('Weet je zeker dat je ALLE laadpalen wilt UIT zetten?', function(){ toggleChargers('off'); })">
                    Alle laadpalen UIT
                </button>
            </div>
    </div>

    <!----------------------- Bevestigingsmodal --------------------------->
    <div id="confirmModal" class="modal">
      <div class="modal-content" style="padding: 20px !important; max-width: 25% !important;">
        <p id="confirmMessage"></p>
        <div class="modal-actions">
          <button id="confirmYes" class="btn-confirm">Ja</button>
          <button onclick="closeConfirmDialog()" class="btn-cancel">Nee</button>
        </div>
      </div>
    </div>
    <?php include_once __DIR__ . '/../components/evboxModal/evboxModalComponent.php'; ?> <!-- Modal voor laadpaal details -->
</body>

<script src="services/home.js"></script>
<script src="components/dashboardMetrics/dashboardMetrics.js"></script>

</html>