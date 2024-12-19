# -*- coding: utf-8 -*-
"""Plant_Disease_Detection.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ZZP5v9FrBEPaZNkAWNc4OjJaI6c6nZP-

<a href="https://colab.research.google.com/github/visha1Sagar/Plant-Disease-Detection/blob/main/Plant_Disease_Detection.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# **Downloading the Dataset**
"""

!pip install kaggle

!kaggle datasets download -d vipoooool/new-plant-diseases-dataset

!unzip new-plant-diseases-dataset.zip

"""# **Importing Libraries**"""

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense,Conv2D,Dropout,MaxPooling2D,Flatten
from tensorflow.keras.callbacks import EarlyStopping,ModelCheckpoint
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential

"""# **1. Read Training Data**"""

train_data=ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,

)

train_generator=train_data.flow_from_directory(
    'New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)/train/',
    target_size=(224, 224),
    batch_size=512,
    class_mode='categorical',
    subset='training'  # Set to 'training' for training images

)

"""# **2.Read Validation Data**"""

validation_generator = train_data.flow_from_directory(
    'New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)/train/',
    target_size=(224, 224),
    batch_size=512,
    class_mode='categorical',
    subset='validation'  # Set to 'validation' for validation images
)

"""# **3. Read Test Data**"""

test_data=ImageDataGenerator(
    rescale=1./255
)

test_generator=test_data.flow_from_directory(
    'New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)/valid/',
    target_size=(224, 224),
    batch_size=512,
    class_mode='categorical'

)

"""**Showing Each Class Name and Coressponding Index**"""

# Display the 38 unique class names (labels) each one in seperated line
for label,index in train_generator.class_indices.items():
    print(index," : ",label)

"""**Show 50 Random Image and Its Corresponding Label**"""

# Get a batch of images and labels from the train_generator
images, labels = next(train_generator)  # Get the next batch (128 images in this case)

# Reverse the class_indices dictionary to get a mapping from index to class name
class_labels = {v: k for k, v in train_generator.class_indices.items()}

# Convert one-hot encoded labels back to the index form (if using categorical mode)
label_indices = np.argmax(labels, axis=1)

# If you want to shuffle the batch and display 20 random images
random_indices = np.random.choice(len(images), 20, replace=False)  # Choose 20 random indices

# Plot 20 random images with labels
plt.figure(figsize=(20, 20))
for i, idx in enumerate(random_indices):
    plt.subplot(5, 4, i + 1)  # Create a grid of 5 rows and 10 columns
    plt.imshow(images[idx])
    plt.title(class_labels[label_indices[idx]])  # Show the label as the title
    plt.axis('off')  # Hide the axis

plt.show()

model = Sequential()
model.add(Conv2D(32, (3,3),activation='relu',input_shape=(224,224,3))) # Change input_shape to (224, 224, 3)
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Conv2D(64, (3,3),activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Conv2D(128, (3,3),activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))


model.add(Dropout(0.5))
model.add(Flatten())
model.add(Dense(32,activation='relu'))
model.add(Dense(38, activation='softmax')) # Change the number of neurons in the output layer to 38

model.compile(optimizer='adam',
              loss='categorical_crossentropy',  # Change to categorical_crossentropy
              metrics=['accuracy'])  # Change metrics to 'accuracy'

import numpy as np

# Assuming 'train_generator' is your training data generator
# Get the total number of training samples
total_samples = train_generator.samples

import numpy as np

# Assuming 'train_generator' is your training data generator
# Get the total number of training samples
total_samples = train_generator.samples

# Get all training data and labels
X_train, y_train = [], []
for _ in range(int(np.ceil(total_samples / train_generator.batch_size))):
    pass # Add code here to actually get the data and labels from the generator.  The original code was incomplete.

# ... (Your existing code for creating and compiling the model) ...

# Fit the model and store the training history
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // train_generator.batch_size,
    epochs=10,  # Adjust the number of epochs as needed
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // validation_generator.batch_size
)


# ... (Your existing code for plotting the accuracy and loss) ...

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Accuracy')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train','val'],loc='upper right')
plt.show()