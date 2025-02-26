import pickle


def save_model(model, filename='neural_network_model.pkl'):
    with open(filename, 'wb') as file:
        pickle.dump(model, file)
    print(f"Model saved: {filename}")

def load_model(filename='neural_network_model.pkl'):
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    print(f"Model loaded: {filename}")

    return model