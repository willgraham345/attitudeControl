const int PWM_signal = 50;
long startTime;
const int IN1 = 1;
const int IN2 = 2;
const int IN3 = 3;
const int IN4 = 4;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.print(millis());

}

void loop() {
  // put your main code here, to run repeatedly:
  if(millis() - startTime < 3000){
    analogWrite(IN1, PWM_signal);
    analogWrite(IN2, PWM_signal);
    analogWrite(IN3, PWM_signal);
    analogWrite(IN4, PWM_signal);
  }
  
  

}
