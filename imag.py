import tensorflow as tf
import numpy as np
import cv2

interpreter = tf.lite.Interpreter("model.tflite")

interpreter.allocate_tensors()


input1 = []
input2 = []

img1 = cv2.imread("test1.png")
img2 = cv2.imread("test2.png")

img1 = img1.astype(np.float32)
img2 = img2.astype(np.float32)

input1.append(img1)
input2.append(img2)

input_array1 = np.asarray(input1)
input_array2 = np.asarray(input2)

interpreter.set_tensor(0,input_array1)
interpreter.set_tensor(1,input_array2)

interpreter.invoke()
output = interpreter.get_tensor(interpreter.get_output_details()[0]["index"])
print("Prediction: ")
print(output)

