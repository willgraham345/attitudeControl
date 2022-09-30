const int M1_pin = 3; // IN_1a
const int M2_pin = 4; // IN_3a
const int M3_pin = 5; // IN_1b
const int M4_pin = 6; // IN_3b
const byte numChars = 32;
char receivedChars[numChars];
char tempChars[numChars];        // temporary array for use when parsing

const byte numBytes = 8;
byte receivedBytes[numBytes];
byte numReceived = 0;

boolean newData = false;
void setup() {
  Serial.begin(115200);
//  Serial.println
}
void loop(){
  parseString();
}
void parseString(){
  if (!Serial.available()){
    String rs = Serial.readString();
    Serial.print("Arduino is getting: ");
    Serial.println();
    
  }
}
//void setup() {
//    Serial.begin(115200);
//    Serial.println("<Arduino is ready>");
//}
//
//void loop() {
//    recvBytesWithStartEndMarkers();
//    showNewData();
//}
//
//void recvBytesWithStartEndMarkers() {
//    static boolean recvInProgress = false;
//    static byte ndx = 0;
//    char startMarker = 's';
//    char endMarker = 'e';
//    byte rb;
//   
//
//    while (Serial.available() > 0 && newData == false) {
//        rb = Serial.read();
//
//        if (recvInProgress == true) {
//            if (rb != endMarker) {
//                receivedBytes[ndx] = rb;
//                ndx++;
//                if (ndx >= numBytes) {
//                    ndx = numBytes - 1;
//                }
//            }
//            else {
//                receivedBytes[ndx] = '\0'; // terminate the string
//                recvInProgress = false;
//                numReceived = ndx;  // save the number for use when printing
//                ndx = 0;
//                newData = true;
//            }
//        }
//
//        else if (rb == startMarker) {
//            recvInProgress = true;
//        }
//    }
//}
//
//void showNewData() {
//    if (newData == true) {
////        Serial.print("This just in (HEX values)... ");
////        for (byte n = 0; n < numReceived; n++) {
////            Serial.print(receivedBytes[n], HEX);
////            Serial.print(' ');
////        }
////        Serial.println();
//
//        Serial.print("This is what Arduino Received: ");
//        
//        int sizeNum = sizeof(receivedBytes);
//        Serial.print(sizeNum);
//        String myString = String(receivedBytes);
//        myString.strip();
//        Serial.print(' ');
//        Serial.print(myString);
//        Serial.println();
//        
//        newData = false;
//    }
//}
