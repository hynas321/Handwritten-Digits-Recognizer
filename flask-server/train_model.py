import time
import pickle
import numpy
from neuralnetwork import NeuralNetwork

def save_model(model, filename='neural_network_model.pkl'):
    with open(filename, 'wb') as file:
        pickle.dump(model, file)
    print(f"Model saved: {filename}")

def train_model():
    learning_rate = 0.1
    input_nodes = 784
    hidden_nodes = 200
    output_nodes = 10

    neural_network = NeuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)

    training_data_file = open("mnist_dataset/mnist_train_60K.csv", 'r')
    training_data_list = training_data_file.readlines()
    training_data_file.close()

    epochs = 10
    start_time = time.time()

    for epoch in range(epochs):
        print(f"Training: Epoch: {epoch + 1}/{epochs}")
        for record in training_data_list:
            all_values = record.split(',')
            inputs = (numpy.asfarray(all_values[1:], dtype='float') / 255.0 * 0.99) + 0.01
            targets = numpy.zeros(output_nodes) + 0.01
            targets[int(all_values[0])] = 0.99
            neural_network.train(inputs, targets)

    end_time = time.time()
    elapsed_time = end_time - start_time

    hours, rem = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(rem, 60)

    print("Model training finished")
    print(f"{int(hours)} hour(s) {int(minutes)} minute(s) {int(seconds)} second(s)")

    save_model(neural_network)

if __name__ == '__main__':
    train_model()