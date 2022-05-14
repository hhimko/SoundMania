#define BUTTON_COUNT 4
#define KNOB_COUNT 2


/* +=======================+ .:: BUTTONS ::.  +=======================+ */
class Button
{
  private:
    uint8_t m_GPIO;
    bool m_prevState = HIGH;
    unsigned long m_pressTime = 0;
    static const unsigned long m_debounceDelay = 2; // delay in ms
    
  public:
    Button(uint8_t gpio)
      : m_GPIO(gpio) {}

    uint8_t getPin()
    {
      return m_GPIO;
    }

    bool isPressed()
    {
      return debounce();
    }

  private:
    bool debounce() 
    {
      bool currState = digitalRead(m_GPIO);
      
      if (m_prevState == HIGH){ 
        if (currState == LOW) {
          m_prevState = LOW;
          m_pressTime = millis();
        }
      } else {
        if (currState == LOW) {
          if (millis() - m_pressTime >= m_debounceDelay)
            return true;
        } else {
          m_prevState = HIGH;
        }
      }
      return false;
    }
};

Button g_buttons[BUTTON_COUNT] = {13, 12, 11, 10}; // buttons[0] should be defined as the leftmost button on the controller
byte g_buttonStates = 0b0000; // each bit corresponds to a single button state


/* +=======================+ .:: KNOBS ::.  +=======================+ */
class Knob 
{
  
};

Knob g_Knobs[KNOB_COUNT] = {};
byte g_KnobStates = 0b0;


/* +=======================+ .:: PROGRAM ::.  +=======================+ */
void setup() 
{
  for (auto button : g_buttons)
    pinMode(button.getPin(), INPUT_PULLUP);
    
  // initialize serial communication at 115200 bits per second
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB
  }
}


void loop() 
{  
  if (readButtonStates(g_buttonStates))
    sendButtonPacket(g_buttonStates); // send packet when the state has chaged
}


bool readButtonStates(byte& state)
/*
    Read the current controller's buttons states into a byte reference.
    Individual bits in the byte represent the consecutive button states, where a binary 1 stands for the button being pressed. 

    If the read sequence differs from the passed reference, the function returns a boolean true, false otherwise.
    This enables the program to send the button packets only if a change of state has occured. 
*/
{
  byte prevState = state;

  for (int i = BUTTON_COUNT-1; i >= 0; --i){
    bool pressed = g_buttons[i].isPressed();
    state = (state & ~(0b1 << i)) | (pressed << i); // set the appropriate bit
  }

  return state ^ prevState; // this will return 0 only when the states are equal
}


void sendButtonPacket(byte state)
/*
    Send the passed buttons state as a packet to the serial port. 

    The button packet should always contain a binary 0 as the MSB,
    so a maximum of 7 button states can be registered.
*/
{
  Serial.write(0b00000000 + state & 0b01111111);
}


bool readKnobState()
{
  return false;
}


void sendKnobPacket(byte state)
/*
    Send the passed knobs state as a packet to the serial port. 

    The knob packet should always contain a binary 1 as the MSB.
*/
{
  Serial.write(0b10000000 + state & 0b01111111);
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
