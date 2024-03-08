from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import cv2
import pickle
import numpy
from neuralnetwork import NeuralNetwork

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def load_model(filename='neural_network_model.pkl'):
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    print(f"Model loaded: {filename}")

    return model

def recognize_digit(img, model):
    img = cv2.resize(img, (28, 28))
    img = img / 255.0
    img_flat = img.flatten()
    img_for_prediction = numpy.reshape(img_flat, (1, 784))

    prediction = model.query(img_for_prediction)
    prediction_int = int(numpy.argmax(prediction))

    print(f"Prediction: {prediction_int}")

    return prediction_int

model = load_model('neural_network_model.pkl')

if __name__ == '__main__':
    @app.route('/recognize-digit', methods=['POST'])
    def recognize():
        try:
            data_url = request.json['imageData']
            _, data = data_url.split(',', 1)
            img_data = base64.b64decode(data)
            img_array = numpy.frombuffer(img_data, dtype=numpy.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)

            predicted_digit = recognize_digit(img, model)

            result = {'message': f"{predicted_digit}"}
            return jsonify(result), 200

        except Exception as e:
            print("Error:", e.with_traceback())
            return jsonify({'message': 'Error processing image'}), 500

    app.run(debug=True)