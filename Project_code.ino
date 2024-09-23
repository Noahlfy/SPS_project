#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <ArduinoJson.h>

// I2C address of the BNO055 sensor
int Adafruit_BNO055_address = 0x28;

// Variables to store sensor data
int accel_X, accel_Y, accel_Z;
int euler_X, euler_Y, euler_Z;

// Register addresses for the BNO055
#define OPR_MODE 0x3D
#define ACC_DATA_X_LSB 0x08
#define ACC_DATA_X_MSB 0x09
#define ACC_DATA_Y_LSB 0x0A
#define ACC_DATA_Y_MSB 0x0B
#define ACC_DATA_Z_LSB 0x0C
#define ACC_DATA_Z_MSB 0x0D
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
  Wire.begin();
  
  Wire.beginTransmission(Adafruit_BNO055_address);
  Wire.write(OPR_MODE);
  Wire.write(0b00001001);  // COMPASS Mode
  Wire.endTransmission();
}

void setup() {
  Serial.begin(115200);

  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  setup_BNO055();
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

  // Measure acceleration
  accel_X = readSensorData(ACC_DATA_X_LSB, ACC_DATA_X_MSB);
  accel_Y = readSensorData(ACC_DATA_Y_LSB, ACC_DATA_Y_MSB);
  accel_Z = readSensorData(ACC_DATA_Z_LSB, ACC_DATA_Z_MSB);

  // Measure Euler angles (orientation)
  euler_X = readSensorData(EUL_DATA_X_LSB, EUL_DATA_X_MSB);
  euler_Y = readSensorData(EUL_DATA_Y_LSB, EUL_DATA_Y_MSB);
  euler_Z = readSensorData(EUL_DATA_Z_LSB, EUL_DATA_Z_MSB);

  // Print acceleration data
  Serial.print("Acceleration X: "); Serial.println(accel_X);
  Serial.print("Acceleration Y: "); Serial.println(accel_Y);
  Serial.print("Acceleration Z: "); Serial.println(accel_Z);

  // Print orientation data
  Serial.print("Euler Angle X (Heading): "); Serial.println(euler_X / 16.0);
  Serial.print("Euler Angle Y (Roll): "); Serial.println(euler_Y / 16.0);
  Serial.print("Euler Angle Z (Pitch): "); Serial.println(euler_Z / 16.0);

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
  client.publish("esp32/output.json", output.c_str());


  // Création d'une chaîne CSV
  String csv_output = String(accel_X) + "," + String(accel_Y) + "," + String(accel_Z) + "," + String(euler_X) + "," + String(euler_Y) + "," + String(euler_Z);
  // Publier le CSV via MQTT
  client.publish("esp32/output.csv", csv_output.c_str());

  delay(200);  // Add a delay between readings
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
    return (MSB << 8) | LSB;  // Combine MSB and LSB
  }
  
  return 0;  // Return 0 if data is unavailable
}
