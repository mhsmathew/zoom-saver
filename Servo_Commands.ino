#include <Servo.h>
Servo servo;

void setup() {
  servo.attach(8);
  Serial.begin(9600);
  servo.write(0);
}

void loop() {
  char inByte = ' ';
  if(Serial.available( ) )  {  
    char inByte = Serial.read(); 
     if (inByte == 's') {
      servo.write(0);
    } else if (inByte == 'h') {
      servo.write(90);
    }
    delay(500);

    

  }  

}
