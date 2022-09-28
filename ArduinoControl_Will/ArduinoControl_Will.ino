int M1_pin = 1;
int M2_pin = 2;
int M3_pin = 3;
int M4_pin = 4;

int data[4];
int data2[4];
char userInput;
const char *delimiter = ",";
char *token;

char commandReceive;
void setup() {
  Serial.begin(115200);

}

void loop() {
  // put your main code here, to run repeatedly:
  while(Serial.available() ==0){
    
  }
  if (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      
    }
    else {
      commandReceive += c;
    }

  }
//  parseCommand(commandReceive);
}



void parseCommand(char com) {
  char M1; char M2; char M3;
  token = strtok(com, delimiter);
  M1 = token[1];
  M2 = token[2];
  M3 = token[3];
  Serial.print("m1 vals");
  Serial.println(M1);
  Serial.print("m2 vals");
  Serial.println(M2);
  Serial.print("m3 vals");
  Serial.println(M3);


}
