<?php
session_start();
require 'services/get_user_role.php';

$uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

// Serve static files directly if they exist
$requestedFile = __DIR__ . $uri;
if ($uri !== '/' && file_exists($requestedFile)) {
    return false; // Let the built-in server handle it
}

$routes = [
    '' => 'pages/home.php',
    'auth' => 'pages/auth.php',
    'usermanagement' => 'pages/usermanagement.php',
    'edit_user' => 'pages/edit_user.php',
    'laadpaalbeheer' => 'pages/laadpaalbeheer.php',
    'sessies' => 'pages/sessions.php',
    'locaties' => 'pages/locations.php',
];

if ($uri !== '/auth') {
    if (!isset($_SESSION['user_token'])) {
        header('Location: /auth');
        exit();
    }

    $jwt = $_SESSION['user_token'];
    $userRole = getUserRole($jwt);
}

$uriTrimmed = trim($uri, '/');

if (array_key_exists($uriTrimmed, $routes)) {
    // Restrict access to usermanagement page
    // Log user role
    if ($uriTrimmed === 'usermanagement') {
        if ($userRole !== 'management' && $userRole !== 'admin') {
            http_response_code(403);
            require 'pages/403.php';
            exit();
        }
    }

    require $routes[$uriTrimmed];
} else {
    http_response_code(404);
    require 'pages/404.php';
}
