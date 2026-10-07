<!DOCTYPE html>
<html lang="nl">

<?php
require 'services/get_user_id.php';

$jwt = $_SESSION['user_token'];
$user_id = getUserID($jwt);
// echo $user_id;
?>

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bewerk Account</title>
    <link rel="stylesheet" href="styles/edit_user.css">
</head>

<body>
    <?php include_once './components/nav.php'; ?>

    <!-- Main content -->
    <div class="main">
        <h1>Bewerk Account Gegevens</h1>
            <form id="update_form" onsubmit="return editUser(<?php echo $user_id; ?>)" method="PUT"><!-- action="view" -->
            <div class="form-row">
                <label for="email">Email</label>
                <input id="email" type="text" name="email"><br>
            </div>
            <div class="form-row">
                <label for="password">Wachtwoord</label>
                <input id="password" type="text" name="password"><br>
            </div>
            <div class="form-row">
                <label for="adress">Adres</label>
                <input id="adress" type="text" name="adress"><br>
            </div>
            <div class="form-row">
                <label for="zipcode">Postcode</label>
                <input id="zipcode" type="text" name="zipcode"><br>
            </div>
            <div class="form-row">
                <label for="country">Land</label>
                <input id="country" type="text" name="country"><br>
            </div>
            <div class="form-row">
                <label for="firstName">Voornaam</label>
                <input id="firstName" type="text" name="firstName"><br>
            </div>
            <div class="form-row">
                <label for="nameParticle">Tussenvoegsel</label>
                <input id="nameParticle" type="text" name="nameParticle"><br>
            </div>
            <div class="form-row">
                <label for="lastName">Achternaam</label>
                <input id="lastName" type="text" name="lastName"><br>
            </div>
            <div class="form-row">
                <label for="phonenumber">Telefoon nummer</label>
                <input id="phonenumber" type="text" name="phonenumber"><br>
            </div>
            <div class="form-row">
                <label for="bankaccount">Bank account</label>
                <input id="bankaccount" type="text" name="bankaccount"><br>
            </div>
            <div class="form-row">
                <!--<label for="update_info">Update gegevens</label>-->
                <input id="update_info" type="submit" name="update_info"><br>
            </div>
            <div class="form-row">
                <input id="userID" type="hidden" name="userID">
            </div>
        </form>
    </div>
</body>

<script src="services/edit_user.js"></script>

</html>