/*
  Single speaker bridge mode

  Wiring:
  Speaker terminal 1 = Pin 9
  Speaker terminal 2 = Pin 10

  Do not connect the speaker to GND.
*/

#define SPK_A 9
#define SPK_B 10

void setup() {
  Serial.begin(115200);

  pinMode(SPK_A, OUTPUT);
  pinMode(SPK_B, OUTPUT);

  // Timer1 PWM ~31kHz
  TCCR1B = (TCCR1B & 0b11111000) | 0x01;

  OCR1A = 128;
  OCR1B = 127;
}

void loop() {
  while (Serial.available()) {

    byte sample = Serial.read();

    OCR1A = sample;
    OCR1B = 255 - sample;
  }
}
