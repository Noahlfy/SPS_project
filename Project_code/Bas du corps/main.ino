#include <Wire.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <Adafruit_BNO055.h>
#include <Adafruit_Sensor.h>

// Initialisation du premier BNO055 pour la jambe droite (adresse 0x28)
Adafruit_BNO055 bno1 = Adafruit_BNO055(55, 0x28);  

// Initialisation du deuxième BNO055 pour la jambe gauche (adresse 0x29)
Adafruit_BNO055 bno2 = Adafruit_BNO055(56, 0x29);

// Variables to store sensor data
float accel_X1, accel_Y1, accel_Z1;
float accel_X2, accel_Y2, accel_Z2;

// Register addresses for the BNO055
#define LIA_DATA_X_LSB 0x28
#define LIA_DATA_X_MSB 0x29
#define LIA_DATA_Y_LSB 0x2A
#define LIA_DATA_Y_MSB 0x2B
#define LIA_DATA_Z_LSB 0x2C
#define LIA_DATA_Z_MSB 0x2D

unsigned long previousMillis = 0;    // Pour la temporisation
const long interval = 10000;         // Intervalle d'affichage de la calibration (10 secondes)

// Wi-Fi credentials
const char* ssid = "iPhone Noah";
const char* password = "polekeleke";

// Set up the broker
const char* mqtt_server = "172.20.10.10";

WiFiClient espClient;
PubSubClient client(espClient);

// Initialisation du capteur BNO055
Adafruit_BNO055 bno = Adafruit_BNO055(55);

void setup_wifi() {
  Serial.println("Connexion au Wi-Fi...");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connexion en cours...");
  }

  Serial.println("Connecté au Wi-Fi");
  Serial.print("Adresse IP : ");
  Serial.println(WiFi.localIP());
}

void setup() {
  // Initialiser la communication série
  Serial.begin(115200);
  delay(100);

  // Connexion Wi-Fi
  setup_wifi();
  client.setServer(mqtt_server, 1883);

  // Initialiser le premier BNO055 (jambe droite)
  if (!bno1.begin()) {
    Serial.println("Erreur de communication avec le capteur BNO055 de la jambe droite (0X28)");
  } else {
    Serial.println("Capteur BNO055 (0X28 - jambe droite) initialisé correctement");
  }
  
  // Initialiser le deuxième BNO055 (jambe gauche)
  if (!bno2.begin()) {
    Serial.println("Erreur de communication avec le capteur BNO055 de la jambe gauche (0X29)");
  } else {
    Serial.println("Capteur BNO055 (0X29 - jambe gauche) initialisé correctement");
  }

  // Temps de stabilisation du capteur BNO055
  delay(1000);

  // Calibration et configuration des deux capteurs
  bno1.setExtCrystalUse(true);
  bno2.setExtCrystalUse(true);

  // Vérification de l'état de calibration
  checkCalibrationStatus(bno1);
  checkCalibrationStatus(bno2);
}

