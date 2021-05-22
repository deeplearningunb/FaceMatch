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

UPLOAD_FOLDER = './uploaded_images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def recognize_image(path):

        possible_classes = {'altura_maxima_permitida': 0, 'area_reservada_para_motos': 1, 'desvio_a_frente': 2,
         'estreitamento_de_pista': 3, 'fiscalizacao_eletronica_horizontal_60_km': 4, 
         'fiscalizacao_eletronica_vertical_50_km': 5, 'fiscalizacao_eletronica_vertical_60_km': 6, 
         'lombada': 7, 'marcas_de_perigo': 8, 'pare': 9, 'passagem_sinalizada_de_escolares': 10, 
         'passagem_sinalizada_de_pedestres': 11, 'placa_de_orientacao_de_destino': 12, 'ponto_de_onibus': 13, 
         'proibido_estacionar': 14, 'proibido_parar_e_estacionar': 15, 'proibido_retornar_a_esquerda': 16, 
         'proibido_trafego_de_caminhoes': 17, 'proibido_virar_a_direita': 18, 
         'proibido_virar_a_direita_veiculos_pesados': 19, 'proibido_virar_a_esquerda': 20, 'rotatoria': 21, 
         'rotatoria_a_frente': 22, 'semaforo_a_frente': 23, 'siga_em_frente': 24, 'siga_em_frente_ou_a_direita': 25,
          'siga_em_frente_ou_a_esquerda': 26, 'velocidade_maxima_30_km': 27, 'velocidade_maxima_40_km': 28, 
          'velocidade_maxima_50_km': 29, 'velocidade_maxima_60_km': 30, 'vire_a_direita': 31, 'vire_a_esquerda': 32}

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
        return jsonify({"result": result})


@app.route('/')
def index():
  return render_template('index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)


