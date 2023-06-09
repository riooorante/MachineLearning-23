# -*- coding: utf-8 -*-
"""TugasAkhir_MLPemula.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1J3XoSZ1vhoGlqP7Tlk5uHnetiRyX45Ia

A. Loading Data

Dataset telah disediakan oleh Dicoding yang disimpan di repository github. !wget digunakan untuk mengunduh data dari sebuah website.
"""

# Loading data
!wget --no-check-certificate \
  https://github.com/dicodingacademy/assets/releases/download/release/rockpaperscissors.zip \
  -O /tmp/rockpaperscissors.zip

# Melakukan ekstrak file zip
import zipfile,os

local_zip = '/tmp/rockpaperscissors.zip'
zip_ref = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall('/tmp')
zip_ref.close()

# Path file train dan val
parent_dir = '/tmp/rockpaperscissors'
train_dir = os.path.join(parent_dir, 'train')
validation_dir = os.path.join(parent_dir, 'val')

# Membuat direktori train dan val
# os.mkdir(train.dir)
# os.mkdir(val.dir)

print(os.listdir('/tmp/rockpaperscissors'))

"""C. Membagi Data

Membagi data kedalam dua kategori yaitu train dan validation. Pembagian data dapat menggunakan train_test_split yang telah disediakan oleh SkLearn. Data yang dialokasikan untuk Validation Set adalah 40% tiap target (Rock, Paper, Scissor). 
"""

# Membagi data Train dan Validation (40%)
from sklearn.model_selection import train_test_split

Rock_train, rock_val = train_test_split(os.listdir('/tmp/rockpaperscissors/rock'), test_size=0.4)
Paper_train, paper_val = train_test_split(os.listdir('/tmp/rockpaperscissors/paper'), test_size=0.4)
Scissors_train, scissors_val = train_test_split(os.listdir('/tmp/rockpaperscissors/scissors'), test_size=0.4)

"""D. Pembuatan Direktori

Dataset train dan validation akan disimpan di direktorinya masing-masing yaitu train dan val direktori. Tiap direktori akan memiliki tiga folder baru dengan nama paper, rock, scissors. Direktori baru dapat dibuat dengan perintah os.mkdir(Lokasi_Direktori_Baru). 
"""

# os.mkdir('/tmp/rockpaperscissors/train/rock')
# os.mkdir('/tmp/rockpaperscissors/train/paper')
# os.mkdir('/tmp/rockpaperscissors/train/scissors')
print(os.listdir('/tmp/rockpaperscissors/train'))

# os.mkdir('/tmp/rockpaperscissors/val/rock')
# os.mkdir('/tmp/rockpaperscissors/val/paper')
# os.mkdir('/tmp/rockpaperscissors/val/scissors')
print(os.listdir('/tmp/rockpaperscissors/val'))

# Image Augmentation
from tensorflow.keras.preprocessing.image import ImageDataGenerator
train_datagen = ImageDataGenerator(
                    rescale=1./255,
                    rotation_range=20,
                    horizontal_flip=True,
                    vertical_flip=True,
                    shear_range=0.2,
                    fill_mode='nearest')
test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(150,150),
    batch_size=32,
    class_mode= 'categorical'
)

validation_generator = train_datagen.flow_from_directory(
    validation_dir,
    target_size=(150,150),
    batch_size=32,
    class_mode= 'categorical'
)

import tensorflow as tf
model = tf.keras.models.Sequential([
  tf.keras.layers.Conv2D(32, (3,3), activation = 'relu', input_shape= (150,150,3)),
  tf.keras.layers.MaxPooling2D(2,2),
  tf.keras.layers.Conv2D(64,(3,3), activation= 'relu'),
  tf.keras.layers.MaxPooling2D(2,2),
  tf.keras.layers.Conv2D(128,(3,3), activation= 'relu'),
  tf.keras.layers.MaxPooling2D(2,2),
  tf.keras.layers.Conv2D(256,(3,3), activation= 'relu'),
  tf.keras.layers.MaxPooling2D(2,2),
  tf.keras.layers.Conv2D(512,(3,3), activation= 'relu'),
  tf.keras.layers.MaxPooling2D(2,2),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(512, activation= 'relu'),
  tf.keras.layers.Dense(3, activation= 'softmax')
])

model.summary()

model.compile(loss = 'categorical_crossentropy',
              optimizer = tf.keras.optimizers.Adadelta(learning_rate=0.1),
              metrics=['accuracy'])

history = model.fit(
    train_generator,
    steps_per_epoch=25,
    epochs=25,
    validation_data=validation_generator,
    validation_steps=5,
    verbose=2)

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
from google.colab import files
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from sklearn.metrics import accuracy_score
# %matplotlib inline
 
uploaded = files.upload()
 
for fn in uploaded.keys():
 
  path = fn
  img = image.load_img(path, target_size=(150,150))
 
  imgplot = plt.imshow(img)
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis=0)

  images = np.vstack([x])
 
  prediksi = model.predict(images, batch_size=10) # [[paper. rock. scissors.]]
  print(prediksi.shape)
  
  if prediksi[0,0] == 1:
    print('Paper')
  elif prediksi[0,1] == 1:
    print('Rock')
  else:
    print('Scissors')

# Mario Valerian Rante Ta'dung
# E-mail = rantetadungrio@gmail.com

