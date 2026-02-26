<?php

header('Content-Type: application/json');

// 1. Get Environment Variables
$botToken = '';
$chatId = '';

// 2. Read JSON Input
$input = json_decode(file_get_contents('php://input'), true);

$name     = $input['name'] ?? 'Anonym';
$question = $input['question'] ?? '';

// 3. Validation
if (empty($question) || empty($botToken) || empty($chatId)) {
    http_response_code(400);
    echo json_encode([
        "status" => "error",
        "message" => "Chybí otázka nebo konfigurace serveru."
    ]);
    exit;
}

// 4. Prepare Telegram Message
$message  = "📩 *Nová zpráva z webu*\n\n";
$message .= "👤 *Od:* " . strip_tags($name) . "\n";
$message .= "❓ *Otázka:* " . strip_tags($question);

$url = "https://api.telegram.org/bot{$botToken}/sendMessage";

$data = [
    'chat_id'    => $chatId,
    'text'       => $message,
    'parse_mode' => 'Markdown'
];

// 5. Send to Telegram using built-in PHP stream context
$options = [
    'http' => [
        'method'  => 'POST',
        'header'  => "Content-Type: application/x-www-form-urlencoded\r\n",
        'content' => http_build_query($data),
        'ignore_errors' => true // allows reading response even on non-200
    ],
    'ssl' => [
        'verify_peer'      => false,
        'verify_peer_name' => false,
        'allow_self_signed'=> true
    ]
];

$context = stream_context_create($options);
$result  = file_get_contents($url, false, $context);

// Extract HTTP status code
$httpCode = 0;
if (isset($http_response_header[0])) {
    preg_match('{HTTP/\S*\s(\d{3})}', $http_response_header[0], $match);
    $httpCode = $match[1] ?? 0;
}

// 6. Return Response to Frontend
if ($httpCode == 200) {
    echo json_encode(["status" => "success"]);
} else {
    http_response_code(500);
    echo json_encode([
        "status" => "error",
        "httpCode" => $httpCode,
        "debug"  => $result,
        "options" => $options,
        "test" => $url . '?' . http_build_query($data)
    ]);
}

?>
