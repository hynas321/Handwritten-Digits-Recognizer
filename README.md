# Handwritten Digits Recognizer

## Introduction

The handwritten digits recognizer application allows users to draw on a canvas to determine the most likely digit that was written on the canvas.

The application has a client-server architecture. For the client-side application Angular framework was used, however, on the server side Flask framework in Python. Training and evaluation were done based on the MNIST (Modified National Institute of Standards and Technology) datasets.

![canvas](https://github.com/hynas321/Handwritten-Digits-Recognizer/assets/76520333/1b9ffa77-70b0-4c29-9aab-82b754862f6e)

## Program Installation

In order to run the web application the whole project needs to be set up in the command line. The commands are shown below

**Angular application commands:**

* ```npm install```
* ```ng serve``` - starts the application

**Flask application commands:**

* ```py -3 -m venv .venv```
* ```.venv\Scripts\activate```
* ```pip install Flask```
* ```pip install flask_cors```
* ```pip install opencv-python```
* ```pip install scipy```
* ```py train_model.py ```
* ```py server.py```

## Neural Network Implementation

The neural network is defined as the Python Neural Network class There are the following parameters:

* input nodes,
* hidden nodes,
* output nodes,
* learning rate,
* activation function: sigmoid,
* weight input matrix,
* weight output matrix.

The class which represents the Neural Network has three methods: train – trains the neural network, sigmoid – runs the activation function, and query – makes predictions.

The train method converts input data and target values into 2D arrays. Then, applies the forward pass, and calculates output errors. Next, applies the backward pass, and lastly, adjusts weights taking into account calculated errors.

The query method uses input data which is processed through the neural network using the forward pass. Thus, the final result – prediction, is returned from the method.

The sigmoid method applies the sigmoid, non-linear function.

## Training of the Neural Network

The trained neural network has the following parameters:

* input nodes: 784 (28x28 pixels = 784 pixels),
* hidden nodes: 200,
* output nodes: 10 (0 to 9 digits = 10 in total),
* learning rate: 0.1.

For the purpose of training, the MNIST dataset from a CSV file is loaded. The dataset contains 60000 records of handwritten digits. During training, the entire dataset is processed 10 times, as the number of epochs is set to 10.

There is a loop iteration which iterates over each record in the training dataset. Each record has information about a handwritten digit in the CSV file. From every digit the  values of pixels are extracted, and normalized so that the colours of the canvas 
background and handwritten digit have a clear contrast. Instead of a range [0:255] for grayscale images, [0.01, 1.0] is introduced. There is no zero, as there could be data loss due to omission of parts of the handwritten digit. Then, there is a target array which is used in the training process in order to set neural network’s weights. It is done based on the error between the desired output and the predicted output.

Approximate time of training during evaluation of the project was 9 minutes, however, it depends on the computer processing speed.

## Model Evaluation and Observations

The model was evaluated based on the MNIST testing dataset of 10000 digit images with a resolution of 28x28 pixels. The score was: 9751 correct predictions out of total 10000 which means that the performance was 97.51%. The model performed well in recognizing digits that the MNIST testing dataset contains.

However, in addition, manual testing was done to check the performance of the model with random images created by a user. Each digit was drawn on the canvas which later converted the drawn image to the 28x28 image. The resolution was very low, so a lot of data could be potentially lost when delivered to the model for digit recognition. In the case of small digit that did not fill as much of a canvas space as possible the results were 
often incorrect. Furthermore, shapes of digits uncommon in MNIST training datasets were one of the causes of incorrect predictions. When similar shapes to the ones in the training datasets were drawn, predictions were correct most of the time.




