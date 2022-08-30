#include <MKRMotorCarrier.h>
#include "SAMDTimerInterrupt.h"


boolean EDGE = true;

#define HW_TIMER_INTERVAL_uS  50 //200Hz PWM desired
int on_cntr = 0;
int duty = 25;
SAMDTimer ITimer(TIMER_TC3);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  while (!Serial);

  //Establishing the communication with the motor shield
  if (controller.begin()) 
    {
      Serial.print("MKR Motor Shield connected, firmware version ");
      Serial.println(controller.getFWVersion());
    } 
  else 
    {
      Serial.println("Couldn't connect! Is the red led blinking? You may need to update the firmware with FWUpdater sketch");
      while (1);
    }

  // Reboot the motor controller; brings every value back to default
  Serial.println("reboot");
  controller.reboot();
  delay(500);

  // Interval in millisecs
  if (ITimer.attachInterruptInterval(HW_TIMER_INTERVAL_uS, TimerHandler))
  {
    Serial.print(F("Starting ITimer OK, millis() = ")); Serial.println(millis());
  }
  else{
    Serial.println(F("Can't set ITimer. Select another freq. or timer"));}

  M1.setDuty(100);

}


void loop() {
  String m1_duty_str;
  float m1_duty;
  // put your main code here, to run repeatedly:
  if (Serial.available()>0){
    m1_duty_str = Serial.readStringUntil('\n');
    m1_duty = m1_duty_str.toFloat();
    if (m1_duty == 100){
      EDGE = true;
      M1.setDuty(100);
    }else if(m1_duty == 0){
      EDGE = true;
      M1.setDuty(0);
    }else{
      EDGE = false;
      duty = m1_duty;
      }
//    Serial.println("Received: " + m1_duty_str);
  }
}




void TimerHandler()
{
  on_cntr++;
  if (!EDGE && (on_cntr == duty)){
    M1.setDuty(0); //filled time with being on, now turn off.
  }
  if (!EDGE && (on_cntr>=100)){
    M1.setDuty(100);
    on_cntr = 0;
  }
}
