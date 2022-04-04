void setup() {
  // initialize serial communication at 9600 bits per second
   Serial.begin(115200);

   while (!Serial) {
     ; // wait for serial port to connect. Needed for native USB
   }

   pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  
}

// serialEvent() is automatically run at the end of loop()
void serialEvent() {
  while (Serial.available()) {
    char recv = Serial.read();
    Serial.write(recv);
    if (recv){
      digitalWrite(LED_BUILTIN, LOW);
    }
    else{
      digitalWrite(LED_BUILTIN, HIGH);
    }
  }
}
