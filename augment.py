import numpy as np
import cv2
from sklearn.datasets import fetch_lfw_people
from sklearn.model_selection import train_test_split


def adjust_gamma(image, gamma=1.0):

   invGamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)]).astype("uint8")

   return cv2.LUT(image, table)


def gaussian_noise(image,mean,std):

   noisy_img = image+ np.random.normal(mean, std, image.shape)
   noisy_img_clipped = np.clip(noisy_img, 0, 255)
   return noisy_img_clipped


def augment_image(image):

    augmented_images = []
    # gama correction
    #for x in range(4):
    #    frame_gama = adjust_gamma(image, 0.35 * (x + 1))
    #    augmented_images.append(frame_gama)
    #    augmented_labels.append(label)

    # gaussian noise
    for x in range(3):
        frame_gauss = gaussian_noise(image, 0.5, 12 * (x + 1))
        augmented_images.append(frame_gauss)

    ksize = (5, 5)
    frame_blur = cv2.blur(image, ksize)
    augmented_images.append(frame_blur)

    return augmented_images


def augment_dataset(dataset, labels):
    augmented_data_images = []
    augmented_data_labels = []

    for index in range(0, len(dataset)):
        new_images = augment_image(dataset[index])
        for k in range(0,len(new_images)):
            augmented_data_images.append(new_images[k])
            augmented_data_labels.append(labels[index])

    augmented_data_images_array = np.asarray(augmented_data_images)
    augmented_data_labels_array = np.asarray(augmented_data_labels)
    print(len(augmented_data_images_array))
    print(len(augmented_data_labels_array))


    #np.append(dataset, augmented_data_images_array)
    #np.append(labels, augmented_data_labels_array)


lfw_people_train = fetch_lfw_people(color=True, resize=0.7)
print(len(lfw_people_train.images))

x_train, x_val, y_train, y_val = train_test_split(lfw_people_train.images[:], lfw_people_train.target[:],
                                                  test_size=0.33)

print(len(x_train))
print(len(y_train))
augment_dataset(x_train, y_train)
print(len(x_train))
print(len(y_train))
