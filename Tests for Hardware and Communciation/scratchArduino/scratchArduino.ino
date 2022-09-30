// Serial Commuincation Protocol
/////////////////////////// GLOBAL VARIABLES /////////////////////////////

int intArray[4] = {};
int *p;
//*p = &intArray;


void setup() {
  // put your setup code here, to run once: 
  Serial.begin(115200);
  Serial.print("*p = "); Serial.println(*p);
  Serial.print("p = "); Serial.println(p);

}

void loop() {
  

}


//}





/////////////////////////// FUNCTIONS /////////////////////////////
