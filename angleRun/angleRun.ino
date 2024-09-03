#include <Servo.h>

Servo myServo; 
int angle = 0; 
void setup() {
  Serial.begin(9600);   
  myServo.attach(9);    
  myServo.write(90);    
}

void loop() {
  if (Serial.available() > 0) {  
    String angleString = Serial.readStringUntil('\n');  
    angle = angleString.toInt();  
    Serial.println(angle);  
    
    if (angle >= 0 && angle <= 180) {  
      myServo.write(angle);  
    }
  }
}
