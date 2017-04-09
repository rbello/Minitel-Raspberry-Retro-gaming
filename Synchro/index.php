<?php

#    _________                          _________                        
#   /   _____/__ ________   ___________/   _____/_  _  _______     ____  
#   \_____  \|  |  \____ \_/ __ \_  __ \_____  \\ \/ \/ /\__  \   / ___\ 
#   /        \  |  /  |_> >  ___/|  | \/        \\     /  / __ \_/ /_/  >
#  /_______  /____/|   __/ \___  >__| /_______  / \/\_/  (____  /\___  / 
#          \/      |__|        \/             \/              \//_____/  
#
# This file is a part of the SuperSwag projet.
# Copyleft 2017 - evolya.fr

// Secret key
$otp_secret = 'LSX2I5BLGSXA4T77';

// n*30 sec clock tolerance
$otp_tolerance = 2;

// Timezone
$current_timezone = 'Europe/Paris';

############ END OF CONFIGURATION ############

if (!function_exists('http_response_code')) {
	function http_response_code($code = NULL) {
		if ($code !== NULL) {
			switch ($code) {
				case 100: $text = 'Continue'; break;
				case 101: $text = 'Switching Protocols'; break;
				case 200: $text = 'OK'; break;
				case 201: $text = 'Created'; break;
				case 202: $text = 'Accepted'; break;
				case 203: $text = 'Non-Authoritative Information'; break;
				case 204: $text = 'No Content'; break;
				case 205: $text = 'Reset Content'; break;
				case 206: $text = 'Partial Content'; break;
				case 300: $text = 'Multiple Choices'; break;
				case 301: $text = 'Moved Permanently'; break;
				case 302: $text = 'Moved Temporarily'; break;
				case 303: $text = 'See Other'; break;
				case 304: $text = 'Not Modified'; break;
				case 305: $text = 'Use Proxy'; break;
				case 400: $text = 'Bad Request'; break;
				case 401: $text = 'Unauthorized'; break;
				case 402: $text = 'Payment Required'; break;
				case 403: $text = 'Forbidden'; break;
				case 404: $text = 'Not Found'; break;
				case 405: $text = 'Method Not Allowed'; break;
				case 406: $text = 'Not Acceptable'; break;
				case 407: $text = 'Proxy Authentication Required'; break;
				case 408: $text = 'Request Time-out'; break;
				case 409: $text = 'Conflict'; break;
				case 410: $text = 'Gone'; break;
				case 411: $text = 'Length Required'; break;
				case 412: $text = 'Precondition Failed'; break;
				case 413: $text = 'Request Entity Too Large'; break;
				case 414: $text = 'Request-URI Too Large'; break;
				case 415: $text = 'Unsupported Media Type'; break;
				case 500: $text = 'Internal Server Error'; break;
				case 501: $text = 'Not Implemented'; break;
				case 502: $text = 'Bad Gateway'; break;
				case 503: $text = 'Service Unavailable'; break;
				case 504: $text = 'Gateway Time-out'; break;
				case 505: $text = 'HTTP Version not supported'; break;
				default:
					exit('Unknown http status code "' . htmlentities($code) . '"');
				break;
			}
			$protocol = (isset($_SERVER['SERVER_PROTOCOL']) ? $_SERVER['SERVER_PROTOCOL'] : 'HTTP/1.0');
			header($protocol . ' ' . $code . ' ' . $text);
			$GLOBALS['http_response_code'] = $code;
		} else {
			$code = (isset($GLOBALS['http_response_code']) ? $GLOBALS['http_response_code'] : 200);
		}
		return $code;
	}
}

function error($code, $message) {
	http_response_code($code);
	echo $message;
	exit();
}

date_default_timezone_set($current_timezone);

if ($_SERVER['REQUEST_METHOD'] == 'GET') {
	if (file_exists('./.cache.php')) {
		$cache = include './.cache.php';
		echo filemtime('./.cache.php');
		foreach ($cache as $game => $data) {
			$update = array_pop($data['updates']);
			echo "\n{$update['hash']} {$update['mtime']} {$data['emulator']} {$game}";
		}
	}
	else echo time();
	exit();
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

	// Check arguments
	if (!array_key_exists('key', $_POST))
		error(401, 'Missing request parameter: authentication password (key)');
	if (!array_key_exists('console', $_POST))
		error(400, 'Missing request parameter: console name (console)');
	if (!array_key_exists('hash', $_POST))
		error(400, 'Missing request parameter: file checksum (hash)');
	if (!array_key_exists('mtime', $_POST))
		error(400, 'Missing request parameter: file modification time (mtime)');
	if (!array_key_exists('plateforme', $_POST))
		error(400, 'Missing request parameter: emulator name (plateforme)');

	// Error level
	error_reporting(E_ALL);

	// Import OTP library
	require_once 'GoogleAuthenticator.php';
	$ga = new PHPGangsta_GoogleAuthenticator();
	//$otp_secret = $ga->createSecret();
	//$otp = $ga->getCode($otp_secret);

	// Check OTP
	if (!$ga->verifyCode($otp_secret, $_POST['key'], $otp_tolerance))
		error(403, 'Forbidden: invalid authentication password');
	
	// Check uploaded file
	if (sizeof($_FILES) !== 1)
		error(400, 'File upload error: no file uploaded');
	
	// Extract game data
	$game = array_shift($_FILES);
	
	// Check upload
	if ($game['error'] !== UPLOAD_ERR_OK)
		error(500, 'File upload error: ' . $game['error']);
	
	// Load cache
	$cache = array();
	if (file_exists('./.cache.php')) $cache = include './.cache.php';
	
	// Fix hash
	$_POST['hash'] = preg_replace("/[^A-Za-z0-9 ]/", '', $_POST['hash']);
	
	// Create store directory
	if (!is_dir('./saves/')) mkdir('./saves/');
	
	//echo "Received update from " . $_POST['console'] . " game " . $game['name'] . " hash " . $_POST['hash'];

	// Try to move uploaded file to store directory
	if (!move_uploaded_file($game['tmp_name'], './saves/' . $_POST['hash']))
		error(500, 'File upload error: unable to move uploaded file');

	// Create save entry
	$update = true;
	if (!array_key_exists($game['name'], $cache)) {
		$cache[$game['name']] = array(
			'emulator' => $_POST['plateforme'],
			'updates' => array()
		);
		$update = false;
	}
	
	// Add update entry
	$cache[$game['name']]['updates'][] = array(
			'from'  => $_POST['console'],
			'hash'  => $_POST['hash'],
			'mtime' => intval($_POST['mtime'])
		);
	
	// Save cache
	file_put_contents('./.cache.php', '<?php return ' . var_export($cache, true) . ';');

	http_response_code($update ? 200 : 201);
	echo 'OK';

}
