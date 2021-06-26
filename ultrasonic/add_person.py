from picamera import PiCamera
import cv2
from haar import return_cropped_face

text = input("Enter person's name:")
camera = PiCamera()
camera.capture('/home/pi/Desktop/new.jpg')
img = cv2.imread('/home/pi/Desktop/new.jpg')
return_cropped_face(img,"known_persons/"+text+".png")