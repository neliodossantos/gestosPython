import cv2
import mediapipe as mp
import math
from collections import deque

# Inicializa o MediaPipe para detecção de mãos
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Fila para suavizar a detecção de dedos
historico_deteccoes = deque(maxlen=5)

# Função para calcular ângulo entre três pontos
def calcular_angulo(p1, p2, p3):
    angulo = math.degrees(math.atan2(p3.y - p2.y, p3.x - p2.x) - math.atan2(p1.y - p2.y, p1.x - p2.x))
    return abs(angulo)
# Função para suavizar a detecção de dedos
def suavizar_deteccao(dedos_levantados):
    historico_deteccoes.append(dedos_levantados)
    media = [sum(col) / len(historico_deteccoes) for col in zip(*historico_deteccoes)]
    return [1 if m > 0.5 else 0 for m in media]

# Função para detectar gestos de uma única mão
def detectar_gesto_unico(dedos_levantados):
    if dedos_levantados == [0, 1, 0, 0, 0]:  # Apenas o indicador levantado
        return "Oi"
    elif dedos_levantados == [0, 1, 1, 1, 1]:  # Todos os dedos, exceto o polegar
        return "Mão aberta"
    elif dedos_levantados == [1, 1, 1, 0, 0]:  # Polegar, indicador e médio levantados
        return "Eu te amo"
    elif dedos_levantados == [0, 0, 0, 0, 0]:  # Nenhum dedo levantado
        return "Não"
    elif dedos_levantados == [1, 0, 0, 0, 0]:  # Apenas o polegar levantado
        return "Sim"
    elif dedos_levantados == [1, 1, 0, 0, 0]:  # Polegar e indicador levantados
        return "Paz"
    elif dedos_levantados == [0, 1, 0, 0, 1]:  # Indicador e mínimo levantados
        return "Eu te amo"
    elif dedos_levantados == [0, 0, 0, 1, 1]:  # Anelar e mínimo levantados
        return "Rock"
    return "Gesto desconhecido"

# Função para combinar gestos de duas mãos
def combinar_gestos(gesto_mao1, gesto_mao2):
    if gesto_mao1 == "Mão aberta" and gesto_mao2 == "Mão aberta":
        return "Bater palmas"
    elif gesto_mao1 == "Sim" and gesto_mao2 == "Sim":
        return "Aprovação dupla"
    elif gesto_mao1 == "Oi" and gesto_mao2 == "Oi":
        return "Saudação dupla"
    elif gesto_mao1 == "Eu te amo" and gesto_mao2 == "Eu te amo":
        return "Amor recíproco"
    elif gesto_mao1 == "Rock" and gesto_mao2 == "Rock":
        return "Rock and Roll"
    elif (gesto_mao1 == "Mão aberta" and gesto_mao2 == "Paz") or (gesto_mao1 == "Paz" and gesto_mao2 == "Mão aberta"):
        return "Paz e Amor"
    return f"{gesto_mao1} + {gesto_mao2}"

# Captura de vídeo
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Converte a imagem para RGB (MediaPipe requer RGB)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    gestos_detectados = []

    # Detecta as mãos e desenha as marcações
    if results.multi_hand_landmarks:
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # IDs das pontas e bases dos dedos
            dedo_ponta_ids = [4, 8, 12, 16, 20]  # IDs das pontas dos dedos
            dedos_levantados = []

            # Verifica se os dedos estão levantados usando ângulos
            for i, id in enumerate(dedo_ponta_ids):
                if i == 0:  # Polegar
                    angulo = calcular_angulo(
                        hand_landmarks.landmark[2],  # Base
                        hand_landmarks.landmark[3],  # Intermediário
                        hand_landmarks.landmark[4],  # Ponta
                    )
                    dedos_levantados.append(1 if angulo < 30 else 0)
                else:  # Outros dedos
                    if hand_landmarks.landmark[id].y < hand_landmarks.landmark[id - 2].y:
                        dedos_levantados.append(1)
                    else:
                        dedos_levantados.append(0)

            # Suaviza a detecção
            dedos_levantados = suavizar_deteccao(dedos_levantados)

            # Detecta o gesto da mão atual
            gesto = detectar_gesto_unico(dedos_levantados)
            gestos_detectados.append(gesto)

            # Mostra o gesto detectado para a mão
            cv2.putText(frame, gesto, (10, 30 + idx * 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        # Combinando gestos de duas mãos
        if len(gestos_detectados) == 2:
            gesto_combinado = combinar_gestos(gestos_detectados[0], gestos_detectados[1])
            cv2.putText(frame, gesto_combinado, (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Exibe o vídeo com as marcações
    cv2.imshow("Reconhecimento de Gestos - Libras", frame)

    # Encerra ao pressionar 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
