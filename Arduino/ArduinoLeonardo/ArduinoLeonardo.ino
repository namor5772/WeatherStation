#include <math.h>
#include <Wire.h>
#include <Servo.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_INA260.h>
#include <Adafruit_BME280.h>

#define SEALEVELPRESSURE_HPA (1013.25)

// Must set "#define DEBUG" if you are to run this code with the Serial set and monitored.
// If running in production (ie. no connection to PC) then MUST comment out "#define DEBUG",
// before compiling and loading, and then disconnecting from PC and restarting.

//#define DEBUG

// creating objects for Adafruit I2C sensors
Adafruit_BME280 bme; // I2C
Adafruit_INA260 ina260 = Adafruit_INA260(); // I2C

// serial message received from Raspberry Pi
char sm[65]; // to match serial buffer size + 1 for string terminator char '\0'
int sml; // length
char c; // first character

// Flashing led - related variable
const int ledPin=13;

// Analog Wind direction  - sensor related variables
int WindDirectionAnalogPin = A2;

// Tipping bucket rain sensor - related variables
const int iRT = 8; // D8
volatile int bRT;
const int nRT=100;
volatile unsigned long aRT[nRT]; // array to store millis time stamps for rain sensor tips

// Cup Anemometer sensor - related variables
const int iCA = 9; // D9
volatile int bCA;
const int nCA=5;
volatile unsigned long aCA[nCA]; // array to store millis time stamps for cup anemometer spins

volatile unsigned long tsINT = 0; // time stamp in millis for generic sensor tip
volatile boolean bINT = false; // flag set when interrupt triggered

// Relay - related variable
const int RelayDigitalPin = 5; // D5

// Servo - related variables
const int ServoDigitalPin = 6; // D6 - PWM
int ServoPos = 0; // variable to store the servo position
int ServoStartpos = 113;
int ServoFinpos = 93;
int ServoPress2Start = 6000;
int ServoPress2Stop = 10000;
Servo DongleServo;


// Flashes Arduino LED (used for fun testing)
void flash(int n) {
  for (int i=0; i<n; i++)  {
    digitalWrite(ledPin, HIGH); delay(250);    
    digitalWrite(ledPin, LOW); delay(250);    
  }
}

// 'magik' software reset function!
void(* resetFunc) (void) = 0;

void setup() {

  // setup ins to differentaiate interrupt source
  pinMode(iRT,INPUT);
  pinMode(iCA,INPUT);

  
  // Digital relay powering wifi dongle set to OFF via pin D5 initially
  pinMode(RelayDigitalPin,OUTPUT);
  digitalWrite(RelayDigitalPin, LOW);
  
  // attaches the servo on pin D6 to the servo object 
  DongleServo.attach(ServoDigitalPin);
  DongleServo.write(ServoStartpos);
  delay(100);  
  
  // Tipping bucket Rain Sensor and Cup Anemometer Sensor interrupt setup
  attachInterrupt(digitalPinToInterrupt(7),aSensorTripped, RISING); // Interrupt on D7
  
  // Flashing LED pin intialised
  pinMode(ledPin, OUTPUT);
  
  // Serial connection to Raspberry PI
  Serial1.begin(4800);
  while (!Serial1){ delay(10); }

  // Serial connection to serial monitor (used for testing purposes)  
  #ifdef DEBUG
    Serial.begin(4800);  
    while (!Serial){ delay(10); }
  #endif  
  Serial.println(" ");
  Serial.println(F("At Startpos deg"));  

  // Starting ina260 sensor board 
  if (!ina260.begin()) {
    Serial.println(F("INA260 not found"));
    while(1);
  } else {
    Serial.println(" ");
    Serial.println(F("Found INA260 chip"));
  }  

  // Starting BME280 sensor board
  unsigned status;
  status = bme.begin();  
  if (!bme.begin()) {
    Serial.println(F("BME280 not found"));
    while (1);
  } else {
    Serial.println(F("Found BME280 chip"));
  }  

  // initialise tipping bucket rain sensor and cup anamometer variables  
  for (int j=0; j<nRT; j++) { aRT[j]=0.0; }
  for (int j=0; j<nCA; j++) { aCA[j]=0.0; }
}

