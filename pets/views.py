from django.shortcuts import render, get_object_or_404, redirect
from .models import Pet, Classification_pet
from datetime import date
import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
from PIL import Image
import tensorflow as tf
from .forms import PostForm

from tensorflow import keras
from tensorflow.keras import layers, datasets, models
from tensorflow.keras.models import Sequential

import pathlib


def main(request):
    return render(request, 'pets/main.html')
# Create your views here.

def pets_owner_list(request):
    user = request.user
    pet = Pet.objects.filter(owner=user)
    return render(request, 'pets/pets_owner_list.html', {'pet': pet})

def pet_detail(request, id):
    pet = get_object_or_404(Pet, id=id)
    return render(request, 'pets/pet_detail.html', {'pet': pet})

def neuron_network(request):
    form = PostForm(request.POST, request.FILES or None)
    if request.method == 'POST':

        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            form = PostForm()


            data_dir = pathlib.Path("dataset/training_set/")

            image_count = len(list(data_dir.glob('*/*.jpg')))

            batch_size = 32
            img_height = 200  # высота изображения в пикселях
            img_width = 200  # ширина изображения в пикселях

            # Данные для тренировки
            train_ds = tf.keras.utils.image_dataset_from_directory(
                data_dir,
                validation_split=0.2,
                subset="training",
                seed=123,
                image_size=(img_height, img_width),
                batch_size=batch_size)

            val_ds = tf.keras.utils.image_dataset_from_directory(
                data_dir,
                validation_split=0.2,
                subset="validation",
                seed=123,
                image_size=(img_height, img_width),
                batch_size=batch_size)

            class_names = train_ds.class_names

            # Настройить набор данных для повышения эффективности
            AUTOTUNE = tf.data.AUTOTUNE

            # Dataset.cache сохраняет изображения в памяти после их загрузки с диска в течение первой эпохи.
            # Это гарантирует, что набор данных не станет узким местом при обучении  модели.
            train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
            # Dataset.prefetch перекрывает предварительную обработку данных и выполнение модели во время обучения
            val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

            # Стандартизировать данные
            normalization_layer = tf.keras.layers.Rescaling(1. / 255)

            normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
            image_batch, labels_batch = next(iter(normalized_ds))
            first_image = image_batch[0]
            # Notice the pixel values are now in `[0,1]`.
            # print(np.min(first_image), np.max(first_image))

            num_classes = len(class_names)

            data_augmentation = keras.Sequential(
                [
                    tf.keras.layers.RandomFlip("horizontal",
                                               input_shape=(img_height,
                                                            img_width,
                                                            3)),
                    tf.keras.layers.RandomRotation(0.1),
                    tf.keras.layers.RandomZoom(0.1),
                ]
            )

            # plt.figure(figsize=(10, 10))
            # for images, _ in train_ds.take(1):
            #     for i in range(9):
            #         augmented_images = data_augmentation(images)
            #         ax = plt.subplot(3, 3, i + 1)
            #         plt.imshow(augmented_images[0].numpy().astype("uint8"))
            #         plt.axis("off")
            #     plt.show()

            model = Sequential([
                data_augmentation,
                tf.keras.layers.Rescaling(1. / 255),
                layers.Conv2D(16, 3, padding='same', activation='relu'),
                layers.MaxPooling2D(),
                layers.Conv2D(32, 3, padding='same', activation='relu'),
                layers.MaxPooling2D(),
                layers.Conv2D(64, 3, padding='same', activation='relu'),
                layers.MaxPooling2D(),
                layers.Dropout(0.2),
                layers.Flatten(),
                layers.Dense(128, activation='relu'),
                layers.Dense(num_classes)
            ])

            model.compile(optimizer='adam',
                          loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                          metrics=['accuracy'])

            # model.summary()

            epochs = 1
            history = model.fit(
                train_ds,
                validation_data=val_ds,
                epochs=epochs
            )

            acc = history.history['accuracy']
            val_acc = history.history['val_accuracy']

            loss = history.history['loss']
            val_loss = history.history['val_loss']

            epochs_range = range(epochs)

            path = post.image.path

            # picture = Image.open(path)
            # picture.show()

            img = tf.keras.utils.load_img(
                path, target_size=(img_height, img_width)
            )

            img_array = tf.keras.utils.img_to_array(img)
            img_array = tf.expand_dims(img_array, 0)  # Create a batch

            predictions = model.predict(img_array)
            score = tf.nn.softmax(predictions[0])

            result_text = (
                "Это изображение, скорее всего, принадлежит {} с {:.2f} процентом достоверности."
                    .format(class_names[np.argmax(score)], 100 * np.max(score))
            )
            return render(request, 'pets/pet_neuron_result.html', {'result_text': result_text})

    return render(request, 'pets/pet_neuron.html', {'form': form})

