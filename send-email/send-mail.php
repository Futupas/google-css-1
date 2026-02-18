<?php

if ($_SERVER['REQUEST_METHOD'] !== 'POST') { http_response_code(405); die(); }

require __DIR__ . '/vendor/autoload.php';

use PHPMailer\PHPMailer\PHPMailer;
use Dotenv\Dotenv;

header('Content-Type: application/json');

// 1. Načtení JSON těla požadavku
$json = file_get_contents('php://input');
$data = json_decode($json, true);

if (!$data) {
    echo json_encode(["status" => "error", "message" => "Neplatná data"]);
    exit;
}

// 2. Načtení .env
$dotenv = Dotenv::createImmutable(__DIR__ . '/../');
$dotenv->load();

$mail = new PHPMailer(true);
try {
    $mail->isSMTP();
    $mail->Host       = $_ENV['SMTP_HOST'];
    $mail->SMTPAuth   = ($_ENV['SMTP_AUTH'] === 'true');
    $mail->Username   = $_ENV['SMTP_USER'];
    $mail->Password   = $_ENV['SMTP_PASS'];
    $mail->SMTPSecure = $_ENV['SMTP_SECURE'];
    $mail->Port       = $_ENV['SMTP_PORT'];
    $mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS; 
    $mail->CharSet    = 'UTF-8';
    $mail->SMTPOptions = array(
        'ssl' => array(
            'verify_peer' => false,
            'verify_peer_name' => false,
            'allow_self_signed' => true
        )
    );
    $mail->SMTPDebug = 2; // Vypíše detailní logování chyb

    $mail->setFrom($data['emailFrom'], $data['emailFromName']);
    $mail->addAddress($data['emailTo']);

    $mail->isHTML($data['isHtml']);
    $mail->Subject = $data['emailSubject'];

    // Pokud je isHtml true, zabalíme zprávu do jednoduchého HTML
    $mail->Body = htmlspecialchars($data['messageText']);

    $mail->send();
    echo json_encode(["status" => "success", "message" => "Email byl úspěšně odeslán!"]);

} catch (Exception $e) {
    echo json_encode(["status" => "error", "message" => "Chyba: {$mail->ErrorInfo}"]);
}
