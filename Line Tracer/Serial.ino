#include <SoftwareSerial.h>
#include <AFMotor.h>
             
AF_DCMotor motor_R(3); 
AF_DCMotor motor_L(4); 

String Speed;
char  LorR;
int  i, s;

char DataToRead[6]; // 라즈베리로부터의 통신 읽어 저장할 배열

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); // 씨리얼!
  
  // 모터 전부 스탑
  motor_L.setSpeed(0);              
  motor_L.run(RELEASE);
  motor_R.setSpeed(0);                 
  motor_R.run(RELEASE);
}

void loop() {  
  
  DataToRead[5] = '\n';
  // 마지막을 \n으로
  Serial.readBytesUntil(char(13), DataToRead, 5);
  // 시리얼 통신 읽어들이기

  LorR = DataToRead[0]; // 방향 가져오기
  Speed = ""; // 스피드 초기화
  for (i = 1; (DataToRead[i] != '\n') && (i < 6); i++) {
    Speed += DataToRead[i]; // 스피드 값 읽기
  }
  s = Speed.toInt(); // 스피드 값 정수로 변환
  if (LorR == 'L') {  // 왼쪽 모터 움직이기
    motor_L.setSpeed(s);
    motor_R.setSpeed(0);
    motor_L.run(FORWARD);
    motor_R.run(FORWARD);
  }
  else if (LorR == 'R') { // 오른쪽 모터 움직이기
    motor_L.setSpeed(0);
    motor_R.setSpeed(s);
    motor_L.run(FORWARD);
    motor_R.run(FORWARD);
  }
  else if (LorR == 'F') { // 직진하기
    motor_L.setSpeed(s);
    motor_R.setSpeed(s);
    motor_L.run(FORWARD);
    motor_R.run(FORWARD); 
  }
  else if (LorR == 'A') { // 왼쪽 모터는 뒤로, 오른쪽 모터는 앞으로 ( 오른쪽 모터 앞으로 가기의 극대화)
    motor_L.setSpeed(s);
    motor_R.setSpeed(s);
    motor_L.run(BACKWARD);
    motor_R.run(FORWARD); 
  }
  else if (LorR == 'B') { // 오른쪽 모터는 뒤로, 왼쪽 모터는 앞으로 ( 왼 모터 앞으로 가기의 극대화)
    motor_L.setSpeed(s);
    motor_R.setSpeed(s);
    motor_L.run(FORWARD);
    motor_R.run(BACKWARD); 
  }
  
  else if (LorR == 'H') { // Hㅜ진
    motor_L.setSpeed(s);
    motor_R.setSpeed(s);
    motor_L.run(BACKWARD);
    motor_R.run(BACKWARD); 
  }

  delay(100);
  delay(100);
  // 0.2초간 움직임
  motor_L.run(RELEASE);
  motor_R.run(RELEASE);
  // 이후 멈춤
  Serial.println("AAAAAAAAAAAA");
  // 모든 행동이 끝난 뒤 시리얼로 문자 보냄.
}
