import cv2
import tkinter as tk
from tkinter import filedialog

def selecionar_video():
    root = tk.Tk()
    root.withdraw()
    caminho_video = filedialog.askopenfilename(
        title="Selecione o vídeo",
        filetypes=[("Arquivos de vídeo", "*.mp4")])
    return caminho_video

# Selecionar o arquivo de vídeo
caminho_video = selecionar_video()

# Verifique se o usuário selecionou um arquivo
if not caminho_video:
    print("Nenhum vídeo selecionado. Encerrando.")
    exit()

rastreador = cv2.TrackerCSRT_create()
video = cv2.VideoCapture(caminho_video)

carregado, frame = video.read()

if not carregado:
    print("Falha ao carregar o vídeo. Encerrando.")
    exit()

balBox = cv2.selectROI(frame)
print(balBox)

carregado = rastreador.init(frame, balBox)

while True:
    carregado, frame = video.read()
    if not carregado:
        break

    carregado, balBox = rastreador.update(frame)

    if carregado:
        (x, y, w, h) = [int(v) for v in balBox]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2, 1)
    else:
        cv2.putText(frame, 'Falha ao rastrear', (80, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255))

    cv2.imshow('Tracking...', frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

video.release()
cv2.destroyAllWindows()


