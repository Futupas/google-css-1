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
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Secure Service</title>

<link rel="stylesheet" href="styles.css" />
</head>

<body>
<div class="container">
    <h1>Secure Online Service</h1>
    <p class="big red" style="text-align:center">
        <b>WARNING: Do not enter real login credentials or real payment card details.</b>
        This service is for testing and demonstration purposes only.
        <b>Use mock or dummy data only.</b>
    </p>
    <p class="big red" style="text-align:center">
        <b>UPOZORNĚNÍ: Nezadávejte skutečné přihlašovací údaje ani reálné údaje platební karty.</b>
        Tato služba slouží pouze k testovacím a demonstračním účelům.
        <b>Používejte pouze testovací nebo fiktivní data.</b>
    </p>

    <div class="grid">

        <!-- LOGIN FORM -->
        <div class="card">
            <h2>Account Login</h2>
            <p class="small">Access your personal dashboard securely.</p>

            <form method="post">
                <label>Login</label>
                <input type="text" name="login" required />

                <label>Password</label>
                <input type="password" name="password" required />

                <button type="submit">Log In</button>
            </form>

            <?php if ($loginSuccess): ?>
                <div class="success">
                    You have successfully logged in.
                </div>
            <?php endif; ?>
        </div>

        <!-- PAYMENT FORM -->
        <div class="card">
            <h2>Payment</h2>
            <p class="small">Enter your credit card details to complete payment.</p>

            <form method="post">
                <label>Cardholder Name</label>
                <input type="text" name="name" required />

                <label>Card Number</label>
                <input type="text" name="card" inputmode="numeric" placeholder="1234 5678 9012 3456" required />

                <label>Expiry Date</label>
                <input type="text" name="expiry" placeholder="MM/YY" required />

                <label>CVV</label>
                <input type="password" name="cvv" inputmode="numeric" required />

                <button type="submit" name="payment">Pay Now</button>
            </form>

            <?php if ($paymentSuccess): ?>
                <div class="success">
                    Payment successful. Thank you!
                </div>
            <?php endif; ?>
        </div>

    </div>
</div>
</body>
</html>
