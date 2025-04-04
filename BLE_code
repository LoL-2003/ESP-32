#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

BLEServer* pServer = NULL;
BLECharacteristic* pSensorCharacteristic = NULL;
BLECharacteristic* pLedCharacteristic = NULL;
bool deviceConnected = false;
bool oldDeviceConnected = false;
int32_t value[4] = {23, -4, 6, 70}; // x-coordinate, y-coordinate, speed, distance

const int ledPin = 2; // GPIO pin for LED

// BLE Service & Characteristic UUIDs
#define SERVICE_UUID                 "19b10000-e8f2-537e-4f6c-d104768a1214"
#define SENSOR_CHARACTERISTIC_UUID    "19b10001-e8f2-537e-4f6c-d104768a1214"
#define LED_CHARACTERISTIC_UUID       "19b10002-e8f2-537e-4f6c-d104768a1214"

class MyServerCallbacks : public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
        deviceConnected = true;
    }

    void onDisconnect(BLEServer* pServer) {
        deviceConnected = false;
    }
};

class MyCharacteristicCallbacks : public BLECharacteristicCallbacks {
    void onWrite(BLECharacteristic* pCharacteristic) {
        std::string rawValue = pCharacteristic->getValue();

        if (rawValue.length() > 0) {
            uint8_t receivedByte = rawValue[0]; // Read first byte as unsigned

            Serial.print("Received raw byte from BLE: ");
            Serial.println(receivedByte); // Debugging output

            if (receivedByte == '1' || receivedByte == 1) {
                digitalWrite(ledPin, HIGH);
                Serial.println("✅ LED ON");
            } else if (receivedByte == '0' || receivedByte == 0) {
                digitalWrite(ledPin, LOW);
                Serial.println("✅ LED OFF");
            } else {
                Serial.println("❌ Invalid value received!");
            }
        }
    }
};

void setup() {
    Serial.begin(115200);
    pinMode(ledPin, OUTPUT);
    digitalWrite(ledPin, LOW); // Ensure LED starts OFF

    // Initialize BLE
    BLEDevice::init("ESP32");
    pServer = BLEDevice::createServer();
    pServer->setCallbacks(new MyServerCallbacks());

    // Create BLE Service
    BLEService *pService = pServer->createService(SERVICE_UUID);

    // Create Sensor Characteristic
    pSensorCharacteristic = pService->createCharacteristic(
        SENSOR_CHARACTERISTIC_UUID,
        BLECharacteristic::PROPERTY_READ |
        BLECharacteristic::PROPERTY_NOTIFY |
        BLECharacteristic::PROPERTY_INDICATE
    );

    // Create LED Characteristic
    pLedCharacteristic = pService->createCharacteristic(
        LED_CHARACTERISTIC_UUID,
        BLECharacteristic::PROPERTY_WRITE
    );

    // Register callback for LED characteristic
    pLedCharacteristic->setCallbacks(new MyCharacteristicCallbacks());

    // Add descriptors
    pSensorCharacteristic->addDescriptor(new BLE2902());
    pLedCharacteristic->addDescriptor(new BLE2902());

    // Start the service
    pService->start();

    // Start advertising
    BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
    pAdvertising->addServiceUUID(SERVICE_UUID);
    pAdvertising->setScanResponse(false);
    pAdvertising->setMinPreferred(0x00);
    BLEDevice::startAdvertising();

    Serial.println("Waiting for a client connection...");
}

void loop() {
    if (deviceConnected) {
        // Send the full `value` array as raw bytes
        pSensorCharacteristic->setValue((uint8_t*)value, sizeof(value));
        pSensorCharacteristic->notify();
        
        Serial.print("Sent values: ");
        Serial.print(value[0]); Serial.print(", ");
        Serial.print(value[1]); Serial.print(", ");
        Serial.print(value[2]); Serial.print(", ");
        Serial.println(value[3]);

        delay(3000);
    }

    if (!deviceConnected && oldDeviceConnected) {
        Serial.println("Device disconnected.");
        delay(500);
        pServer->startAdvertising();
        Serial.println("Restart advertising");
        oldDeviceConnected = deviceConnected;
    }

    if (deviceConnected && !oldDeviceConnected) {
        Serial.println("Device Connected");
        oldDeviceConnected = deviceConnected;
    }
}
