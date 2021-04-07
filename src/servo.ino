// Include the Servo library 
#include <Servo.h> 
// Declare the Servo pin 
int servoXPin = 9;
int servoYPin = 13;
int led = 13;
// Create a servo object 
Servo Servox;
Servo Servoy; 

float x;
float y;
void setup() {
 Serial.begin(1000000);
 Serial.setTimeout(10);
 pinMode(led, OUTPUT);
 Servox.attach(servoXPin); 
 Servoy.attach(servoYPin); 
}
void loop() {
 while (!Serial.available());
 String data = Serial.readString();
 x = get_x(data);
 y = get_y(data);
 Servox.write(x);
 Servoy.write(y);
 Serial.println(x);
 Serial.println(y);
}

float get_x(String data) {
  int commaI = data.indexOf(',');
  return data.substring(0, commaI).toFloat();
}

float get_y(String data) {
  int commaI = data.indexOf(',');\
  int array_length = data.length();
  return data.substring(commaI + 1, array_length + 1).toFloat();
}
