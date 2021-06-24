import tensorflow as tf
import numpy as np
import cv2
import os

interpreter = tf.lite.Interpreter("model.tflite")

interpreter.allocate_tensors()
input1 = []
img1 = cv2.imread("tati/tati1.png")
img1 = img1.astype(np.float32)
input1.append(img1)
input_array1 = np.asarray(input1)
directory = "buni"
for filename in os.listdir(directory):
    full_name =directory+"/"+filename
    input2 = []
    img2 = cv2.imread(full_name)
    img2 = img2.astype(np.float32)
    input2.append(img2)
    input_array2 = np.asarray(input2)
    interpreter.set_tensor(0,input_array1)
    interpreter.set_tensor(1,input_array2)

    interpreter.invoke()
    output = interpreter.get_tensor(interpreter.get_output_details()[0]["index"])
    print("Prediction: ")
    print(output)



