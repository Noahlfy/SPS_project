#include <Wire.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <Adafruit_BNO055.h> 
#include <Adafruit_Sensor.h>
#include <MAX30105.h>
#include "algorithm.h"  // Bibliothèque pour les calculs du pouls et du SpO2
#include <Adafruit_BMP280.h>

// Déclaration du capteur BMP280
Adafruit_BMP280 bmp; 

// Initialisation du premier BNO055 (adresse 0x28)
Adafruit_BNO055 bno1 = Adafruit_BNO055(55, 0x28);  

// Initialisation du deuxième BNO055 (adresse 0x29)
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

#define BUFFER_SIZE 100 // Taille du buffer pour le calcul du pouls et du SpO2

// Variables for HW-605 (MAX30102)
MAX30105 particleSensor;
long irValue = 0; // Infrarouge (IR) du capteur, utilisé pour mesurer le pouls
float spo2 = 0; // Taux de SpO2 (saturation en oxygène)
int beatsPerMinute; // Pouls en BPM

// Pour stocker les données du capteur
uint32_t ir_buffer[100]; // Utilisation de uint32_t pour le buffer IR
uint32_t red_buffer[100]; // Utilisation de uint32_t pour le buffer rouge
int bufferLength = BUFFER_SIZE;

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

  // Initialiser le premier BNO055
  if (!bno1.begin()) {
    Serial.println("Échec de la connexion au premier BNO055 (0x28) !");
    while (1);
  }
  
  // Initialiser le deuxième BNO055
  if (!bno2.begin()) {
    Serial.println("Échec de la connexion au deuxième BNO055 (0x29) !");
    while (1);
  }

  // // Initialisation du capteur BMP280
  // if (!bmp.begin(0x77)) {  // Adresse I2C du BMP280 (peut être 0x76 ou 0x77)
  //   Serial.println("Erreur de communication avec le BMP280");
  //   while (1); // Boucle infinie en cas d'erreur
  // }

  // Configuration des paramètres du BMP280
  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,  // Mode normal
                  Adafruit_BMP280::SAMPLING_X2,   // Sur-échantillonnage x2 pour la température
                  Adafruit_BMP280::SAMPLING_X16,  // Sur-échantillonnage x16 pour la pression
                  Adafruit_BMP280::FILTER_X16,    // Filtrage x16
                  Adafruit_BMP280::STANDBY_MS_500);  // Délai d'attente entre mesures 500 ms

  // Initialiser le capteur MAX30102 (HW-605)
  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) {
    Serial.println("Échec de la connexion au MAX30102 !");
    while (1);
  }
  particleSensor.setup(); // Configurer le capteur
  particleSensor.setPulseAmplitudeRed(0x0A);  // Ajuster la LED rouge (affecte la mesure de SpO2)
  particleSensor.setPulseAmplitudeIR(0x0F);  // Puissance LED IR pour la lecture de pouls

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
    Serial.println("Le capteur n'est pas entièrement calibré. Calibration en cours...");
    
    if (accel < 3) Serial.println("Calibrez l'accéléromètre en bougeant l'appareil sur tous les axes.");
    if (gyro < 3) Serial.println("Calibrez le gyroscope en laissant l'appareil immobile sur une surface plane.");
    if (mag < 3) Serial.println("Calibrez le magnétomètre en effectuant des mouvements en forme de 8.");
    
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


  // Vérification de l'état de calibration pour les deux capteurs
  checkCalibrationStatus(bno1);  
  checkCalibrationStatus(bno2);  

  // Lire les données d'accélération manuellement pour le premier BNO055 (0x28)
  float accel_X1, accel_Y1, accel_Z1;
  readAcceleration(0x28, accel_X1, accel_Y1, accel_Z1);

  // Lire les quaternions du premier BNO055 (0x28)
  imu::Quaternion quat1 = bno1.getQuat();
  float quat_W1 = quat1.w();
  float quat_X1 = quat1.x();
  float quat_Y1 = quat1.y();
  float quat_Z1 = quat1.z();

  // Lire les données d'accélération manuellement pour le deuxième BNO055 (0x29)
  float accel_X2, accel_Y2, accel_Z2;
  readAcceleration(0x29, accel_X2, accel_Y2, accel_Z2);

  // Lire les quaternions du deuxième BNO055 (0x29)
  imu::Quaternion quat2 = bno2.getQuat();
  float quat_W2 = quat2.w();
  float quat_X2 = quat2.x();
  float quat_Y2 = quat2.y();
  float quat_Z2 = quat2.z();

  // Lire les données du capteur MAX30102
  for (int i = 0; i < bufferLength; i++) {
    while (!particleSensor.available()) {
      particleSensor.check();
    }

    // Récupérer les valeurs Rouge et IR
    red_buffer[i] = particleSensor.getRed();
    ir_buffer[i] = particleSensor.getIR();

    // Supprimer l'échantillon précédent pour faire de la place
    particleSensor.nextSample();
  }

  // Variables pour les résultats des calculs
  int32_t spo2_val = 0; // Changer uint32_t en int32_t
  int8_t spo2_valid = 0; // État de validité de SpO2
  int32_t heart_rate = 0; // Changer uint32_t en int32_t
  int8_t hr_valid = 0; // État de validité du pouls

  // Calculer le SpO2 et le pouls à partir des buffers IR et rouge
  maxim_heart_rate_and_oxygen_saturation(ir_buffer, bufferLength, red_buffer, &spo2_val, &spo2_valid, &heart_rate, &hr_valid);

  // Vérifier les valeurs de SpO2 et de fréquence cardiaque
  if (spo2_val < 90 || spo2_val > 100) {
    spo2_val = 0; // Ou une valeur par défaut ou un message d'erreur
    spo2_valid = 0; // Indiquer que la mesure n'est pas valide
  }

  if (heart_rate < 30 || heart_rate > 200) {
    heart_rate = 0; // Ou une valeur par défaut ou un message d'erreur
    hr_valid = 0; // Indiquer que la mesure n'est pas valide
  }

  // Lire la température et la pression depuis le BMP280
  float temperature = bmp.readTemperature();
  float pressure = bmp.readPressure() / 100.0; // Conversion en hPa

  // Afficher les données sur le moniteur série pour le capteur 1
  Serial.println("=== Capteur 1 (0x28) ===");
  Serial.print("Acceleration X1 (m/s²): "); Serial.println(accel_X1);
  Serial.print("Acceleration Y1 (m/s²): "); Serial.println(accel_Y1);
  Serial.print("Acceleration Z1 (m/s²): "); Serial.println(accel_Z1);
  Serial.print("Quaternion W1: "); Serial.println(quat_W1, 4);
  Serial.print("Quaternion X1: "); Serial.println(quat_X1, 4);
  Serial.print("Quaternion Y1: "); Serial.println(quat_Y1, 4);
  Serial.print("Quaternion Z1: "); Serial.println(quat_Z1, 4);

  // Afficher les données sur le moniteur série pour le capteur 2
  Serial.println("=== Capteur 2 (0x29) ===");
  Serial.print("Acceleration X2 (m/s²): "); Serial.println(accel_X2);
  Serial.print("Acceleration Y2 (m/s²): "); Serial.println(accel_Y2);
  Serial.print("Acceleration Z2 (m/s²): "); Serial.println(accel_Z2);
  Serial.print("Quaternion W2: "); Serial.println(quat_W2, 4);
  Serial.print("Quaternion X2: "); Serial.println(quat_X2, 4);
  Serial.print("Quaternion Y2: "); Serial.println(quat_Y2, 4);
  Serial.print("Quaternion Z2: "); Serial.println(quat_Z2, 4);

  // Afficher les résultats du capteur MAX30102
  spo2 = static_cast<float>(spo2_val); // Conversion en float si nécessaire
  beatsPerMinute = heart_rate;

  // Affiche les valeurs pour le pouls et SpO2
  Serial.print("Pouls (BPM): "); Serial.println(beatsPerMinute);
  Serial.print("SpO2: "); Serial.println(spo2);

  // Afficher la température et la pression lues depuis le BMP280
  Serial.print("Température (°C) : "); Serial.println(temperature);
  Serial.print("Pression (hPa) : "); Serial.println(pressure);

  // Création d'un objet JSON pour envoyer les données via MQTT
  StaticJsonDocument<512> doc;

  // Ajouter les données du capteur MAX30102
  JsonObject max30102 = doc.createNestedObject("MAX30102");
  max30102["SpO2"] = spo2;
  max30102["BPM"] = beatsPerMinute;

  // Ajouter les données du capteur BMP280
  JsonObject bmp280 = doc.createNestedObject("BMP280");
  bmp280["temperature"] = temperature;
  bmp280["pressure"] = pressure;

  // Ajouter les données du premier BNO055 (tête)
  JsonObject bno055_head = doc.createNestedObject("BNO055_head");
  bno055_head["accel_x"] = accel_X1;
  bno055_head["accel_y"] = accel_Y1;
  bno055_head["accel_z"] = accel_Z1;
  bno055_head["quat_w"] = quat_W1;
  bno055_head["quat_x"] = quat_X1;
  bno055_head["quat_y"] = quat_Y1;
  bno055_head["quat_z"] = quat_Z1;

  // Ajouter les données du deuxième BNO055 (torse)
  JsonObject bno055_chest = doc.createNestedObject("BNO055_chest");
  bno055_chest["accel_x"] = accel_X2;
  bno055_chest["accel_y"] = accel_Y2;
  bno055_chest["accel_z"] = accel_Z2;
  bno055_chest["quat_w"] = quat_W2;
  bno055_chest["quat_x"] = quat_X2;
  bno055_chest["quat_y"] = quat_Y2;
  bno055_chest["quat_z"] = quat_Z2;

  // Publier les données en format JSON
  String output;
  serializeJson(doc, output);
  client.publish("esp32/output", output.c_str());

  delay(500);  // Délai entre les lectures
}