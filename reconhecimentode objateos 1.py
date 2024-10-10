# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 16:58:19 2024

@author: User
"""
# Instalar dependências (caso necessário)
# !pip install tensorflow tensorflow-hub opencv-python-headless pillow

# Imports and function definitions
import tensorflow as tf
import tensorflow_hub as hub
import cv2
import numpy as np
from PIL import Image, ImageDraw
import time

# Função para desenhar caixas de detecção na imagem
def draw_boxes(image, boxes, class_names, scores, max_boxes=10, min_score=0.1):
    """
    Função para desenhar as caixas de detecção de objetos na imagem.
    
    image: imagem a ser desenhada
    boxes: coordenadas das caixas delimitadoras
    class_names: nomes das classes dos objetos detectados
    scores: pontuações (confiabilidade) das detecções
    max_boxes: número máximo de caixas a desenhar
    min_score: pontuação mínima para exibir a detecção
    """
    draw = ImageDraw.Draw(image)
    width, height = image.size
    for i in range(min(len(boxes), max_boxes)):
        if scores[i] >= min_score:
            box = boxes[i]
            ymin, xmin, ymax, xmax = box
            left, right, top, bottom = (xmin * width, xmax * width, ymin * height, ymax * height)
            draw.rectangle([(left, top), (right, bottom)], outline="red", width=3)
            draw.text((left, top), f"{class_names[i]}: {int(scores[i] * 100)}%", fill="red")

# Função para realizar o reconhecimento de objetos
def detect_objects(model, image_np):
    """
    Função para realizar a detecção de objetos em uma imagem.
    
    model: modelo carregado do TensorFlow Hub
    image_np: imagem em formato numpy
    """
    # Expandir a imagem para corresponder ao formato esperado pelo modelo
    image_np_expanded = np.expand_dims(image_np, axis=0)
    
    # Converter a imagem para float32
    converted_img = tf.image.convert_image_dtype(image_np_expanded, dtype=tf.float32)
    
    # Acessar a função de assinatura específica para inferência
    detector = model.signatures.get('default')
    if detector is None:
        print("Erro: a assinatura 'default' não está disponível no modelo.")
        return None
    
    # Tentar rodar a inferência com o modelo
    try:
        result = detector(converted_img)
    except Exception as e:
        print(f"Erro ao realizar a inferência: {e}")
        return None
    
    # Converter o resultado em um dicionário legível
    result = {key: value.numpy() for key, value in result.items()}
    return result

# Função principal para capturar a imagem da câmera e realizar a detecção
def run_object_detection():
    # Carregar o modelo do TensorFlow Hub (MobileNet SSD v2)
    model_url = "https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1"
    model = hub.load(model_url)
    
    # Iniciar a captura da câmera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erro ao acessar a câmera!")
        return

    print("Pressione 'q' para sair.")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Erro ao capturar o frame da câmera.")
                break

            # Converter a imagem para formato compatível com o modelo
            image_np = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(image_np)

            # Realizar a detecção de objetos
            start_time = time.time()
            result = detect_objects(model, image_np)
            end_time = time.time()

            if result is None:
                print("Erro ao detectar objetos. Interrompendo...")
                break

            # Desenhar as caixas de detecção na imagem
            draw_boxes(pil_image, result['detection_boxes'], result['detection_class_entities'], result['detection_scores'])

            # Mostrar a imagem com as detecções
            output_image = np.array(pil_image)
            cv2.imshow('Reconhecimento de Objetos', cv2.cvtColor(output_image, cv2.COLOR_RGB2BGR))

            print(f"Tempo de inferência: {end_time - start_time:.2f} segundos")

            # Pressione 'q' para sair
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        # Liberar a câmera e fechar as janelas
        cap.release()
        cv2.destroyAllWindows()

# Executar a função principal
if __name__ == "__main__":
    run_object_detection()