void loop() {
  int n, i, j, sni;
  double T;
  double cu, bv, po;
  double te, pr, hu;
  float wr, ws, wd;
  int ra;
  int iwd;

  // perform non-time critical actions if interrupt triggered (outside of ISR) 
  if (bINT) {
    if (bCA==1) {
      // push last timestamp tsCA1 onto the end of the aCA[] array (element nCA-1). aCA[0] is lost.
      for (int j=1; j<nCA; j++) aCA[j-1] = aCA[j];
      aCA[nCA-1] = tsINT;
    }
    else if (bRT==1) {
      // push last timestamp tsINT onto the end of the aRT[] array (element nRT-1). aRT[0] is lost.
      for (int j=1; j<nRT; j++) aRT[j-1] = aRT[j];
      aRT[nRT-1] = tsINT;
    }
    // reset ISR flag to false after ISR has been processed
    bINT = false;
  }    

  // Reading serial messages received from the Raspberry PI.
  // Assuming <= 64 bytes, and ignoring rest if any.
  sml = 0;
  while (Serial1.available()) {
    delay(3);
    if (Serial1.available() >0) {
      c = Serial1.read();
      if (sml<64) {
        sm[sml] = c;
        sml += 1;
      }
    }    
  }
  sm[sml] = '\0'; // add string terminator character
  
  if (sml >0) {      
    c = sm[0];
    n = c-'0';
    Serial.println(" ");
    Serial.print(F("NUM,CHR: "));
    Serial.print(sml);
    Serial.print(" ");
    i = 0; while (sm[i] != '\0') { Serial.print(sm[i]); i++; }    
    Serial.println(" ");
    
    if (c=='f') {
      // Flashes Arduino LED n times (used for fun testing)   
      c = sm[1];
      n = c-'0';
      flash(n);
      delay(100);
      Serial.println(F("flashed LED"));
    }
    else if (c=='q') {
      // goes from startpos degrees to finpos degrees (to press wifi dongle button)
      for(ServoPos = ServoStartpos; ServoPos>=ServoFinpos; ServoPos-=10) { 
        DongleServo.write(ServoPos);   // tell servo to go to position in variable 'Servopos' 
        delay(15);                     // waits 15ms for the servo to reach the position 
      }
      Serial.println(F("At Finpos deg"));
      
      delay(ServoPress2Stop); // keeps button pressed for ServoPress2Stop milliseconds
      
      // goes from finpos degrees to startpos degrees (to stop pressing button)
      for(ServoPos = ServoFinpos; ServoPos <= ServoStartpos; ServoPos += 10) { 
        DongleServo.write(ServoPos);     // tell servo to go to position in variable 'Servpos' 
        delay(15);                       // waits 15ms for the servo to reach the position 
      }
      Serial.println(F("At Startpos degrees"));
    }
    else if (c=='s') {
      // goes from startpos degrees to finpos degrees (to press wifi dongle button)
      for(ServoPos = ServoStartpos; ServoPos>=ServoFinpos; ServoPos-=10) { 
        DongleServo.write(ServoPos);   // tell servo to go to position in variable 'Servopos' 
        delay(15);                     // waits 15ms for the servo to reach the position 
      }
      Serial.println(F("At Finpos degrees"));
      
      delay(ServoPress2Start); // keeps button pressed for ServoPress2Start milliseconds
      
      // goes from finpos degrees to startpos degrees (to stop pressing button)
      for(ServoPos = ServoFinpos; ServoPos <= ServoStartpos; ServoPos += 10) { 
        DongleServo.write(ServoPos);     // tell servo to go to position in variable 'Servpos' 
        delay(15);                       // waits 15ms for the servo to reach the position 
      }
      Serial.println(F("At Startpos degrees"));
    }
    else if (c=='u') {
      // reads the digital I2C BME280 sensor. Temperature, Pressure and Humidity
      te = bme.readTemperature();
      pr = bme.readPressure() / 100.0F;
      hu = bme.readHumidity();

      // send Temperature, Pressure and Humidity to serial monitor
      Serial.print(F("Temperature: "));
      Serial.print(te);
      Serial.println(F(" *C"));
      Serial.print(F("Pressure: "));
      Serial.print(pr);
      Serial.println(F(" hPa"));
      Serial.print(F("Humidity: "));
      Serial.print(hu);
      Serial.println(F(" %"));

      // send Temperature, Pressure and Humidity to Raspberry Pi
      Serial1.print(te);
      Serial1.print(" ");
      Serial1.print(pr);
      Serial1.print(" ");
      Serial1.print(hu);
      Serial1.print(" ");
      delay(500);

      // measure last hours cumulative rainfall, current wind speed and current wind dirction
      // (averaged over a short time)
      wr = getCumulativeRainfall(0.25);
      ws = getWindSpeed();
      wd = getWindDirection();
      
      //wr = -4.0;
      //ws = -5.0;
      //wd = -6.0;
      
      // send data to serial monitor
      Serial.print(F("Rainfall: "));
      Serial.print(wr);
      Serial.println(F(" mm"));
      Serial.print(F("Wind speed: "));
      Serial.print(ws);
      Serial.println(F(" km/h"));
      Serial.print(F("Wind direction: "));
      Serial.print(wd);
      Serial.println(F(" deg"));
      
      // send data to Raspberry Pi
      Serial1.print(wr);
      Serial1.print(" ");
      Serial1.print(ws);
      Serial1.print(" ");
      Serial1.print(wd);
      Serial1.print(" ");
      delay(500);

      // reads the digital I2C INA260 sensor. IOT Current, Voltage and Power
      cu = ina260.readCurrent();
      bv = ina260.readBusVoltage();
      po = ina260.readPower();
      
      // send Current, Bus Voltage and Power to serial monitor
      Serial.print(F("Current: "));
      Serial.print(cu);
      Serial.println(F(" mA"));
      Serial.print(F("Bus Voltage: "));
      Serial.print(bv);
      Serial.println(" mV");
      Serial.print(F("Power: "));
      Serial.print(po);
      Serial.println(F(" mW"));

      // send Current, Bus Voltage and Power to Raspberry Pi
      Serial1.print(cu);
      Serial1.print(" ");
      Serial1.print(bv);
      Serial1.print(" ");
      Serial1.println(po);
      delay(500);
    }    
    else if (c=='x') {
      // set the relay to LOW - connection set - USB power working
      digitalWrite(RelayDigitalPin, LOW);      
      Serial.println("LOW");
    }
    else if (c=='y') {
      // set the relay to HIGH - connection broken - USB power off
      digitalWrite(RelayDigitalPin, HIGH);      
      Serial.println("HIGH");
    }
    else if (c=='z') {
      // Reset arduino programatically
      Serial.println(F("Resetting Arduino"));
      delay(200);
      Serial.println();
      resetFunc();
      Serial.println(F("NEVER REACHED"));
    }
    else if ((sm[0]=='a')&&(sm[1]=='b')) {
      // running serial test
      Serial.println(F("Serial message from the Arduino"));
      Serial1.println(F("Serial message from the Arduino --------"));
      delay(200);
    }
  }

}

