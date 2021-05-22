from flask import Flask, render_template, flash, request, redirect, url_for, jsonify
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
import tensorflow as tf
from PIL import Image
import numpy as np
import requests
import os

app = Flask(__name__)
bootstrap = Bootstrap(app)

UPLOAD_FOLDER = 'web/static/uploaded_images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def recognize_image(path):

        possible_classes = {'altura maxima permitida': 0, 'area reservada para motos': 1, 'desvio a frente': 2,
         'estreitamento de pista': 3, 'fiscalizacao eletronica horizontal 60 km': 4, 
         'fiscalizacao eletronica vertical 50 km': 5, 'fiscalizacao eletronica vertical 60 km': 6, 
         'lombada': 7, 'marcas de perigo': 8, 'pare': 9, 'passagem sinalizada de escolares': 10, 
         'passagem sinalizada de pedestres': 11, 'placa de orientacao de destino': 12, 'ponto de onibus': 13, 
         'proibido estacionar': 14, 'proibido parar e estacionar': 15, 'proibido retornar a esquerda': 16, 
         'proibido trafego de caminhoes': 17, 'proibido virar a direita': 18, 
         'proibido virar a direita veiculos pesados': 19, 'proibido virar a esquerda': 20, 'rotatoria': 21, 
         'rotatoria a frente': 22, 'semaforo a frente': 23, 'siga em frente': 24, 'siga em frente ou a direita': 25,
          'siga em frente ou a esquerda': 26, 'velocidade maxima 30 km': 27, 'velocidade maxima 40 km': 28, 
          'velocidade maxima 50 km': 29, 'velocidade maxima 60 km': 30, 'vire a direita': 31, 'vire a esquerda': 32}

        model = tf.keras.models.load_model('saved_model/traffic_signs_model')
        uploaded_image = image.load_img(path, target_size = (64, 64))
        uploaded_image = uploaded_image.resize((64,64),Image.ANTIALIAS)
        uploaded_image = image.img_to_array(uploaded_image)
        uploaded_image = np.expand_dims(uploaded_image, axis = 0)
        result = model.predict(uploaded_image)
        possible_classes_map = {v: k for k, v in possible_classes.items()}
        return possible_classes_map[np.where(result == 1)[1][0]]


@app.route('/upload_file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"error":"no file received"})

        file1 = request.files['file']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(path)
        result = recognize_image(path)
        return render_template('index.html', result=result, filename=file1.filename )


@app.route('/')
def index():
  return render_template('index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)


