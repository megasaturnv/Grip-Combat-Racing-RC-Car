#include <AFMotor.h>

AF_DCMotor motor1(1);
AF_DCMotor motor2(2);
AF_DCMotor motor3(3);
AF_DCMotor motor4(4);

bool haveMessage = false;

//byte receivedBytes[8];
byte receivedBytes[] = {0, 0, 0, 0, 0, 0, 0, 0};
byte receivedArrayLength = 8;

///////////////
// Functions //
///////////////
void serialFlush() {
  char x;
  while (Serial.available() > 0) {
    x = Serial.read();
  }
}

//const byte leftMotorLeftPin = 8;
//const byte leftMotorRightPin = 7;
//const byte leftMotorPwmPin = 9;
void leftTrackForward(byte pwmSpeed) {
  motor1.run(FORWARD);
  motor2.run(FORWARD);
  motor1.setSpeed(pwmSpeed);
  motor2.setSpeed(pwmSpeed);
}
void leftTrackBackward(byte pwmSpeed) {
  motor1.run(BACKWARD);
  motor2.run(BACKWARD);
  motor1.setSpeed(pwmSpeed);
  motor2.setSpeed(pwmSpeed);
}
void leftTrackStop() {
  motor1.setSpeed(0);
  motor2.setSpeed(0);
}

//const byte rightMotorLeftPin = 5;
//const byte rightMotorRightPin = 4;
//const byte rightMotorPwmPin = 3;
void rightTrackForward(byte pwmSpeed) {
  motor3.run(FORWARD);
  motor4.run(FORWARD);
  motor3.setSpeed(pwmSpeed);
  motor4.setSpeed(pwmSpeed);
}
void rightTrackBackward(byte pwmSpeed) {
  motor3.run(BACKWARD);
  motor4.run(BACKWARD);
  motor3.setSpeed(pwmSpeed);
  motor4.setSpeed(pwmSpeed);
}
void rightTrackStop() {
  motor3.setSpeed(0);
  motor4.setSpeed(0);
}

void blinkLED() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(50);
  digitalWrite(LED_BUILTIN, LOW);
  delay(50);
}

void stopAllMotors() {
  motor1.setSpeed(0);
  motor2.setSpeed(0);
  motor3.setSpeed(0);
  motor4.setSpeed(0);
  motor1.run(RELEASE);
  motor2.run(RELEASE);
  motor3.run(RELEASE);
  motor4.run(RELEASE);
}


///////////
// Setup //
///////////
void setup() {
  pinMode(13, OUTPUT);

  blinkLED();
  Serial.begin(9600);

  stopAllMotors();

  for (int i = 0; i <= 7; i++) {
    receivedBytes[i] = 0;
  }

  blinkLED();

  //Serial.println("Ready!");
}


//////////
// Loop //
//////////
void loop() {
  /*  if (Serial.available() >= 8) {
      for (int i = 0; i <= 7; i++) {
        receivedBytes[i] = Serial.read();
         //= Serial.readStringUntil('\n');
      }*/
  if (Serial.available() >= 8) {
    Serial.readBytes(receivedBytes, 8);
    haveMessage = true;
    for (int i = 0; i <= 7; i++) {
      //Serial.print(receivedBytes[i], HEX);
      //Serial.print(" ");
    }
    //Serial.println(" ");

    serialFlush();

  }

  if (haveMessage) {
    digitalWrite(LED_BUILTIN, HIGH);

    if (receivedBytes[0] > 0x00) { //left track has data
      if (receivedBytes[0] < 0x80) { //If < 128 (DEC), track goes backwards
        //range of values of receivedBytes[0] = 1 to 127 (127 total values)
        //range of pwm values = 0 to 255 (256 total values)
        //pwmValue = ((128-receivedBytes[0])*2)+1
        //for a range of 1 to 127, this gives a range of 3-255

        leftTrackBackward(((128 - receivedBytes[0]) * 2) + 1);
        //Serial.println("LTBw");
      } else if (receivedBytes[0] > 0x80) { //If > 128 (DEC), track goes forwards
        //range of values of receivedBytes[0] = 129 to 255 (127 total values)
        //range of pwm values = 0 to 255 (256 total values)
        //pwmValue = ((receivedBytes[0]-128)*2)+1
        //for a range of 129 to 255, this gives a range of 3-255

        leftTrackForward(((receivedBytes[0] - 128) * 2) + 1);
        //Serial.println("LTFw");
      } else {
        leftTrackStop(); //Stop if receivedBytes[0] = 0x80
      }

    }
    if (receivedBytes[1] > 0x00) { //right track has data
      if (receivedBytes[1] < 0x80) { //If < 128 (DEC), track goes backwards
        rightTrackBackward(((128 - receivedBytes[1]) * 2) + 1);
        //Serial.println("RTBw");
      } else if (receivedBytes[1] > 0x80) { //If > 128 (DEC), track goes forwards
        rightTrackForward(((receivedBytes[1] - 128) * 2) + 1);
        //Serial.println("RTFw");
      } else {
        rightTrackStop(); //Stop if receivedBytes[1] = 0x80
      }
    }





    //receivedBytes[2] to receivedBytes[7] not used yet
    //e.g.  receivedBytes[2] = Amount of time to execute left wheel's command for
    //      receivedBytes[3] = Amount of time to execute right wheel's command for
    //      receivedBytes[4] = Brightness of headlights
    //      receivedBytes[5] = Weapon functions
    //      receivedBytes[6] = Return information about the current state of the vehicle
    //      receivedBytes[7] = Parity
    // Haven't decided on a delimiter like '\n' yet





    for (int i = 0; i <= 7; i++) {
      receivedBytes[i] = 0;
    }
    haveMessage = false;
    //Serial.println("FINISH LOOP\n");
    digitalWrite(LED_BUILTIN, LOW);
  }
}
