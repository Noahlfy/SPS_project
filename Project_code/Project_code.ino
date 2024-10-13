#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <ArduinoJson.h>

// I2C address of the BNO055 sensor
int Adafruit_BNO055_address = 0x28;

// Variables to store sensor data
float accel_X, accel_Y, accel_Z;
float euler_X, euler_Y, euler_Z;

// Register addresses for the BNO055
#define OPR_MODE 0x3D
#define CALIB_STAT 0x35
#define LIA_DATA_X_LSB 0x28
#define LIA_DATA_X_MSB 0x29
#define LIA_DATA_Y_LSB 0x2A
#define LIA_DATA_Y_MSB 0x2B
#define LIA_DATA_Z_LSB 0x2C
#define LIA_DATA_Z_MSB 0x2D
#define EUL_DATA_X_LSB 0x1A
#define EUL_DATA_X_MSB 0x1B
#define EUL_DATA_Y_LSB 0x1C
#define EUL_DATA_Y_MSB 0x1D
#define EUL_DATA_Z_LSB 0x1E
#define EUL_DATA_Z_MSB 0x1F

// Wi-Fi credentials
const char* ssid = "iPhone Noah";
const char* password = "polekeleke";

// Set up the broker
const char* mqtt_server = "172.20.10.10";

WiFiClient espClient;
PubSubClient client(espClient);


void checkCalibrationStatus() {
  Wire.beginTransmission(Adafruit_BNO055_address);
  Wire.write(CALIB_STAT);  // Registre de statut de calibration
  Wire.endTransmission();
  
  Wire.requestFrom(Adafruit_BNO055_address, 1);  // Demande d'une seule valeur (le statut de calibration)

  if (Wire.available()) {
    byte calibration_status = Wire.read();
    byte sys = (calibration_status >> 6) & 0x03;  // Système
    byte gyro = (calibration_status >> 4) & 0x03;  // Gyroscope
    byte accel = (calibration_status >> 2) & 0x03; // Accéléromètre
    byte mag = calibration_status & 0x03;          // Magnétomètre

    Serial.print("Calib Sys: "); Serial.print(sys, DEC);
    Serial.print(", Gyro: "); Serial.print(gyro, DEC);
    Serial.print(", Accel: "); Serial.print(accel, DEC);
    Serial.print(", Mag: "); Serial.println(mag, DEC);

    if (sys < 3 || gyro < 3 || accel < 3 || mag < 3) {
      Serial.println("Le capteur n'est pas entièrement calibré. Calibration en cours...");
    } else {
      Serial.println("Le capteur est entièrement calibré.");
    }
  }
}

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

void setup_BNO055() {
  
  Wire.beginTransmission(Adafruit_BNO055_address);
  Wire.write(OPR_MODE);
  Wire.write(0b00001100);  // IMU Mode
  Wire.endTransmission();
  delay(20);
}

void setup() {
  
  Wire.begin();
  Serial.begin(115200);
  delay(100);

  setup_wifi();
  client.setServer(mqtt_server, 1883);
  setup_BNO055();

  // Vérification de l'état de calibration
  Wire.beginTransmission(Adafruit_BNO055_address);
  Wire.write(CALIB_STAT);  // Calibration status register
  Wire.endTransmission();
  Wire.requestFrom(Adafruit_BNO055_address, 1);
  
  if (Wire.available()) {
    byte calibration_status = Wire.read();
    Serial.print("Calibration status: ");
    Serial.println(calibration_status, BIN);
  }
}

void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("espClient")) {
      Serial.println("connected");
      client.subscribe("esp32/output");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  checkCalibrationStatus();

  // Measure acceleration (in m/s²)
  accel_X = readSensorData(LIA_DATA_X_LSB, LIA_DATA_X_MSB) / 100.0;
  accel_Y = readSensorData(LIA_DATA_Y_LSB, LIA_DATA_Y_MSB) / 100.0;
  accel_Z = readSensorData(LIA_DATA_Z_LSB, LIA_DATA_Z_MSB) / 100.0;

  // Measure Euler angles (orientation in degrees)
  euler_X = readSensorData(EUL_DATA_X_LSB, EUL_DATA_X_MSB) / 16.0;
  euler_Y = readSensorData(EUL_DATA_Y_LSB, EUL_DATA_Y_MSB) / 16.0;
  euler_Z = readSensorData(EUL_DATA_Z_LSB, EUL_DATA_Z_MSB) / 16.0;

  // Print acceleration data
  Serial.print("Acceleration X (m/s²): "); Serial.println(accel_X);
  Serial.print("Acceleration Y (m/s²): "); Serial.println(accel_Y);
  Serial.print("Acceleration Z (m/s²): "); Serial.println(accel_Z);

  // Print orientation data
  Serial.print("Euler Angle X (Heading): "); Serial.println(euler_X);
  Serial.print("Euler Angle Y (Roll): "); Serial.println(euler_Y);
  Serial.print("Euler Angle Z (Pitch): "); Serial.println(euler_Z);

  // Creating a JSON object
  StaticJsonDocument<200> doc;
  doc["accel_x"] = accel_X;
  doc["accel_y"] = accel_Y;
  doc["accel_z"] = accel_Z;
  doc["eul_x"] = euler_X;
  doc["eul_y"] = euler_Y;
  doc["eul_z"] = euler_Z;

  // Publish JSON to MQTT
  String output;
  serializeJson(doc, output);
  client.publish("esp32/output", output.c_str());

  // Création d'une chaîne CSV
  String csv_output = String(accel_X) + "," + String(accel_Y) + "," + String(accel_Z) + "," + String(euler_X) + "," + String(euler_Y) + "," + String(euler_Z);
  // Publier le CSV via MQTT
  client.publish("esp32/output.csv", csv_output.c_str());

  delay(500);  // Add a delay between readings
}

// Function to read data from two registers (LSB and MSB) and combine them into a 16-bit value
int readSensorData(int LSB_reg, int MSB_reg) {
  Wire.beginTransmission(Adafruit_BNO055_address);
  Wire.write(LSB_reg);  // Point to the LSB register
  Wire.endTransmission();

  delayMicroseconds(50);

  Wire.requestFrom(Adafruit_BNO055_address, 2);  // Request 2 bytes of data from the sensor

  if (Wire.available() == 2) {
    int LSB = Wire.read();  // Read LSB
    int MSB = Wire.read();  // Read MSB

    int value = (MSB << 8) | LSB;
    if (value > 32767) {
      value -= 65536;
    }
    return value;  // Combine MSB and LSB
  }
  
  return 0;  // Return 0 if data is unavailable
}
