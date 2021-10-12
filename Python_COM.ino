int x; 
void setup() {
 Serial.begin(9600);
 Serial.setTimeout(1);
 
 for (int j = 0; j <= 4; j++){ 
  pinMode(j+3, OUTPUT);
  digitalWrite(j+3, LOW);
 }
 
}
void loop() {
 while (!Serial.available()); 
 x = Serial.readString().toInt(); 
 
 for (int i = 0; i <= 4; i++){ 
  if (x == i){ 
     digitalWrite(i+3, HIGH);
  }
  else if (x == i+5){
     digitalWrite(i+3, LOW);
  }
 }
}
