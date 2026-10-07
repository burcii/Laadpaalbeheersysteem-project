<?php
header('Content-Type: application/json');

// Lees parameter
$state = $_GET['state'] ?? null;

if (!$state || !in_array($state, ['on', 'off'])) {
    echo json_encode(["success" => false, "message" => "Ongeldige parameter"]);
    exit;
}

// Hier zou je database-update of API-call naar backend doen
// Voorbeeld: update alle laadpalen status in DB
// ...

echo json_encode([
    "success" => true,
    "message" => "Alle laadpalen zijn succesvol op '$state' gezet."
]);
