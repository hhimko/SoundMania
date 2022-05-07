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
  /*
      Read the current controller's buttons states into a byte reference.
      Individual bits in the byte represent the consecutive button states, where a binary 1 stands for the button being pressed. 

      If the read sequence differs from the passed reference, the function returns a boolean true, false otherwise.
      This enables the program to send the button packets only if a change of state has occured. 
  */
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
  /*
      Send the passed buttons state as a packet to the serial port. 

      The button packet should always contain a binary 0 as the MSB,
      so a maximum of 7 button states can be registered.
  */
  Serial.write(0b00000000 + state & 0b01111111);
}


void sendKnobPacket(byte state){
  /*
      Send the passed knobs state as a packet to the serial port. 

      The knob packet should always contain a binary 1 as the MSB.
  */
  Serial.write(0b10000000 + state & 0b01111111);
}


// serialEvent() is automatically run at the end of loop()
void serialEvent() { // TODO: recieve button colors and lcd commands (?)
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
