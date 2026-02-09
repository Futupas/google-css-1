<?php
$loginSuccess = false;
$paymentSuccess = false;

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    if (isset($_POST["login"])) {
        $loginSuccess = true;
    }
    if (isset($_POST["payment"])) {
        $paymentSuccess = true;
    }
}
?>
<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Zabezpečená služba</title>

<link rel="stylesheet" href="styles.css" />
</head>

<body>
<div class="container">
    <h1>Zabezpečená online služba</h1>
    <p class="big red" style="text-align:center">
        <b>UPOZORNĚNÍ: Nezadávejte skutečné přihlašovací údaje ani reálné údaje platební karty.</b>
        Tato služba slouží pouze k testovacím a demonstračním účelům.
        <b>Používejte pouze testovací nebo fiktivní data.</b>
    </p>

    <div class="grid">

        <!-- PŘIHLAŠOVACÍ FORMULÁŘ -->
        <div class="card">
            <h2>Přihlášení k účtu</h2>
            <p class="small">Bezpečný přístup k vašemu osobnímu panelu.</p>

            <form method="post">
                <label>Přihlašovací jméno</label>
                <input type="text" name="login" required />

                <label>Heslo</label>
                <input type="password" name="password" required />

                <button type="submit">Přihlásit se</button>
            </form>

            <?php if ($loginSuccess): ?>
                <div class="success">
                    Přihlášení proběhlo úspěšně
                </div>
            <?php endif; ?>
        </div>

        <!-- PLATEBNÍ FORMULÁŘ -->
        <div class="card">
            <h2>Platba</h2>
            <p class="small">Zadejte údaje o platební kartě pro dokončení platby.</p>

            <form method="post">
                <label>Jméno držitele karty</label>
                <input type="text" name="name" />

                <label>Číslo karty</label>
                <input type="text" name="card" inputmode="numeric" placeholder="1234 5678 9012 3456" required />

                <label>Datum platnosti</label>
                <input type="text" name="expiry" placeholder="MM/RR" required />

                <label>CVV</label>
                <input type="password" name="cvv" inputmode="numeric" required />

                <button type="submit">Zaplatit</button>
            </form>

            <?php if ($paymentSuccess): ?>
                <div class="success">
                    Platba byla úspěšná. Děkujeme!
                </div>
            <?php endif; ?>
        </div>

    </div>
</div>
</body>
</html>
