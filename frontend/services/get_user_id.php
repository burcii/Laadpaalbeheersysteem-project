<?php

function getUserID($jwt) {

    try {
        $parts = explode('.', $jwt);
        if (count($parts) !== 3) {
            throw new Exception("Invalid JWT format");
        }

        $payload = json_decode(base64_decode(strtr($parts[1], '-_', '+/')), true);
        if (!$payload || !isset($payload['user_id'])) {
            throw new Exception("JWT does not contain user_id");
        }

        $user_id = $payload['user_id'];
        return $user_id;
    } catch (Exception $e) {
        error_log("Error fetching userID: " . $e->getMessage());
        return null;
    }
}
?>