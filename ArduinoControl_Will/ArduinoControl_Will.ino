//zoomkat 11-12-13 String capture and parsing
//from serial port input (via serial monitor)
//and print result out serial port
//copy test strings and use ctrl/v to paste in
//serial monitor if desired
// * is used as the data string delimiter
// , is used to delimit individual data

String msgReceived; //main captured String
const int max_msg_len = 3;
//const char delim ;
long unsigned int a, b, c, d;
int ind1; // , locations
int ind2;
int ind3;
int ind4;

const int M1_pin = 3; const int M2_pin = 5; const int M3_pin = 6; const int M4_pin = 9;


void setup() {
  Serial.begin(115200);
  Serial.println("Arduino ready");
}

void loop() {
  if (Serial.available() == 0) {
    // do nothing
  }

  if (Serial.available())  {
    a, b, c, d = parsingString();
    
    
  }
  analogWrite(M1_pin, a);
  analogWrite(M2_pin, b);
  analogWrite(M3_pin, c);
  analogWrite(M4_pin,d);
//  Serial.print("d = "); Serial.println(d);
}

int parsingString(){
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

      return a, b, c, d;




      //      Serial.print(M[0]); Serial.print(', '); Serial.print(M[1]);Serial.print(', ');
      //      Serial.print(M[2]); Serial.pritn(', '); Serial.println(M[3])
    }


    else {
      msgReceived += c; //makes the string msgReceived
    }
}
