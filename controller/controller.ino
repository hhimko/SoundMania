/* IO PINS */
#define BTN1 10
#define BTN2 11

/* CONTROLLER STATES */
bool BTN1Down = false;
bool BTN2Down = false;


void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  
  pinMode(BTN1, INPUT_PULLUP);
  pinMode(BTN2, INPUT_PULLUP);

  // initialize serial communication at 9600 bits per second
  Serial.begin(115200);

  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB
  }

}

void loop() {
  if (!digitalRead(BTN1) ^ BTN1Down) {
    Serial.write((byte)0);
    BTN1Down = !BTN1Down;
  }

  if (!digitalRead(BTN2) ^ BTN2Down) {
    Serial.write((byte)1);
    BTN2Down = !BTN2Down;
  }
}

// serialEvent() is automatically run at the end of loop()
void serialEvent() {
  while (Serial.available() > 0) {
    char recv = Serial.read();
    
    if (recv){
      digitalWrite(LED_BUILTIN, LOW);
    }
    else{
      digitalWrite(LED_BUILTIN, HIGH);
    }
  }
}
