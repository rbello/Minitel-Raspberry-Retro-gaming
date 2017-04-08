<?php

$secret = 'LSX2I5BLGSXA4T77';

$tolerance = 1; // n*30sec clock tolerance

date_default_timezone_set('Europe/Paris');

if ($_SERVER['REQUEST_METHOD'] == 'GET') {
	if (file_exists('.cache')) {
		include '.cache';
	}
	else echo time();
	exit();
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
	
	if (!array_key_exists('key', $_POST))
		exit('No key given');

	error_reporting(E_ALL);

	require_once 'GoogleAuthenticator.php';
	$ga = new PHPGangsta_GoogleAuthenticator();
	//$secret = $ga->createSecret();
	//$otp = $ga->getCode($secret);

	if (!$ga->verifyCode($secret, $_POST['key'], $tolerance)) {
		exit('Invalid key');
	}
	
	if (!array_key_exists('console', $_POST))
		exit('No console name given');
	
	// $_POST['hash']
	// $_POST['mtime']

	$game = @array_shift($_FILES);
	
	if ($game['error'] !== 0)
		exit('File upload error: ' . $game['error']);
	
	echo "Received update from " . $_POST['console'] . " game " . $game['name'] . " hash " . $_POST['hash'];
}
