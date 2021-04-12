import tensorflow as tf
import numpy as np
from sklearn.datasets import fetch_lfw_people
import cv2

model = tf.keras.models.load_model("best_model.h5", custom_objects={"euclidean_distance": euclidean_distance,
                                                                  "tf_siamese_nn":tf_siamese_nn})
model.summary()

input1 = []
input2 = []

img1 = cv2.imread("crop.png")
img2 = cv2.imread("crop2.png")

input1.append(img1)
input2.append(img2)

input_array1 = np.asarray(input1)
input_array2 = np.asarray(input2)


print("Prediction")
print(model.predict([input_array1[:1], input_array2[:1]]))
