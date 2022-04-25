from gpiozero import AngularServo

servo = AngularServo(11, min_angle = -45, max_angle = 45)

servo.value = 0