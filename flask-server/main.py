from flask import Flask, request, jsonify
from flask_cors import CORS
from custom_utils.file_utils import load_model, save_model
from model.model_logic import recognize_digit, train_model
import base64
import cv2
import numpy


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

model = None

try:
    model = load_model('neural_network_model.pkl')
except FileNotFoundError:
    model = train_model()
    save_model(model)


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

if __name__ == '__main__':
    app.run(debug=True)