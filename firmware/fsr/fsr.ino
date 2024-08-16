int fsrPins[] = {A0, A1, A2, A3, A4, A5};
int numFSRs = 4; // will be set over serial connection

int delayTime = 16;  // in ms, calculated based on publishRate

int fsrValue = 0;

void setup() { 
  Serial.begin(115200);
} 
void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');

    // Process the input
    if (input.startsWith("INIT,")) {
      processInitMessage(input);
    } else {
      Serial.println("ERROR,Invalid Command");
    }
  }

  
  
  for (int i = 0; i < numFSRs; i++) {
    fsrValue = analogRead(fsrPins[i]);
    // Print the value in the format "FSR,i,value"
    Serial.print("FSR,");
    Serial.print(i);
    Serial.print(",");
    Serial.println(fsrValue);
  }
  delay(delayTime);
}

void processInitMessage(String input) {
  // Expected format: "INIT,numSensors,publishRate"
  int firstComma = input.indexOf(',');
  int secondComma = input.indexOf(',', firstComma + 1);

  if (firstComma > 0 && secondComma > firstComma) {
    // Extract and convert the parameters
    int tempNumFSRs = input.substring(firstComma + 1, secondComma).toInt();
    int tempPublishRate = input.substring(secondComma + 1).toInt();

    // Validate the parameters
    if (tempNumFSRs > 0 && tempNumFSRs <= 6 && tempPublishRate > 0 && tempPublishRate <= 120) {
      
      delayTime = 1000 / tempPublishRate;  // Update delay time based on the new publish rate

      // Confirm initialization
      Serial.println("INIT,OK");
      numFSRs = tempNumFSRs;
    } else {
      Serial.println("ERROR,Invalid parameters");
    }
  } else {
    Serial.println("ERROR,Invalid INIT format");
  }
}
