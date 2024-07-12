int fsrPins[] = {A0, A1, A2};
int fsrValue = 0;

int piezoPins[] = {A3, A4, A5};
int piezoValue = 0;

void setup() { 
  Serial.begin(115200);
} 
void loop() {
  // force sensitive resistors 
  for (int i = 0; i < 3; i++) {
    fsrValue = analogRead(fsrPins[i]);
    // Print the value in the format "FSR,i,value"
    Serial.print("FSR,");
    Serial.print(i);
    Serial.print(",");
    Serial.println(fsrValue);
  }

  // piezoelectric sensors
  for (int i = 0; i < 3; i++) {
    piezoValue = analogRead(piezoPins[i]);
    // Print the value in the format "PZ,i,value"
    Serial.print("PZ,");
    Serial.print(i);
    Serial.print(",");
    Serial.println(piezoValue);
  }
}
