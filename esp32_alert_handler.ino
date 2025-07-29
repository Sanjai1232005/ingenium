
#include <WiFi.h>
#include <WebServer.h>
#include <Firebase_ESP_Client.h>

const char* ssid = "vivo Y56 5G";
const char* password = "87654321";

#define FIREBASE_HOST "https://test-f50f7-default-rtdb.asia-southeast1.firebasedatabase.app/"
#define FIREBASE_AUTH "AIzaSyBgh4xC-JSxaks8MoiKYorkOeBs3fZ4VyI"

FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

WebServer server(80);

void handleAlert() {
  String message = server.arg("message");
  
  if (message == "eyes_closed") {
    Serial.println("Alert: Eyes Closed detected!");
  } else if (message == "no_face") {
    Serial.println("Alert: No Face detected!");
  } else if (message == "drowsy") {
    Serial.println("Alert: Drowsiness detected!");
  } else {
    Serial.println("Unknown alert message.");
  }

  String path = "/hello/" + String(millis());

  if (Firebase.RTDB.setString(&fbdo, path.c_str(), message.c_str())) {
    Serial.println("Alert sent to Firebase successfully!");
  } else {
    Serial.println("Firebase Error: " + fbdo.errorReason());
  }

  server.send(200, "text/plain", "Alert received: " + message);
}

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to Wi-Fi");
  Serial.print("ESP32 IP Address: ");
  Serial.println(WiFi.localIP());

  config.database_url = FIREBASE_HOST;
  config.signer.tokens.legacy_token = FIREBASE_AUTH;

  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);

  server.on("/alert", HTTP_GET, handleAlert);
  server.begin();
}

void loop() {
  server.handleClient();
}
