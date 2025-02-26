import time
import numpy
import cv2
from .neural_network import NeuralNetwork

def train_model(
        learning_rate=0.1,
        input_nodes=784,
        hidden_nodes=200,
        output_nodes=10,
        epochs=10):

    model = NeuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)

    training_data_file = open("./mnist_dataset/mnist_train.csv", 'r')
    training_data_list = training_data_file.readlines()
    training_data_file.close()

    start_time = time.time()

    for epoch in range(epochs):
        print(f"Training: Epoch: {epoch + 1}/{epochs}")
        for record in training_data_list:
            all_values = record.split(',')
            inputs = (numpy.asfarray(all_values[1:], dtype='float') / 255.0 * 0.99) + 0.01
            targets = numpy.zeros(output_nodes) + 0.01
            targets[int(all_values[0])] = 0.99
            model.train(inputs, targets)

    end_time = time.time()
    elapsed_time = end_time - start_time

    hours, rem = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(rem, 60)

    print("Model training finished")
    print(f"{int(hours)} hour(s) {int(minutes)} minute(s) {int(seconds)} second(s)")

    return model

def evaluate_model(model):
    print("Model Evaluation Started")
    test_data_file = open("../mnist_dataset/mnist_test.csv", 'r')
    test_data_list = test_data_file.readlines()
    test_data_file.close()

    scorecard = []

    for record in test_data_list:
        all_values = record.split(',')
        correct_label = int(all_values[0])
        inputs = (numpy.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
        outputs = model.query(inputs)
        predicted_label = numpy.argmax(outputs)

        if predicted_label == correct_label:
            scorecard.append(1)
        else:
            scorecard.append(0)

    scorecard_array = numpy.asarray(scorecard)
    print("Model Evaluation Finished")
    print(f"Score: {scorecard_array.sum()}/{scorecard_array.size}")
    print("Performance: {:.2f}%".format((scorecard_array.sum() / scorecard_array.size) * 100.0))

def recognize_digit(img, model):
    img = cv2.resize(img, (28, 28))
    img = img / 255.0
    img_flat = img.flatten()
    img_for_prediction = numpy.reshape(img_flat, (1, 784))

    prediction = model.query(img_for_prediction)
    prediction_int = int(numpy.argmax(prediction))

    print(f"Prediction: {prediction_int}")

    return prediction_int