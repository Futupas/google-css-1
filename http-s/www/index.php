<?php
session_start();
$file = 'chat.txt';

if(isset($_POST['message'])) {
    $msg = htmlspecialchars($_POST['message']);
    file_put_contents($file, date('[H:i] ') . $msg . PHP_EOL, FILE_APPEND);
}

$messages = file_exists($file) ? file($file) : [];
?>

<h2>Simple Chat</h2>
<div style="height:300px;overflow:auto;border:1px solid #000;padding:5px;">
<?php foreach($messages as $m) echo htmlspecialchars($m) . "<br>"; ?>
</div>

<form method="post">
    <input name="message" style="width:80%;">
    <button>Send</button>
</form>
