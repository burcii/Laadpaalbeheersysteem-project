<!DOCTYPE html>
<html lang="nl">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Locaties</title>
    <link rel="stylesheet" href="styles/home.css">
</head>

<body>

    <?php include_once './components/nav.php'; ?>

    <!-- Main content -->
    <div class="main">
        <h1>Overzicht Locaties</h1>
        <table id="sessionsTable">
            <thead>
                <tr>
                    <th style="width: 10%;">Locatie ID</th>
                    <th>Naam</th>
                    <th>Adres</th>
                    <th>Stad</th>
                    <th>Acties</th>
                </tr>
            </thead>
            <tbody id="locationsBody">
                <!-- Dynamisch geladen sessies komen hier -->
            </tbody>
        </table>
    </div>

    <script src="services/locations.js"></script>

    <?php //include_once __DIR__ . '/../components/evboxModal/evboxModalComponent.php'; ?> <!-- Modal voor laadpaal details -->

</body>