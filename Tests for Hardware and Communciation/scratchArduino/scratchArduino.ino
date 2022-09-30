const int IN1_p = 6;
const int IN2_p = 9;
const int IN3_p = 5;
const int IN4_p = 3;

int PWM = 50;
String msg = "000,000,000,000"
// void setup() {
//   // put your setup code here, to run once:
//   Serial.begin(9600);

// }

// void loop() {
//   // put your main code here, to run repeatedly:
//   analogWrite(IN1_p, PWM);
//   analogWrite(IN2_p, 0);
//   analogWrite(IN3_p, PWM);
//   analogWrite(IN4_p, 0);
// }

for
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
    msgReceived = '';

    return a, b, c, d;




    //      Serial.print(M[0]); Serial.print(', '); Serial.print(M[1]);Serial.print(', ');
    //      Serial.print(M[2]); Serial.pritn(', '); Serial.println(M[3])
  }


  else {
    msgReceived += c; //makes the string msgReceived
  }