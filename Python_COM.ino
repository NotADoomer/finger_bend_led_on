int x; // Переменная для коммуникации с питон программой
void setup() {
 Serial.begin(9600);
 Serial.setTimeout(1);
 
 for (int j = 0; j <= 4; j++){ //В цикле инициализируем пины от  3 до 8-го  и выключаем их
  pinMode(j+3, OUTPUT);
  digitalWrite(j+3, LOW);
 }
 
}
void loop() {
 while (!Serial.available()); //Если есть что то последовательном порте
 x = Serial.readString().toInt(); //Читаем это и переводим в инт
 
 for (int i = 0; i <= 4; i++){ //Цикл для проверки сигнала в переменной x
  if (x == i){ 
     digitalWrite(i+3, HIGH); //Если сигнал был от 0 до 4 то включить соответствующий светодиоды
  }
  else if (x == i+5){
     digitalWrite(i+3, LOW); //Если больше то выключить
  }
 }
}
