#include <Encoder.h>

#define BUTTON_COUNT 4
#define KNOB_COUNT 2


/* +=======================+ .:: BUTTONS ::.  +=======================+ */
class Button
{
public:
  Button(uint8_t pin)
    : mGPIO(pin) {}

  uint8_t getPin()
  {
    return mGPIO;
  }

  bool isPressed()
  {
    return debounce();
  }

private:
  uint8_t mGPIO;
  bool mPrevState = HIGH;
  unsigned long mPressTime = 0;
  static const unsigned long sDebounceDelay = 25; // delay in ms

private:
  bool debounce() 
  {
    bool currState = digitalRead(mGPIO);
    
    if (mPrevState == HIGH){ 
      if (currState == LOW) {
        mPrevState = LOW;
        mPressTime = millis();
      }
    } else {
      if (currState == LOW) {
        if (millis() - mPressTime >= sDebounceDelay)
          return true;
      } else {
        mPrevState = HIGH;
      }
    }
    return false;
  }
};

Button gButtons[BUTTON_COUNT] = {13, 12, 11, 10}; // buttons[0] should be defined as the leftmost button on the controller
uint8_t gButtonStates = 0b0000; // each bit corresponds to a single button state


/* +=======================+ .:: KNOBS ::.  +=======================+ */
class Knob 
{
public:
  Knob(uint8_t pinA, uint8_t pinB)
    : mGPIO_A(pinA), mGPIO_B(pinB), mEncoder{pinA, pinB} {}

  uint8_t getPinA()
  {
    return mGPIO_A;
  }

  uint8_t getPinB()
  {
    return mGPIO_B;
  }

  int32_t readAbsolute()
  {
    return mEncoder.read();
  }

  int32_t readRelative()
  {
    int32_t temp = mPrevReading;
    mPrevReading = readAbsolute();
    return mPrevReading - temp;
  }

private:
  uint8_t mGPIO_A;
  uint8_t mGPIO_B;
  Encoder mEncoder;
  int32_t mPrevReading = 0;
};

Knob gKnobL = {2, 4};
Knob gKnobR = {3, 5};


/* +=======================+ .:: PROGRAM ::.  +=======================+ */
void setup() 
{
  for (auto button : gButtons)
    pinMode(button.getPin(), INPUT_PULLUP);
    
  // initialize serial communication at 115200 bits per second
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB
  }
}


void loop() 
{  
  if (readButtonStates(gButtonStates))
    sendButtonPacket(gButtonStates);
    
  int32_t kl = gKnobL.readRelative();
  if (kl != 0)
    sendKnobPacket(kl, 0);
    
  int32_t kr = gKnobR.readRelative();
  if (kr != 0)
    sendKnobPacket(kr, 1);
}


bool readButtonStates(uint8_t& state)
/*
    Read the current controller's buttons states into a byte reference.
    Individual bits in the byte represent the consecutive button states, where a binary 1 stands for the button being pressed. 

    If the read sequence differs from the passed reference, the function returns a boolean true, false otherwise.
    This enables the program to send the button packets only if a change of state has occured. 
*/
{
  uint8_t prevState = state;

  for (int i = BUTTON_COUNT-1; i >= 0; --i){
    bool pressed = gButtons[i].isPressed();
    state = (state & ~(0b1 << i)) | (pressed << i); // set the appropriate bit
  }

  return state ^ prevState; // this will return 0 only when the states are equal
}


void sendButtonPacket(uint8_t state)
/*
    Send the passed buttons state as a packet to the serial port. 

    The button packet should always contain a binary 0 as the MSB,
    so a maximum of 7 button states can be registered.
*/
{
  Serial.write(0b00000000 + (state & 0b01111111));
}


void sendKnobPacket(int32_t state, bool id)
/*
    Send the relative knob state change as a packet to the serial port.
    The packet consists of a knob identifier (1 bit), sign of the change value (1 bit) and the integer value (5 bits).

    The knob packet should always contain a binary 1 as the MSB.
*/
{
  bool sgn = state < 0;
  uint32_t val = abs(state);
  
  Serial.write(0b10000000 + 0b01000000 * id + 0b00100000 * sgn + (val & 0b00011111));
}


//// serialEvent() is automatically run at the end of loop()
//void serialEvent() { // TODO: recieve button colors and lcd commands (?)
//  while (Serial.available() > 0) {
//    char recv = Serial.read();
//    
//    if (recv){
//      digitalWrite(LED_BUILTIN, LOW);
//    }
//    else{
//      digitalWrite(LED_BUILTIN, HIGH);
//    }
//  }
//}
