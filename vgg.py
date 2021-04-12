import tensorflow as tf
from keras import backend as K
from sklearn.datasets import fetch_lfw_people
from sklearn.model_selection import train_test_split
import numpy as np
import random
from euclidian_distance import euclidean_distance, tf_siamese_nn


lfw_people_train = fetch_lfw_people(color=True, resize=0.7)
print(len(lfw_people_train.images))

x_train, x_val, y_train, y_val = train_test_split(lfw_people_train.images[:], lfw_people_train.target[:],
                                                  test_size=0.33)


def create_pairs(images, labels):
    # initialize two empty lists to hold the (image, image) pairs and
    # labels to indicate if a pair is positive or negative
    random.seed(2021)
    pairImages = []
    pairLabels = []

    # calculate the total number of classes present in the dataset
    # and then build a list of indexes for each class label that
    # provides the indexes for all examples with a given label
    numClasses = len(np.unique(y_val))
    classes = np.unique(y_val)
    idx = [np.where(y_val == classes[i]) for i in range(0, numClasses)]

    # loop over all images
    for idxA in range(len(images)):
        # grab the current image and label belonging to the current iteration
        currentImage = images[idxA]
        label = labels[idxA]

        # randomly pick an image that belongs to the same class
        # label
        posId = random.choice(list(np.where(labels == label)))
        posIdx = random.choice(posId)
        posImage = images[posIdx]

        # prepare a positive pair and update the images and labels
        pairImages.append([currentImage, posImage])
        pairLabels.append([1])

        # grab the indices for each of the class labels not equal to
        # the current label and randomly pick an image corresponding
        # to a label not equal to the current label
        negId = random.choice(list(np.where(labels != label)))
        negIdx = random.choice(negId)
        negImage = images[negIdx]

        # prepare a negative pair of images and update our lists
        pairImages.append([currentImage, negImage])
        pairLabels.append([0])

    return (np.array(pairImages), np.array(pairLabels))


(pairTrain, labelTrain) = create_pairs(x_train, y_train)
(pairTest, labelTest) = create_pairs(x_val, y_val)

img1 = tf.keras.layers.Input(shape=lfw_people_train.images[0].shape)
img2 = tf.keras.layers.Input(shape=lfw_people_train.images[0].shape)

featureExtractor = tf_siamese_nn(lfw_people_train.images[0].shape, fineTune=True)

featsA = featureExtractor(img1)
featsB = featureExtractor(img2)

distance = tf.keras.layers.Lambda(euclidean_distance)([featsA, featsB])

outputs = tf.keras.layers.Dense(1, activation="sigmoid")(distance)
model = tf.keras.Model(inputs=[img1, img2], outputs=outputs)

model.summary()

serena = []
for i in range(0, len(lfw_people_train.images)):
    if lfw_people_train.target[i] == 4963:
        serena.append(lfw_people_train.images[i])

print(type(serena))
print(type(lfw_people_train.images))
serena_array = np.asarray(serena)
print(type(serena_array))
def contrastive_loss(y, preds, margin=1):
    # explicitly cast the true class label data type to the predicted
    # class label data type
    y = tf.cast(y, preds.dtype)
    # calculate the contrastive loss between the true labels and
    # the predicted labels
    squaredPreds = K.square(preds)
    squaredMargin = K.square(K.maximum(margin - preds, 0))
    loss = 1 - K.mean(y * squaredPreds + (1 - y) * squaredMargin)
    return loss

save_best_model = tf.keras.callbacks.ModelCheckpoint(
    filepath="best_model.h5",
    monitor="val_accuracy",
    verbose=1,
    save_best_only=True,
    mode="max",
    save_freq="epoch"
)

adam_optimizer = tf.keras.optimizers.Adam(
    learning_rate=0.1
)

reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
    patience=4,
    factor=0.9,
    min_lr=0.001,
    verbose=1
)

model.compile(loss="binary_crossentropy", optimizer=adam_optimizer, metrics=["accuracy"])
# train the model
history = model.fit([pairTrain[:, 0], pairTrain[:, 1]], labelTrain[:],
                    validation_data=([pairTest[:, 0], pairTest[:, 1]], labelTest[:]), batch_size=128, epochs=100, callbacks=[save_best_model, reduce_lr])

#print(model.predict([serena_array[:20], serena_array[20:40]]))
#print(model.predict([serena_array[:20], serena_array[:20]]))

model.save("modelino.h5")