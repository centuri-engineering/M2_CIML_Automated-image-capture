#define EN 8 /* enable pin for all stepper outputs*/
#define X_DIR 5 /* direction-pin for X-axis */
#define X_STEP 2 /* step-pin for X-axis */
#define Y_DIR 6 /* direction-pin for Y-axis*/
#define Y_STEP 3 /* step-pin for Y-axis */
#define Z_DIR 7 /* direction-pin for Z-axis */
#define Z_STEP 4 /* step-pin for Z-axis */
#define A_DIR 13 /*direction-pin for A-axis */
#define A_STEP 12 /* step-pin for A-axis */
int Count = 0; /* counter to count number of steps made */
boolean Direction = LOW; /* ratational direction of stepper motors*/

void setup() {
  Serial.begin(9600); /* configure the stepper drive pins as outputs */
  pinMode(EN, OUTPUT);
  pinMode(X_DIR, OUTPUT);
  pinMode(X_STEP, OUTPUT);
  pinMode(Y_DIR, OUTPUT);
  pinMode(Y_STEP, OUTPUT);
  pinMode(Z_DIR, OUTPUT);
  pinMode(Z_STEP, OUTPUT);
  pinMode(A_DIR, OUTPUT);
  pinMode(A_STEP, OUTPUT);
  digitalWrite(EN, LOW); //low to enable
}

void loop()
{
  /* count one step */
  Count++;
  /* if reached 500 steps then change the stepper direction and reset the  counter*/
  if (Count >= 500)
  {
    Direction = !Direction;
    digitalWrite(X_DIR, Direction); // Low = CW
    digitalWrite(Y_DIR, Direction); // Low = CW
    digitalWrite(Z_DIR, Direction); // Low = CW
    digitalWrite(A_DIR, Direction); // Low = CW
    Count = 0;
  }
  /* Step the X, Y, Z, and A Motoren */
  digitalWrite(X_STEP, HIGH);
  delay(1);
  digitalWrite(Y_STEP, HIGH);
  delay(1);
  digitalWrite(Z_STEP, HIGH);
  delay(1);
  digitalWrite(A_STEP, HIGH);
  delay(1);
  digitalWrite(X_STEP, LOW);
  delay(1);
  digitalWrite(Y_STEP, LOW);
  delay(1);
  digitalWrite(Z_STEP, LOW);
  delay(1);
  digitalWrite(A_STEP, LOW);
  delay(1);
}
