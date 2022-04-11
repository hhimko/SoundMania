/* IO PINS */
#define BUTTON_COUNT 4
byte BUTTON_PINS[BUTTON_COUNT] = {10, 11, 12, 13}; // BUTTON_PINS[0] should be defined as the leftmost button on the controller

/* CONTROLLER STATES */
byte buttonState = 0b0000; // each bit corresponds to a single button state
byte knobState   = 0b0;


void setup() {

  for (auto bp : BUTTON_PINS)
    pinMode(bp, INPUT_PULLUP);

  // initialize serial communication at 9600 bits per second
  Serial.begin(115200);

  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB
  }

}

void loop() {
  
  if (readButtonState(buttonState))
    sendButtonPacket(buttonState); // send packet only if the state has chaged

}

bool readButtonState(byte& state){
  byte previous_state = state;

  for (int i=BUTTON_COUNT-1; i >= 0; --i){
    bool pin = !digitalRead(BUTTON_PINS[i]); // boolean value is negated here because of the INPUT_PULLUP mode

    if (pin ^ ((state >> i) & 0b1)){
      byte new_state = (state & ~(0b1 << i)) | (pin << i); // set the appropriate bit
      state = new_state;
    }
    
  }

  return state ^ previous_state; // this will return 0 only when the states are equal
}

void sendButtonPacket(byte state){
  Serial.write(0b00000000 + state);
}

void sendKnobPacket(byte state){
  Serial.write(0b10000000 + state);
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
