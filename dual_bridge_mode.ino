/*
  Two speakers in bridge mode

  Speaker 1:
    Pin 9  = Speaker = Pin 10

  Speaker 2:
    Pin 3  = Speaker = Pin 11

  Do not connect either speaker to GND.
*/

#define SPK1_A 9
#define SPK1_B 10

#define SPK2_A 3
#define SPK2_B 11

void setup() {

  Serial.begin(115200);

  pinMode(SPK1_A, OUTPUT);
  pinMode(SPK1_B, OUTPUT);

  pinMode(SPK2_A, OUTPUT);
  pinMode(SPK2_B, OUTPUT);

  // Timer1 -> Pins 9,10
  TCCR1B = (TCCR1B & 0b11111000) | 0x01;

  // Timer2 -> Pins 3,11
  TCCR2B = (TCCR2B & 0b11111000) | 0x01;

  OCR1A = 128;
  OCR1B = 127;

  OCR2A = 127;
  OCR2B = 128;
}

void loop() {

  while (Serial.available()) {

    byte sample = Serial.read();
    byte inverted = 255 - sample;

    // Speaker 1
    OCR1A = sample;
    OCR1B = inverted;

    // Speaker 2
    OCR2B = sample;
    OCR2A = inverted;
  }
}
