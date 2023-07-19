from pathlib import Path

import pandas as pd
from flask import Flask, jsonify, render_template, request

from src.pipeline.batch_prediction import start_batch_prediction
from src.pipeline.training_pipeline import start_training_pipeline

input_fp = Path('input.csv')
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/train_model', methods=['POST'])
def train_model():
    start_training_pipeline()
    return jsonify({'message': 'Model Training Completed!'})


@app.route('/predict')
def predict():
    return render_template('predict.html')


@app.route('/batch_prediction', methods=['POST'])
def batch_prediction():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'})

    try:
        df = pd.read_csv(file.stream)
        df.to_csv(input_fp)
        prediction_fp = Path(start_batch_prediction(input_fp))
        return {
            'message': 'Prediction Completed!',
            'prediction_path': prediction_fp.absolute().as_uri(),
        }
    except Exception as e:
        return jsonify(f'Error occurred: {e}')


if __name__ == '__main__':
    app.run(debug=True, port=8501)
