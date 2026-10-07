<?php
// set-session.php
session_start();
header('Content-Type: application/json');

$input = json_decode(file_get_contents('php://input'), true);
if (!isset($input['token']) || empty($input['token'])) {
    http_response_code(400);
    echo json_encode(['error' => 'Missing token']);
    exit;
}

$_SESSION['user_token'] = $input['token'];

echo json_encode(['success' => true, 'session_id' => session_id()]);