void checkCalibrationStatus(Adafruit_BNO055 &bno) {
  uint8_t system, gyro, accel, mag;
  bno.getCalibration(&system, &gyro, &accel, &mag);

  Serial.print("Calib Sys: "); Serial.print(system);
  Serial.print(", Gyro: "); Serial.print(gyro);
  Serial.print(", Accel: "); Serial.print(accel);
  Serial.print(", Mag: "); Serial.println(mag);

  if (system < 3 || gyro < 3 || accel < 3 || mag < 3) {
    Serial.println("Le capteur n'est pas entièrement calibré.");
  } else {
    Serial.println("Le capteur est entièrement calibré.");
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("espClient")) {
      Serial.println("connected");
      client.subscribe("esp32/output");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());  // Imprimer le code d'erreur de la connexion MQTT
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

// Fonction pour lire les données d'accélération via I2C pour un capteur donné
void readAcceleration(uint8_t bno_address, float &accel_X, float &accel_Y, float &accel_Z) {
  Wire.beginTransmission(bno_address);
  Wire.write(LIA_DATA_X_LSB);
  Wire.endTransmission();
  Wire.requestFrom(bno_address, 6);

  if (Wire.available() == 6) {
    // Lire les données brutes de chaque axe
    int16_t rawX = (Wire.read() | (Wire.read() << 8));
    int16_t rawY = (Wire.read() | (Wire.read() << 8));
    int16_t rawZ = (Wire.read() | (Wire.read() << 8));

    // Conversion des données brutes en m/s²
    accel_X = rawX / 100.0;
    accel_Y = rawY / 100.0;
    accel_Z = rawZ / 100.0;
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long currentMillis = millis();

  // Vérification de l'état de calibration toutes les 10 secondes
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    // Vérifier l'état de calibration seulement à intervalles réguliers
    checkCalibrationStatus(bno1);  
    checkCalibrationStatus(bno2);  
  }

  // Lire les données d'accélération pour le premier BNO055 (jambe droite, 0x28)
  readAcceleration(0x28, accel_X1, accel_Y1, accel_Z1);

  // Lire les quaternions du premier BNO055 (0x28)
  imu::Quaternion quat1 = bno1.getQuat();
  float quat_W1 = quat1.w();
  float quat_X1 = quat1.x();
  float quat_Y1 = quat1.y();
  float quat_Z1 = quat1.z();

  // Lire les données d'accélération pour le deuxième BNO055 (jambe gauche, 0x29)
  readAcceleration(0x29, accel_X2, accel_Y2, accel_Z2);

  // Lire les quaternions du deuxième BNO055 (0x29)
  imu::Quaternion quat2 = bno2.getQuat();
  float quat_W2 = quat2.w();
  float quat_X2 = quat2.x();
  float quat_Y2 = quat2.y();
  float quat_Z2 = quat2.z();

  // Afficher les données sur le moniteur série pour le capteur 1 (jambe droite)
  Serial.println("=== Capteur Jambe Droite (0x28) ===");
  Serial.print("Acceleration X1 (m/s²): "); Serial.println(accel_X1);
  Serial.print("Acceleration Y1 (m/s²): "); Serial.println(accel_Y1);
  Serial.print("Acceleration Z1 (m/s²): "); Serial.println(accel_Z1);
  Serial.print("Quaternion W1: "); Serial.println(quat_W1, 4);
  Serial.print("Quaternion X1: "); Serial.println(quat_X1, 4);
  Serial.print("Quaternion Y1: "); Serial.println(quat_Y1, 4);
  Serial.print("Quaternion Z1: "); Serial.println(quat_Z1, 4);

  // Afficher les données sur le moniteur série pour le capteur 2 (jambe gauche)
  Serial.println("=== Capteur Jambe Gauche (0x29) ===");
  Serial.print("Acceleration X2 (m/s²): "); Serial.println(accel_X2);
  Serial.print("Acceleration Y2 (m/s²): "); Serial.println(accel_Y2);
  Serial.print("Acceleration Z2 (m/s²): "); Serial.println(accel_Z2);
  Serial.print("Quaternion W2: "); Serial.println(quat_W2, 4);
  Serial.print("Quaternion X2: "); Serial.println(quat_X2, 4);
  Serial.print("Quaternion Y2: "); Serial.println(quat_Y2, 4);
  Serial.print("Quaternion Z2: "); Serial.println(quat_Z2, 4);
  
  // Paquet 1: BNO055_right_leg (données de la jambe droite)
  StaticJsonDocument<128> doc4;
  JsonObject bno055_right_leg = doc4.createNestedObject("BNO055_right_leg");
  bno055_right_leg["accel_x"] = accel_X1;
  bno055_right_leg["accel_y"] = accel_Y1;
  bno055_right_leg["accel_z"] = accel_Z1;
  bno055_right_leg["quat_w"] = quat_W1;
  bno055_right_leg["quat_x"] = quat_X1;
  bno055_right_leg["quat_y"] = quat_Y1;
  bno055_right_leg["quat_z"] = quat_Z1;

  // Sérialisation et publication sur le canal "esp32/output4"
  String output4;
  serializeJson(doc4, output4);
  client.publish("esp32/output4", output4.c_str());

  // Paquet 2: BNO055_left_leg (données dde la jambe gauche)
  StaticJsonDocument<128> doc5;
  JsonObject bno055_left_leg = doc5.createNestedObject("BNO055_left_leg");
  bno055_left_leg["accel_x"] = accel_X2;
  bno055_left_leg["accel_y"] = accel_Y2;
  bno055_left_leg["accel_z"] = accel_Z2;
  bno055_left_leg["quat_w"] = quat_W2;
  bno055_left_leg["quat_x"] = quat_X2;
  bno055_left_leg["quat_y"] = quat_Y2;
  bno055_left_leg["quat_z"] = quat_Z2;

  // Sérialisation et publication sur le canal "esp32/output5"
  String output5;
  serializeJson(doc5, output5);
  client.publish("esp32/output5", output5.c_str());

  delay(100);  // Délai pour s'assurer que le paquet du bas du corps est bien envoyé
}