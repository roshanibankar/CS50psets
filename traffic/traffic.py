import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split
from tensorflow import layers, models

# Image dimensions
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
EPOCHS = 10


def main():

    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")
    images, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=0.4
    )
    model = get_model()
    model.fit(X_train, y_train, epochs=EPOCHS)
    model.evaluate(X_test, y_test, verbose=2)
    if len(sys.argv) == 3:
        model.save(sys.argv[2])
        print("Model saved.")


def load_data(data_dir):

    images = []
    labels = []
    for category in range(NUM_CATEGORIES):
        category_path = os.path.join(data_dir, str(category))

        for filename in os.listdir(category_path):
            img_path = os.path.join(category_path, filename)

            image = cv2.imread(img_path)
            image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))

            images.append(image)
            labels.append(category)

    return images, labels


def get_model():
  
    model = models.Sequential()

    model.add(layers.Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Conv2D(64, (3, 3), activation="relu"))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Conv2D(128, (3, 3), activation="relu"))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Flatten())
    model.add(layers.Dense(128, activation="relu"))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(NUM_CATEGORIES, activation="softmax"))

    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


if __name__ == "__main__":
    main()
