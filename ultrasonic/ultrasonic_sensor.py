#Libraries
import RPi.GPIO as GPIO
import time
from picamera import PiCamera
from time import sleep
import cv2
from haar import return_cropped_face
import tensorflow as tf
import numpy as np
from send import send_message
from upload_to_drive import upload_image


#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

interpreter = tf.lite.Interpreter("model.tflite")

interpreter.allocate_tensors()
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    camera = PiCamera()
    try:
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            if(dist<=80):
                camera.capture('/home/pi/Desktop/try.jpg')
                img = cv2.imread('/home/pi/Desktop/try.jpg')
                return_cropped_face(img)
                
                input1 = []
                img1 = cv2.imread("sexy.png")
                img1 = img1.astype(np.float32)
                input1.append(img1)
                input_array1 = np.asarray(input1)
                
                input2 = []
                img2 = cv2.imread("buni1.png")
                img2 = img2.astype(np.float32)
                input2.append(img2)
                input_array2 = np.asarray(input2)
                interpreter.set_tensor(0,input_array1)
                interpreter.set_tensor(1,input_array2)

                interpreter.invoke()
                output = interpreter.get_tensor(interpreter.get_output_details()[0]["index"])
                print("Prediction: ")
                print(output)
                if output<0.75:
                    upload_image()
                    send_message()
                
                break
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()