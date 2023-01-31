
from sklearn.preprocessing import LabelEncoder
import tensorflow.keras as keras
import numpy as np


L = keras.layers
def define_dense_model():
    model = keras.Sequential([
        L.Dense(10, activation='relu'),
        L.BatchNormalization(),
        L.Dropout(0.15),
        L.Dense(9, activation='softmax')
    ])
    
    model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])
    return model

def label_encode(candidates_list):
    labels = [candidate['label'] for candidate in candidates_list]
    label_encoder = LabelEncoder()
    integers_encoded = label_encoder.fit_transform(labels)
    for integer, candidate in zip(integers_encoded, candidates_list):
        candidate['encoded_label'] = integer
    
    def vector_to_labels(vector, threshold=0.4):
        assert len(vector) == len(label_encoder.classes_)
        indexes = np.where(vector>threshold)[0]
        return label_encoder.inverse_transform(indexes)
    
    return vector_to_labels


def get_x_and_y(candidates_list):
    features = [candidate['features']['spacy_vector'] for candidate in candidates_list]
    integers_encoded = [candidate['encoded_label'] for candidate in candidates_list]

    y = keras.utils.to_categorical(integers_encoded)    
    X = np.vstack(features)
    
    return X, y


def inference_on_example(
    candidate, model, vector_to_labels, threshold=0.2, show=False,   
    ):
    candidate_text = candidate['candidate'][0]
    type_ = candidate['type']
    meta = candidate['meta']
    
    x = candidate['features']['spacy_vector']
    true_label = candidate['label']
    
    predicted_vector = model(x.reshape(1, -1)).numpy().flatten()
    
    predicted_labels = vector_to_labels(predicted_vector, threshold=threshold)
    
    if show:
        print(f'Candidate Info:\n\ttext: {candidate_text}\n\ttype: {type_}\n\tmeta: {meta}')
        print(f'\nResult:\n\ttrue_label: {true_label}\n\tpredicted_labels: {predicted_labels}')
    
    
    return predicted_labels
    