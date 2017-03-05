//    _________                          _________                        
//   /   _____/__ ________   ___________/   _____/_  _  _______     ____  
//   \_____  \|  |  \____ \_/ __ \_  __ \_____  \\ \/ \/ /\__  \   / ___\ 
//   /        \  |  /  |_> >  ___/|  | \/        \\     /  / __ \_/ /_/  >
//  /_______  /____/|   __/ \___  >__| /_______  / \/\_/  (____  /\___  / 
//          \/      |__|        \/             \/              \//_____/  
//
// This file is a part of the SuperSwag projet.
// Copyleft 2017 - evolya.fr

#include <Wire.h>

// -- Configuration des pins

#define PIN_LED_R 2       // Pin LED couleur ROUGE
#define PIN_LED_Y 3       // Pin LED couleur VERT
#define PIN_PWR_RPI 5     // Pin allumage alimentation Raspberry Pi (5V)
#define PIN_PWR_SCREEN 6  // Pin allumage alimentation Ecran (12V)
#define PIN_SWITCH 12     // Pin du switch On/Off
#define PIN_POT A0        // Pin du potentiomètre du volume sonore

// -- Configuration des délais (en ms)

#define TTL_STARTING 30000
#define TTL_SHUTDOWN 30000
#define LED_BLINK_DELAY 500
#define SHUTDOWN_SAFETY_DELAY 10000
#define RPI_ALIVE_TTL 2000

// -- Configurations avancées

#define SERIAL_BAUDRATE 9600    // Taux de transmission de l'arduino pour la liaison série
#define SLAVE_ADDRESS 0x04      // Adresse I2C de l'arduino
#define SHUTDOWN_ON_ERROR false // Couper l'alimentation de la Rpi si le démarrage échoue

// -- Etats possibles du système

#define STATE_OFF 0       // Le système est arrêté
#define STATE_STARTING 1  // Le système est en cours de démarrage
#define STATE_STARTED 2   // Le système est démarré et en fonctionnement
#define STATE_SHUTDOWN 3  // Le système est en cours d'arrêt

// Enregistre l'état actuel du système
int generalState = STATE_OFF;

// Utilisés pour gérer l'état de la LED clignotante
bool ledState = true;
long ledTimer = 0;

// Enregistre le moment où à commencé le lancement ou l'arrêt du système
long startStopTime = 0;

// Volume (de 0 à 100)
int volume = 0;

// Etat du bouton On/Off : ouvert ou fermé
bool switchState = false;

// Timestamp du moment où vérifier l'état de la RPI (par gpio)
long rpiCheckTime = 1;

// Valeur du pin PIN_RUNNING (temporisé pour éviter le changement trop rapide d'état lors du lancement de la rpi)
int rpiPinValue = 0;

// Conserve l'état de lancement du script python sur le raspberry
bool rpiState = false;

// Tempon d'écriture I2C vers le raspberry
volatile byte e_keys;

// Timestamp de la dernière requête de la RPI
long rpiLastRequest = 0;

// Indique si la raspberry est connectée en I2C
bool rpiConnected = false;

// Quand le maitre (raspberry) demande quelque chose à l'esclave (arduino)
void i2c_requests()
{
  //Serial.println("I2C request");
  rpiLastRequest = millis();
  if (!rpiConnected) {
    Serial.println("Raspberry was connected!");
    rpiConnected = true;
    if (generalState == STATE_STARTING) {
      generalState = STATE_STARTED;
      Serial.println("New state: STARTED");
      digitalWrite(PIN_LED_R, LOW);
      digitalWrite(PIN_LED_Y, HIGH);
    }
  }
  if (e_keys == 0) return;
  Wire.write(e_keys);
  Serial.print("I2C sent: ");
  Serial.println((int)e_keys);
  e_keys = 0;
}

void i2c_sendData(byte value)
{
  // Rien ne peut empêcher le signal de shutdown
  if (e_keys != 201)
    e_keys = value;
}

void setup()
{
  
  Serial.begin(SERIAL_BAUDRATE);
  Serial.println("Init...");

  pinMode(PIN_SWITCH, INPUT);
  digitalWrite(PIN_SWITCH, HIGH);
  
  pinMode(PIN_LED_R, OUTPUT);
  pinMode(PIN_LED_Y, OUTPUT);
  digitalWrite(PIN_LED_R, LOW);
  digitalWrite(PIN_LED_Y, LOW);
  
  pinMode(PIN_PWR_RPI, OUTPUT);
  pinMode(PIN_PWR_SCREEN, OUTPUT);
  setPowerEnabled(false);

  pinMode(PIN_POT, INPUT);

  // Initialisation I2C
  Wire.begin(SLAVE_ADDRESS);
  Wire.onRequest(i2c_requests);

  Serial.println("New state: OFF");
  Serial.println("Ready!");
}

void startblink(int pinColor)
{
  digitalWrite(PIN_LED_R, pinColor == PIN_LED_R ? HIGH : LOW);
  digitalWrite(PIN_LED_Y, pinColor == PIN_LED_Y ? HIGH : LOW);
  ledState = true;
  ledTimer = startStopTime = millis();
}

void ledblink(int colorPin)
{
  ledState = !ledState;
  digitalWrite(colorPin, ledState ? HIGH : LOW);
  ledTimer = millis();
}

void sendShutdownSignal()
{
  i2c_sendData(201);
}

