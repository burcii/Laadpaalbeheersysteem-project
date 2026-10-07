<!DOCTYPE html>
<html lang="nl">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Laadsessies</title>
    <link rel="stylesheet" href="styles/home.css">
    <link rel="stylesheet" href="components/dashboardMetrics/dashboardMetrics.css">
    <link rel="stylesheet" href="components/dateFilter/dateFilter.css">
</head>

<body>

    <?php include_once './components/nav.php'; ?>

    <!-- Main content -->
    <div class="main">
        <h1>Overzicht Sessies</h1>
        <?php include_once './components/dateFilter/dateFilter.php'; ?>
        <table id="sessionsTable">
            <thead>
                <tr>
                    <th>Sessie ID</th>
                    <th>Laadpaal ID</th>
                    <th>Locatie</th>
                    <th>Gebruiker</th>
                    <th>Start Tijd</th>
                    <th>Eind Tijd</th>
                    <th>Verbruikte Energie (kWh)</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody id="sessionsBody">
                <!-- Dynamisch geladen sessies komen hier -->
            </tbody>
        </table>
    </div>

    <script src="services/sessions.js"></script>

    <?php //include_once __DIR__ . '/../components/evboxModal/evboxModalComponent.php'; ?> <!-- Modal voor laadpaal details -->

</body>