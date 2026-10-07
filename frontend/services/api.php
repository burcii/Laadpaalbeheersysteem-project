<?php
class ApiClient {
    private $baseUrl;
    private $headers;
    private $withCredentials;

    public function __construct($baseUrl, $withCredentials = false, $headers = []) {
        $this->baseUrl = rtrim($baseUrl, '/');
        $this->withCredentials = $withCredentials;
        $this->headers = array_merge([
            'Accept: application/json',
            'Content-Type: application/json'
        ], $headers);
    }

    private function request($method, $endpoint, $data = null, $token = null) {
        $url = $this->baseUrl . '/' . ltrim($endpoint, '/');
        $ch = curl_init($url);

        $opts = [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_CUSTOMREQUEST  => strtoupper($method),
            CURLOPT_HTTPHEADER     => $this->buildHeaders($token),
        ];

        if ($this->withCredentials) {
            $opts[CURLOPT_COOKIEFILE] = ''; // enable cookie handling
            $opts[CURLOPT_COOKIEJAR]  = '';
        }

        if ($data !== null) {
            $opts[CURLOPT_POSTFIELDS] = json_encode($data);
        }

        curl_setopt_array($ch, $opts);

        $response = curl_exec($ch);
        $error = curl_error($ch);
        $status = curl_getinfo($ch, CURLINFO_HTTP_CODE);

        curl_close($ch);

        if ($error) {
            throw new Exception("cURL error: " . $error);
        }

        return [
            'status' => $status,
            'data'   => json_decode($response, true),
            'raw'    => $response
        ];
    }

    private function buildHeaders($token) {
        $headers = $this->headers;
        if ($token) {
            $headers[] = 'Authorization: Bearer ' . $token;
        }
        return $headers;
    }

    public function get($endpoint, $token = null) {
        return $this->request('GET', $endpoint, null, $token);
    }

    public function post($endpoint, $data, $token = null) {
        return $this->request('POST', $endpoint, $data, $token);
    }

    public function put($endpoint, $data, $token = null) {
        return $this->request('PUT', $endpoint, $data, $token);
    }

    public function delete($endpoint, $token = null) {
        return $this->request('DELETE', $endpoint, null, $token);
    }
}
