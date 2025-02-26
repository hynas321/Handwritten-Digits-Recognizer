import time
import numpy
import cv2
from .neural_network import NeuralNetwork

def train_model(
        learning_rate=0.1,
        input_nodes=784,
        hidden_nodes=200,
        output_nodes=10,
        epochs=20,
        patience=2):
    model = NeuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)

    with open("./mnist_dataset/mnist_train.csv", 'r') as training_data_file:
        training_data_list = training_data_file.readlines()

    best_accuracy = 0.0
    no_improve_count = 0
    start_time = time.time()

    for epoch in range(epochs):
        print(f"Training: Epoch {epoch + 1}/{epochs}")
        for record in training_data_list:
            all_values = record.strip().split(',')
            inputs = (numpy.asfarray(all_values[1:], dtype='float') / 255.0 * 0.99) + 0.01
            targets = numpy.zeros(output_nodes) + 0.01
            targets[int(all_values[0])] = 0.99
            model.train(inputs, targets)

        accuracy = evaluate_model(model)

        if accuracy > best_accuracy:
            best_accuracy = accuracy
            no_improve_count = 0
        else:
            no_improve_count += 1
            print(f"No improvement for {no_improve_count} epoch(s)")
            if no_improve_count >= patience:
                print(f"Early stopping triggered after {epoch + 1} epochs")
                break

    elapsed_time = time.time() - start_time
    hours, rem = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(rem, 60)
    print("Model training finished")
    print(f"{int(hours)} hour(s) {int(minutes)} minute(s) {int(seconds)} second(s)")

    return model

def evaluate_model(model):
    with open("./mnist_dataset/mnist_test.csv", 'r') as test_data_file:
        test_data_list = test_data_file.readlines()

    scorecard = []

    for record in test_data_list:
        all_values = record.strip().split(',')
        correct_label = int(all_values[0])
        inputs = (numpy.asfarray(all_values[1:], dtype='float') / 255.0 * 0.99) + 0.01
        outputs = model.query(inputs)
        predicted_label = numpy.argmax(outputs)

        if predicted_label == correct_label:
            scorecard.append(1)
        else:
            scorecard.append(0)

    scorecard_array = numpy.asarray(scorecard)
    accuracy = scorecard_array.sum() / scorecard_array.size
    print(f"Score: {scorecard_array.sum()}/{scorecard_array.size}")
    print("Performance: {:.2f}%".format(accuracy * 100.0))
    return accuracy

def recognize_digit(img, model):
    img = cv2.resize(img, (28, 28))
    img = img / 255.0
    img_flat = img.flatten()
    img_for_prediction = numpy.reshape(img_flat, (1, 784))

    prediction = model.query(img_for_prediction)
    prediction_int = int(numpy.argmax(prediction))

    print(f"Prediction: {prediction_int}")

    return prediction_int