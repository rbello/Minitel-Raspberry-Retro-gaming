<?php

error_reporting(E_ALL);

date_default_timezone_set('Europe/Paris');

require_once 'GoogleAuthenticator.php';

$ga = new PHPGangsta_GoogleAuthenticator();

//$secret = $ga->createSecret();
$secret = "LSX2I5BLGSXA4T77";

$oneCode = $ga->getCode($secret);

echo $oneCode . "\r\n<br>";

$checkResult = $ga->verifyCode($secret, $oneCode, 1); // n*30sec clock tolerance
if ($checkResult) {
    echo 'OK';
} else {
    echo 'FAILED';
}