// Serial Commuincation Protocol
/////////////////////////// GLOBAL VARIABLES /////////////////////////////
#include <avr/io.h>
#include <avr/interrupt.h>

//3~= 200 Hz total period
//6.25~= 100 Hz total period
unsigned int reload = 3;//want full wave at 200 Hz, therefore need timer frequency of 200*100 = 20,000. i.e. T=0.00005 S.
// Arduino clock speed is 16 MHz, timer1 has pre scalar of 256. therefore Timer 1 speed = 16MHz/256=62.5kHz
//pulse time = 1/62.5kHz = 16 us.
// reload = desired_T / 16us (in the case of 200 Hz thats 5e-5/16e-6 = 3.125

//AF_DCMotor motor(4);

boolean EDGE = true;
volatile int on_cntr = 0;
int duty = 50;
int cntrl_pin = 3;
int cntrl_pin2 = 4;
int cntrl_pin3;
int cntrol_pin4;
int intArray[4];
const unsigned int MAX_MESSAGE_LENGTH = 13;
char terminateChar = ',';
int intVal;



void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(cntrl_pin, OUTPUT);

}

void loop() {
  if (Serial.available() == 0) {}
  if (Serial.available() > 0) {
    if (Serial.read() == '<') {
      // put your main code here, to run repeatedly:
      static char message[MAX_MESSAGE_LENGTH];
      int data = Serial.parseInt();
      Serial.println(data);
    }
  }
}






/////////////////////////// FUNCTIONS /////////////////////////////
//
//void parseStringTo4Ints(String* msg, int* intVal) {
//  *intVal = Serial.parseInt(*msg, ',');
//  return;
//}