void setPowerEnabled(bool enabled)
{
  Serial.print("Set power: ");
  Serial.println(enabled ? "ON" : "OFF");
  digitalWrite(PIN_PWR_RPI, enabled ? HIGH : LOW);
  digitalWrite(PIN_PWR_SCREEN, enabled ? HIGH : LOW);
}

void setStateStarting()
{
  // Changement d'état
  startStopTime = millis();
  generalState = STATE_STARTING;
  Serial.println("New state: STARTING");
  // On commence un clignotement vert
  startblink(PIN_LED_Y);
  // Allumage de l'alimentation des autres composants
  setPowerEnabled(true);
}

void setStateShutdown() {
  // Changement d'état
  generalState = STATE_SHUTDOWN;
  Serial.println("New state: SHUTDOWN");
  // On envoie l'interruption au Rpi
  sendShutdownSignal();
  // On commence un clignotement rouge
  startblink(PIN_LED_R);
}

void handleStarting()
{
  // Détection de l'expiration du délais maximum de lancement de la Rpi
  if (millis() - startStopTime > TTL_STARTING) {
    Serial.println("Error: maximum time to start is reached !");
    generalState = STATE_OFF;
    Serial.println("New state: OFF (with failure)");
    digitalWrite(PIN_LED_R, HIGH);
    digitalWrite(PIN_LED_Y, LOW);
    // On coupe l'alimentation
    if (SHUTDOWN_ON_ERROR) setPowerEnabled(false);
    return;
  }
  // Sinon : clignotement de LED lors du démarrage
  if (millis() - ledTimer > LED_BLINK_DELAY) {
    ledblink(PIN_LED_Y);
  }
}

void handleShutdown()
{
  // Détection de l'expiration du délais maximum d'arrêt de la Rpi
  if (millis() - startStopTime > TTL_SHUTDOWN) {
    Serial.println("Error: maximum time to shutdown is reached !");
    generalState = STATE_OFF;
    Serial.println("New state: OFF (with failure)");
    digitalWrite(PIN_LED_R, LOW);
    digitalWrite(PIN_LED_Y, LOW);
    // On coupe l'alimentation
    setPowerEnabled(false);
    return;
  }
  // Sinon : clignotement de LED lors de l'arrêt
  if (millis() - ledTimer > LED_BLINK_DELAY) {
    ledblink(PIN_LED_R);
  }
}

void setStarted(bool onOff) {
  Serial.print("Consigne bouton : ");
  Serial.println(onOff ? "ON" : "OFF");
  // Et on modifie l'état
  if (onOff && generalState == STATE_OFF)       setStateStarting();
  if (!onOff && generalState == STATE_STARTED)  setStateShutdown();
}

void loop()
{

  ////// 
  //////  GESTION DU BOUTON ON/OFF
  //////
  int btn = digitalRead(PIN_SWITCH);
  // Changement d'état du bouton ON/OFF
  if (btn != switchState) {
    if (btn == 1 && generalState == STATE_OFF) {
      setStarted(true);
      switchState = btn;
    }
    else if (btn == 0 && generalState == STATE_STARTED) {
      setStarted(false);
      switchState = btn;
    }
  }
  // Gestion des changements d'états
  if (generalState == STATE_STARTING) handleStarting();
  if (generalState == STATE_SHUTDOWN) handleShutdown();

  ////// 
  //////  GESTION DE LA MOLETTE DU VOLUME
  //////
  if (generalState == STATE_STARTED) {
    int snd = analogRead(PIN_POT);
    int delta = abs(volume - snd);
    if (delta > 25) {
      int cl = (int)((float)snd / 1024.0 * 99.0) + 1;
      Serial.print("Volume : ");
      Serial.print(cl);
      Serial.println("%");
      volume = snd;
      i2c_sendData(cl);
    }
  }

  ////// 
  //////  GESTION DES ENTREES SERIE
  //////
  if (Serial.available()) {
    String data = Serial.readString();
    if (data == "help") {
      Serial.println("Commands :");
      Serial.println("  on | off    Change current consigne");
      Serial.println("  test-i2c    Sent 111 to the raspberry pi");
      Serial.println("  shutdown    Shutdown the raspberry pi");
      Serial.println("  reboot      Reboot the raspberry pi");
    }
    else if (data == "on") {
      setStarted(true);
    }
    else if (data == "off") {
      setStarted(false);
    }
    else if (data == "test-i2c") {
      i2c_sendData(111);
    }
    else if (data == "shutdown") {
      sendShutdownSignal();
    }
    else if (data == "reboot") {
      i2c_sendData(202);
    }
    else {
      Serial.println("Invalid commande. Type help to list available commands.");
    }
  }

  if (rpiConnected && millis() - rpiLastRequest >= RPI_ALIVE_TTL) {
    Serial.println("Raspberry was disconnected...");
    rpiConnected = false;
    if (generalState == STATE_SHUTDOWN) {
      digitalWrite(PIN_LED_R, HIGH);
      digitalWrite(PIN_LED_Y, LOW);
      // On attend encore un petit peu par sécurité
      delay(SHUTDOWN_SAFETY_DELAY);
      generalState = STATE_OFF;
      Serial.println("New state: OFF");
      digitalWrite(PIN_LED_R, LOW);
      digitalWrite(PIN_LED_Y, LOW);
      // On coupe l'alimentation
      setPowerEnabled(false);
    }
  }

}
