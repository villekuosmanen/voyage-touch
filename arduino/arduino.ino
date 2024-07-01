int fsrPins[] = {A0, A1, A2};
int fsrValue = 0;

void setup() { 
  Serial.begin(115200);
} 
void loop() { 
  for (int i = 0; i < 3; i++) {
    fsrValue = analogRead(fsrPins[i]);  // Read the analog value from each FSR
    // Print the value in the format "FSR,i,value"
    Serial.print("FSR,");
    Serial.print(i);
    Serial.print(",");
    Serial.println(fsrValue);
  }
  delay(100);
}
