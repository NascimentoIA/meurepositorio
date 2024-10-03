import cv2
import numpy as np
import face_recognition
import os

# Função para carregar uma única imagem
def carregar_imagem(caminho_imagem):
    imagem = cv2.imread(caminho_imagem)
    if imagem is None:
        raise FileNotFoundError(f"Erro ao carregar a imagem: {caminho_imagem}")
    return imagem

# Função para gerar encodings da imagem
def gerar_encoding(imagem):
    # Converte BGR para RGB (o formato usado pelo face_recognition)
    img_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
    
    # Gera o encoding do rosto
    encodings = face_recognition.face_encodings(img_rgb)
    
    if len(encodings) > 0:
        return encodings[0]
    else:
        raise ValueError("Nenhum rosto encontrado na imagem.")

##########################################################################################################################
# Atenção !!!!!! Mude para seu caminho colocando a foto que deseja ser reconhecido - Carregar a imagem do banco de dados #
##########################################################################################################################
caminho_imagem = r"F:/Anaconda/socorro/analuiza.jpg" # Certifique-se de que o caminho está correto
imagem = carregar_imagem(caminho_imagem)
encoding_cadastrado = gerar_encoding(imagem)

# Iniciar a captura de vídeo da câmera
video_capture = cv2.VideoCapture(0)

while True:
    # Captura frame a frame
    ret, frame = video_capture.read()
    
    # Redimensiona o vídeo para processar mais rapidamente (escala de 0.25)
    frame_pequeno = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    
    # Converte o frame de BGR (padrão OpenCV) para RGB (padrão face_recognition)
    frame_rgb = cv2.cvtColor(frame_pequeno, cv2.COLOR_BGR2RGB)
    
    # Detectar as localizações dos rostos no frame
    localizacoes_rostos = face_recognition.face_locations(frame_rgb)
    
    # Codificar os rostos detectados no frame
    encodings_rostos = face_recognition.face_encodings(frame_rgb, localizacoes_rostos)
    
    # Para cada rosto detectado no vídeo
    for (top, right, bottom, left), encoding_rosto in zip(localizacoes_rostos, encodings_rostos):
        # Comparar com o rosto cadastrado
        resultado = face_recognition.compare_faces([encoding_cadastrado], encoding_rosto)
        distancia = face_recognition.face_distance([encoding_cadastrado], encoding_rosto)
        
        if resultado[0]:
            nome = "IDENTIFICADO"
        else:
            nome = "DESCONHECIDO"
        
        # Reverter o redimensionamento (já que redimensionamos o frame)
        top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4
        
        # Desenhar um retângulo ao redor do rosto
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        
        # Exibir o nome abaixo do rosto
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, nome, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
    
    # Exibir a imagem da câmera com reconhecimento facial
    cv2.imshow('Video - Reconhecimento Facial', frame)
    
    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libere a câmera e feche todas as janelas
video_capture.release()
cv2.destroyAllWindows()
