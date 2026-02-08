<?php

header('Content-Type: application/json');

// 1. Get Environment Variables
$botToken = getenv('TELEGRAM_BOT_TOKEN');
$chatId = getenv('TELEGRAM_CHAT_ID');

// 2. Read JSON Input
$input = json_decode(file_get_contents('php://input'), true);

$name = $input['name'] ?? 'Anonym';
$question = $input['question'] ?? '';

// 3. Validation
if (empty($question) || empty($botToken) || empty($chatId)) {
    http_response_code(400);
    echo json_encode(["status" => "error", "message" => "Chybí otázka nebo konfigurace serveru."]);
    exit;
}

// 4. Prepare Telegram Message
$message = "📩 *Nová zpráva z webu*\n\n";
$message .= "👤 *Od:* " . strip_tags($name) . "\n";
$message .= "❓ *Otázka:* " . strip_tags($question);

$url = "https://api.telegram.org/bot$botToken/sendMessage";
$data = [
    'chat_id' => $chatId,
    'text' => $message,
    'parse_mode' => 'Markdown'
];

// 5. Send to Telegram using cURL
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false); // Quick fix for local dev; in prod use certs
$result = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

// 6. Return Response to Frontend
if ($httpCode == 200) {
    echo json_encode(["status" => "success"]);
} else {
    http_response_code(500);
    echo json_encode(["status" => "error", "debug" => $result]);
}

?>
