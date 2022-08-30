#include <MKRMotorCarrier.h>
#include "SAMDTimerInterrupt.h"
//#include "SAMD_ISR_Timer.h"

#define INTERRUPT_PIN 6


//Variable to change the motor speed and direction
float freq = 200; // operate time = 3 mS, release time = 2 mS 
float period = (1/freq);// convert seconds to mS
String m1_duty_str = "0";
String m2_duty_str = "0";
String m3_duty_str = "0";
String m4_duty_str = "0";
float m1_duty;
float m2_duty;
float m3_duty;
float m4_duty;
bool ON = true;
//#include "SAMDTimerInterrupt.h"
//#include "SAMD_ISR_Timer.h"

#define HW_TIMER_INTERVAL_MS      500

// Depending on the board, you can select SAMD21 Hardware Timer from TC3, TC4, TC5, TCC, TCC1 or TCC2
// SAMD51 Hardware Timer only TC3

// Init SAMD timer TIMER_TC3
//SAMDTimer ITimer(TIMER_TC3);//////////////////
//SAMD_ISR_Timer ISR_Timer;


//#define TIMER_INTERVAL_1S             1000

//void TimerHandler(void)
//{
//  ISR_Timer.run();
//}
void TimerHandler()
{
//  digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
//  Serial.println(F("G"));
M1.setDuty(ON * 100);
ON = !ON;
}
void setup() 
{
  
  //Serial port initialization
  Serial.begin(115200);
  //while (!Serial);
//  Serial.println("About to reboot controller");
  // Reboot the motor controller; brings every value back to default
//  controller.reboot();
//  delay(500);
//  Serial.println("Controller Rebooted, about to set pwm");
  //default should be fully open
//  M1.setDuty(100);
//  M2.setDuty(100);
//  M3.setDuty(100);
//  M4.setDuty(100);


Serial.println("Test");
  
//  pinMode(LED_BUILTIN,  OUTPUT);
  
  // Interval in millisecs
//  if (ITimer.attachInterruptInterval_MS(HW_TIMER_INTERVAL_MS, TimerHandler))
//  {
//    Serial.print(F("Starting ITimer OK, millis() = ")); Serial.println(millis());
//  }
//  else
//    Serial.println(F("Can't set ITimer. Select another freq. or timer"));
  
//  ISR_Timer.setInterval(TIMER_INTERVAL_1S,  doingSomething1);
}

void loop() {
//  if (Serial.available()>0){
//    m1_duty_str = Serial.read();
//    m2_duty_str = Serial.read();
//    m3_duty_str = Serial.read();
//    m4_duty_str = Serial.read();
//    m1_duty = m1_duty_str.toFloat();
//    m2_duty = m2_duty_str.toFloat();
//    m3_duty = m3_duty_str.toFloat();
//    m4_duty = m4_duty_str.toFloat();
//    Serial.println("M1: " + String(m1_duty) + " M2: " + String(m2_duty) + " M3: " + String(m3_duty) + " M4: " + String(m4_duty));
    //M1.setDuty(m1_duty);
//    M2.setDuty(m2_duty);
//    M3.setDuty(m3_duty);
//    M4.setDuty(m4_duty);
//  }
}
