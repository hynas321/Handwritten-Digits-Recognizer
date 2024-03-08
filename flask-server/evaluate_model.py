import pickle
import numpy
from neuralnetwork import NeuralNetwork

def load_model(filename='neural_network_model.pkl'):
    with open(filename, 'rb') as file:
        model = pickle.load(file)

    return model

def evaluate_model():
    model = load_model('neural_network_model.pkl')

    print("Model Evaluation Started")
    test_data_file = open("mnist_dataset/mnist_test_10K.csv", 'r')
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

if __name__ == '__main__':
    evaluate_model()