import cv2
from hand_tracker import HandTracker
import socket

# Parâmetros da câmera
width, height = 1280, 720

cap = cv2.VideoCapture(1)
cap.set(3, width)  # Set width
cap.set(4, height)   # Set height

detector = HandTracker(maxHands=1)

# Comunicação UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ('127.0.0.1', 6767)

while True:
    success, img = cap.read()
    if not success:
        break

    hands, img = detector.process_frame(img)

    data = []
    # Landmark valores - (x, y, z) * 21
    if hands:
        hand = hands[0]
        lmList = hand  # Lista de 21 landmarks

        for lm in lmList:
            data.extend([lm[0], height- 350 - lm[1], lm[2]])  # Agregar x, y, z a la lista de datos
        
        sock.sendto(str(data).encode(), serverAddressPort)
    
    
    img = cv2.resize(img, (0, 0), None, 0.5, 0.5)  # Reduzir a imagem para metade do tamanho
    cv2.imshow("Webcam", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break