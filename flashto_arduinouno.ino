// Includes the needed libraries 
#include <DHT.h>
#include <Wire.h>

// Defining the variables
#define IRd           8
#define LDRPin        A1
#define DHTPin        9
#define DHTType       DHT22
#define SLAVE_ADDRESS 0x04        // Defining this Arduino as a slave to the Raspberry Pi
#define ADCValue      0.0048828125

// Initialise the DHT sensor
DHT dht(DHTPin, DHTType);

// Defining the flag used to stop the program
bool done = false;

// Toggling built-in LED for verifying that the program is working
int LEDPin = 13;

// Defining the variables used for data collection
int ldrValue, luxValue;
int IRAnalog, IRDigital;
byte imu_data[] = {0, 0, 0, 0};

// Initialise the LED for testing purposes
boolean ledOn = false;

// Callback for received data
void processMessage(int n){
  char ch = Wire.read();
  if(ch == '1'){
    toggleLED();
  }
}
// Ending the program
void end_program(){
  // Used for reading data from the serial monitor
  char ch;
  // Check to see if ! is available to be read
  if(Serial.available()){
    // Read the character
    ch = Serial.read();
    // End the program if exclamation point is entered in the serial monitor
    if(ch == '!'){
      done = true;
      Serial.println("Finished recording data");
    }
  }
}

// Method to toggle the LED for testing
void toggleLED(){
  ledOn = !ledOn;
  digitalWrite(LEDPin, ledOn);
}
 
// Executes when request is received from Raspberry Pi
void sendIMUReading(){
  Wire.write(imu_data, 4); 
}

void setup() {
  // Initialising the serial monitor
  Serial.begin(9600);
  pinMode(LEDPin, OUTPUT);
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(processMessage); // Used to specify a function when data is received from Master
  Wire.onRequest(sendIMUReading); // Used to specify a function when the Master requests data
  
  // Setting the pin to output or input
  pinMode(IRd, INPUT);

  dht.begin();
}

void loop() {
    // Calibrates the LDR and converts it to output in Lux
    ldrValue = analogRead(LDRPin);
	  luxValue = int(250.0/(ADCValue*ldrValue)-50.0);
	  
    // Reads the analog and digital value of TCRT5000
    IRDigital = digitalRead(IRd);
  
    // Reads the temperature or humidity for DHT22
    float humid = dht.readHumidity();
    float temp = dht.readTemperature();
    Serial.print("Analog Reading: "); Serial.print(IRAnalog);
    Serial.print("\t Digital Reading: "); Serial.println(IRDigital);
    Serial.print(luxValue); Serial.println(" Lux");
    Serial.print("Humidity: "); Serial.print(humid);Serial.print("%");
    Serial.print("\t Temperature: "); Serial.print(temp);Serial.println("°C");
  
    imu_data[0] = luxValue;
    imu_data[1] = humid;
    imu_data[2] = temp;
    imu_data[3] = IRDigital;
    Serial.print(imu_data[0]); Serial.print(imu_data[1]); Serial.println(imu_data[2]); Serial.println(imu_data[3]);
    end_program();
}
