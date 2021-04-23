import cv2


def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized


# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# Read the input image
img = cv2.imread('test4.jpg')

img = image_resize(img, 400, 400)
# Convert into grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Detect faces
faces = face_cascade.detectMultiScale(gray, 1.1, 10)
# Draw rectangle around the faces
for (x, y, w, h) in faces:
    crop = img[y:(y + h), x:(x + w)]
    cv2.imshow("img",img)
    cv2.waitKey()
    crop = image_resize(crop,87,65)

    crop = crop[0:87,14:79]
    print(crop.shape)
    cv2.imwrite("test4.png",crop)
    cv2.imshow('crop', crop)
    cv2.waitKey()
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

#faces[0] = image_resize(faces[0], 87, 65)

# Display the output
