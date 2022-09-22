int M1_pin = 1;
int M2_pin = 2;
int M3_pin = 3;
int M4_pin = 4;

int data[4];
int data2[4];
char userInput;


void setup() {
  Serial.begin(115200);

}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 4) {
    for (int i = 0; i < 4; i++) {
      data[i] = Serial.read();
    }

    for (int i = 0; i < 4; i++) {
      data2[i] = data[i] + 1;
      Serial.print(i); 
      Serial.println(data2[i]);
    }
  }
}
