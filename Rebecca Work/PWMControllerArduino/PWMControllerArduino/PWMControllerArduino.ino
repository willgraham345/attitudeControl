#include <MKRMotorCarrier.h>

//Variable to store the battery voltage
static int batteryVoltage;

//Variable to change the motor speed and direction
float duty = 100;
float freq = 200;
float period = (1/freq)*1000000;// convert seconds to uS
int start_time = 0;
int elapsed_time = 0;
float time_on = period;
float time_off = 0;
bool ON = true;
bool EDGE = true; // starts with 100% duty wich is the edge technically



void setup() 
{
  //Serial port initialization
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
  M1.setDuty(100);
}

void loop() {
//  float test_end;
//  float test_time = micros();
  if (Serial.available()>0){
    
//    String raw_msg = Serial.readStringUntil('\n');
        // Split the string into substrings
 
    String duty_str = Serial.readStringUntil('\n');

    duty = duty_str.toFloat();
    time_on = period*(duty/100);
    time_off = period - time_on;
    start_time = micros();
   // Serial.println("Period: " + String(period) + ", Time on: " + String(time_on));
   
    if (!ON & (duty == 100)){
      M1.setDuty(100);
      ON = true;
      EDGE = true;
    }else if (ON & (duty == 0)){
      M1.setDuty(0);
      ON = false;
      EDGE = true;
    }else{
      EDGE = false;
    }
  }
  if(!EDGE){ // if not a solid on or off, execute timing
    elapsed_time = micros()-start_time;
    if(ON & (elapsed_time >= time_on)){
      //finished being on
      // turn off
      M1.setDuty(0);
      ON = false;
      start_time = micros();
    }else if(!ON & (elapsed_time >= time_off)){
      M1.setDuty(100);
      ON = true;
      start_time = micros();
    }
  }//takes about 9 micro seconds to execute loop
//  test_end = micros() - test_time;
//  Serial.println(test_end);
}
