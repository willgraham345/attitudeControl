const int M1a_pin = 3; // IN_1
const int M1b_pin = 4; // IN_2
const int M2a_pin = 5; // IN_3
const int M2b_pin = 6; // IN_4
const int M3a_pin = 7; // IN_1
const int M3b_pin = 8; // IN_2
const int M4a_pin = 9; // IN_3
const int M4b_pin = 10; // IN_4
String msgReceived; //main captured String
const int max_msg_len = 3;
//const char delim ;
long unsigned int a = 0, b = 0, c = 0, d = 0;
int ind1; // , locations
int ind2;
int ind3;
int ind4;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.println("ready");
}

void loop() {
  // put your main code here, to run repeatedly:


  if (Serial.available() > 0)  {

    a, b, c, d = parsingString();
    //    analogWrite(M1a_pin, a);
    //    analogWrite(M1b_pin, 0);
    //    analogWrite(M2a_pin, b);
    //    analogWrite(M2b_pin, 0);
    //    analogWrite(M3a_pin, c);
    //    analogWrite(M3b_pin, 0);
    //    analogWrite(M4a_pin, d);
    //    analogWrite(M4b_pin, 0);


  }
  else {
    Serial.println("...");
    delay(1500);
  }

}










// Functions below //
/////////////////////////////////////////////////////////////////////////////////////////////////////////
int parsingString() {
  char c = Serial.read();  //gets one byte from serial buffer
  if (c == '\n') {
    ind1 = msgReceived.indexOf(',');  //finds location of first ,
    ind2 = msgReceived.indexOf(',', ind1 + 1 ); //finds location of second ,
    ind3 = msgReceived.indexOf(',', ind2 + 1 );
    ind4 = msgReceived.indexOf(',', ind3 + 1 );
    int indx[] = {ind1, ind2, ind3, ind4};

    String M1 = msgReceived.substring(0, ind1);   //captures first data String
    String M2 = msgReceived.substring(ind1 + 1, ind2); //captures second data String
    String M3 = msgReceived.substring(ind2 + 1, ind3);
    String M4 = msgReceived.substring(ind3 + 1); //captures remain part of data after last

    //      M = {M1.toInt(), M2.toInt(), M3.toInt(), M4.toInt()};
    a = M1.toInt(); b = M2.toInt(); c = M3.toInt(); d = M4.toInt();
    Serial.println(msgReceived);
    msgReceived = "";
    Serial.println(M1 + M2 + M3 + M4);
    Serial.println(msgReceived);

    Serial.print("Wrote the following to pins: ");
    Serial.print(a + 1); Serial.print(", ");
    Serial.print(b + 1); Serial.print(", ");
    Serial.print(c + 1); Serial.print(", ");
    Serial.print(d + 1); Serial.print(", ");
    return a, b, c, d;




    //      Serial.print(M[0]); Serial.print(', '); Serial.print(M[1]);Serial.print(', ');
    //      Serial.print(M[2]); Serial.pritn(', '); Serial.println(M[3])
  }


  else {
    msgReceived += c; //makes the string msgReceived
  }
}