// returns mm of rain during last fh hours 
float getCumulativeRainfall(float fh)
{
//  float wr, ts, tsh;
  float ts = millis(); // current time stamp as float
  float tsh = ts - fh*1000.0*60.0*60.0; // time stamp "fh" hours ago
  if (tsh<0.0) tsh = 0.0; // no rain and initialization adjustment ;-)

  // count number of times bucket has tipped during last "fh" hours
  float wr = 0.0;
  for (int j=nRT-1; j>=0; j--) { if (aRT[j]>tsh) { wr += 1.0; } }

  // each bucket tip corresponds to 0.2794 mm of rain  
  return wr*0.2794;
}

// returns windspeed based on averaging several spin times 
float getWindSpeed()
{
  int gp = 1;
//  float ws;

  // count average time gap between last and last-4 time stamp and convert to km/h
  // where 1 spin/second = 2.4km/h. When first started, time stamps are initialised to
  // 0 or only one exists. In that case set wind speed to 0. Also if last time stamp occured
  // more than 20 seconds ago interpret that also as 0 windspeed.
  if ((aCA[nCA-1]==0) || (aCA[nCA-1-gp]==0) || (millis()-aCA[nCA-1] > 20000.0)){
    return 0.0;
  } 
  else {
    return 2400.0*gp/(aCA[nCA-1] - aCA[nCA-1-gp]);
  }
}

// returns wind direction 
float getWindDirection()
{
  float x;
  int iwd = analogRead(WindDirectionAnalogPin);      
  if (iwd < 72) { x = 112.5; }
  else if (iwd < 86) { x = 67.5; }
  else if (iwd < 107) { x = 90.0; }
  else if (iwd < 153) { x = 157.5; }
  else if (iwd < 212) { x = 135.0; }
  else if (iwd < 264) { x = 202.5; }
  else if (iwd < 346) { x = 180.0; }
  else if (iwd < 434) { x = 22.5; }
  else if (iwd < 531) { x = 45.0; }
  else if (iwd < 615) { x = 247.5; }
  else if (iwd < 665) { x = 225.0; }
  else if (iwd < 742) { x = 337.5; }
  else if (iwd < 806) { x = 0.0; }
  else if (iwd < 858) { x = 292.5; }
  else if (iwd < 917) { x = 315.0; }
  else if (iwd < 989) { x = 270.0; }
  else { x = -1.0; }
  return x;
}

// a Sensor is tripped - No software debounce since assume hardware
void aSensorTripped()
{
//  if ((millis() - tsINT) > 25 ) {
    // determine which sensor triggered interrupt
    bRT = digitalRead(iRT);  
    bCA = digitalRead(iCA);

    // time stamp for sensor trip      
    tsINT = millis();

    // set interrupt flag to true (for processing outside of this ISR)
    bINT = true;

    // just for debugging
    Serial.print(bRT);
    Serial.print(bCA);
    Serial.println(tsINT);
//  }
}
