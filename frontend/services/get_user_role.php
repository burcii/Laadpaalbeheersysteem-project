<?php
require 'api.php';

function getUserRole($jwt) {
    $api = new ApiClient('http://localhost:8001');

    try {
        // Decode JWT without verification to get user_id
        $parts = explode('.', $jwt);
        if (count($parts) !== 3) {
            throw new Exception("Invalid JWT format");
        }

        $payload = json_decode(base64_decode(strtr($parts[1], '-_', '+/')), true);
        if (!$payload || !isset($payload['user_id'])) {
            throw new Exception("JWT does not contain user_id");
        }

        $user_id = $payload['user_id'];

        // Send GET request with user_id in the URL
        $endpoint = '/get_role/' . urlencode($user_id);
        $response = $api->get($endpoint);

        if ($response['status'] !== 200) {
            error_log("Flask returned status " . $response['status']);
            return null;
        }

        return $response['data']['role'] ?? null;

    } catch (Exception $e) {
        error_log("Error fetching user role: " . $e->getMessage());
        return null;
    }
}

