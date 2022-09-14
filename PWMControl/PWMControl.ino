//#include <AFMotor.h>
//#include <TimerInterrupt.h>

#include <avr/io.h>
#include <avr/interrupt.h>

//3~= 200 Hz total period
//6.25~= 100 Hz total period
unsigned int reload = 3;//want full wave at 200 Hz, therefore need timer frequency of 200*100 = 20,000. i.e. T=0.00005 S.
// Arduino clock speed is 16 MHz, timer1 has pre scalar of 256. therefore Timer 1 speed = 16MHz/256=62.5kHz
//pulse time = 1/62.5kHz = 16 us.
// reload = desired_T / 16us (in the case of 200 Hz thats 5e-5/16e-6 = 3.125


boolean EDGE = true;
volatile int on_cntr = 0;
int duty = 50;
int M1_pin = 1;
int M2_pin = 2;
int M3_pin = 3;
int M4_pin = 4;


boolean ON = true;

void setup() {
  // put your setup code here, to run once:

  Serial.begin(115200);
  pinMode(M1_pin, OUTPUT);
  pinMode(M2_pin, OUTPUT);
  pinMode(M3_pin, OUTPUT);
  pinMode(M4_pin, OUTPUT);

  cli();
  TCCR1A = 0;
  TCCR1B = 0;
  OCR1A = reload;
  TCCR1B = (1 << WGM12) | (1 << CS12);
  TIMSK1 = (1 << OCIE1A);
  sei();
  //Serial.println("TIMER1 Setup Finished.");
  digitalWrite(M1_pin, 1);
}


void loop() {
  String m1_duty_str;
  int m1_duty;
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    m1_duty_str = Serial.readStringUntil('\n');
    m1_duty = m1_duty_str.toInt();
    if (m1_duty == 100) {
      EDGE = true;
      digitalWrite(M1_pin, 1);
      ON = true;
    } else if (m1_duty == 0) {
      EDGE = true;
      ON = false;
      digitalWrite(M1_pin, 0);
    } else {
      EDGE = false;
      duty = m1_duty;

    }
    Serial.println("Received: " + m1_duty_str);
  }
  TimerHandler();
}

ISR(TIMER1_COMPA_vect)
{
  on_cntr++;
  //TimerHandler();
}

void TimerHandler()
{
  if (!EDGE && ON && (on_cntr >= duty)) {
    digitalWrite(M1_pin, 0);
    ON = false;

  }
  if (!EDGE && !ON && (on_cntr >= 100)) {
    digitalWrite(M1_pin, 1);
    ON = true;
    on_cntr = 0;
  }
}
