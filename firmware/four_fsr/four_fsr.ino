int fsrPins[] = {A0, A1, A2, A3};
int fsrValue = 0;

byte i = 0;

void setup() { 
  Serial.begin(115200);
} 
void loop() {
  // force sensitive resistors. Only send data once every 8 loops
  if (i == 0) {
    for (int k = 0; k < 4; k++) {
      fsrValue = analogRead(fsrPins[k]);
      // Print the value in the format "FSR,i,value"
      Serial.print("FSR,");
      Serial.print(k);
      Serial.print(",");
      Serial.println(fsrValue);
    }
  }

  // increment counter
  i++;
  if (i >= 8) {
    i = 0;
  }
}
