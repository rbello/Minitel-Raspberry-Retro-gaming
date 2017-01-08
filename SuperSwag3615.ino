#include <Wire.h>

// -- Configuration des pins

#define PIN_LED_R 11      // Pin LED couleur ROUGE
#define PIN_LED_Y 10      // Pin LED couleur VERT
#define PIN_PWR_RPI 3     // Pin allumage alimentation Raspberry Pi (5V)
#define PIN_PWR_SCREEN 4  // Pin allumage alimentation Ecran (12V)
#define PIN_SWITCH 8      // Pin du switch On/Off
#define PIN_RUNNING 2     // Pin permettant de récupérer l'état d'alimentation de la Rpi
#define PIN_POT A3        // Pin du potentiomètre du volume sonore

// -- Configuration des délais (en ms)

#define TTL_STARTING 10000
#define TTL_SHUTDOWN 10000
#define LED_BLINK_DELAY 500

// -- Configurations avancées

#define SERIAL_BAUDRATE 9600
#define SLAVE_ADDRESS 0x04

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

// Etat de la consigne On/Off : allumé ou éteint
bool onOff = false;

// Conserve l'état de lancement du script python sur le raspberry
// Arrive par le pin PIN_RUNNING
int rpiRunning = 0;

// Tempon d'écriture I2C vers le raspberry
volatile byte e_keys;

// Quand le maitre (raspberry) demande quelque chose à l'esclave (arduino)
void i2c_requests()
{
  if (e_keys == 0) return;
  Wire.write(e_keys);
  //Serial.print("Sent: ");
  //Serial.println((int)e_keys);
  e_keys = 0;
}

void i2c_sendData(byte value)
{
  // Rien ne peut empêcher le signal de shutdown
  if (e_keys != 200)
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

  pinMode(PIN_RUNNING, INPUT);

  pinMode(PIN_POT, INPUT);

  // Initialisation I2C
  Wire.begin(SLAVE_ADDRESS);
  Wire.onRequest(i2c_requests);

  Serial.println("Ready!");
  Serial.println("New state: OFF");
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
  i2c_sendData(200);
}

void setPowerEnabled(bool enabled)
{
  digitalWrite(PIN_PWR_RPI, enabled ? HIGH : LOW);
  digitalWrite(PIN_PWR_SCREEN, enabled ? HIGH : LOW);
}

void setStateStarting()
{
  // Changement d'état
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
  // Détection du signal provenant de la Raspberry Pi pour indiquer son bon démarrage
  if (millis() - startStopTime > 4000 - 200) {
    // TODO Changer la condition du test bien entendu ;-)
    generalState = STATE_STARTED;
    Serial.println("New state: STARTED");
    digitalWrite(PIN_LED_R, LOW);
    digitalWrite(PIN_LED_Y, HIGH);
    return;
  }
  // Détection de l'expiration du délais maximum de lancement de la Rpi
  if (millis() - startStopTime > TTL_STARTING) {
    Serial.println("Error: maximum time to start is reached !");
    generalState = STATE_OFF;
    Serial.println("New state: OFF (with failure)");
    digitalWrite(PIN_LED_R, HIGH);
    digitalWrite(PIN_LED_Y, LOW);
    // On coupe l'alimentation
    setPowerEnabled(false);
    return;
  }
  // Sinon : clignotement de LED lors du démarrage
  if (millis() - ledTimer > LED_BLINK_DELAY) {
    ledblink(PIN_LED_Y);
  }
}

void handleShutdown()
{
  // Détection du signal provenant de la Raspberry Pi pour indiquer son arrêt complet
  if (millis() - startStopTime > TTL_SHUTDOWN - 200) {
    // TODO Changer la condition du test bien entendu ;-)
    generalState = STATE_OFF;
    Serial.println("New state: OFF");
    digitalWrite(PIN_LED_R, LOW);
    digitalWrite(PIN_LED_Y, LOW);
    // On coupe l'alimentation
    setPowerEnabled(false);
    return;
  }
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
  Serial.print("Consigne : ");
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
  // Changement d'état du bouton ON/OFF : fonctionne uniquement au repos (Off ou Started) pas les états intermédiaires
  if (btn != switchState && (generalState == STATE_OFF || generalState == STATE_STARTED)) {
    // Quand le bouton est enfoncé
    if (btn == 1) {
      // On inverse la consigne
      onOff = !onOff;
      setStarted(onOff);
    }
    switchState = btn;
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
      Serial.println("  test-i2c    Sent a 111 to the raspberry");
    }
    else if (data == "on") {
      setStarted(true);
    }
    else if (data == "off") {
      setStarted(false);
    }
    else if (data == "test-i2c") {
      Serial.println("Send '7' to I2C connection");
      i2c_sendData(0x07);
    }
    else {
      Serial.println("Invalid commande. Type help to list available commands.");
    }
  }

  ////// 
  //////  GESTION RECEPTION DE l'ETAT DE LANCEMENT DU SCRIPT PYTHON SUR LE RPI
  //////
  int val = digitalRead(PIN_RUNNING);
  if (val != rpiRunning) {
    Serial.print("Rpi running state: ");
    Serial.println(rpiRunning);
    rpiRunning = val;
  }
  
}
