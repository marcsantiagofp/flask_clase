import cv2
import numpy as np
import pytesseract
import requests
import time
import json

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# IP de la cámara
esp32_url = "http://172.16.5.74/capture"

def ordenar_puntos(puntos):
    puntos = puntos.reshape(4, 2)
    suma = puntos.sum(axis=1)
    diferencia = np.diff(puntos, axis=1)
    return np.array([ 
        puntos[np.argmin(suma)],
        puntos[np.argmin(diferencia)],
        puntos[np.argmax(suma)],
        puntos[np.argmax(diferencia)]
    ], dtype="float32")

def enderezar_imagen(imagen, puntos):
    puntos_ordenados = ordenar_puntos(puntos)
    (tl, tr, br, bl) = puntos_ordenados
    ancho = max(np.linalg.norm(br - bl), np.linalg.norm(tr - tl))
    alto = max(np.linalg.norm(tr - br), np.linalg.norm(tl - bl))
    destino = np.array([[0, 0], [ancho - 1, 0], [ancho - 1, alto - 1], [0, alto - 1]], dtype="float32")
    matriz = cv2.getPerspectiveTransform(puntos_ordenados, destino)
    return cv2.warpPerspective(imagen, matriz, (int(ancho), int(alto)))

def enviar_matricula_a_entrada(matricula):
    url = "http://172.16.6.167:81/api/entrada"
    data = {"matricula": matricula}
    headers = {"Content-Type": "application/json"}

    try:
        print(f"\n Enviando solicitud a {url}")
        print(f" Datos enviados: {json.dumps(data, indent=2)}")

        response = requests.post(url, json=data, headers=headers, timeout=10)

        print(f" Código de estado: {response.status_code}")

        print(f" Respuesta completa: {response.text}")

        try:
            respuesta_json = response.json()
            print(f" Respuesta JSON: {json.dumps(respuesta_json, indent=2)}")
        except json.JSONDecodeError:
            print(" Respuesta no es JSON válido:")
            print(response.text)

        if response.status_code == 200:
            print(" Entrada registrada exitosamente.")
            return True
        elif response.status_code == 400:
            print(" Error: Datos incorrectos (400 Bad Request).")
        elif response.status_code == 403:
            print(" Matrícula no registrada (403 Forbidden).")
        elif response.status_code == 404:
            print(" Ruta no encontrada (404 Not Found).")
        elif response.status_code == 409:
            print(" Parking completo (409 Conflict).")
        else:
            print(f" Error desconocido ({response.status_code})")

        return False
        
    except requests.ConnectionError as e:
        print(f" Error de conexión: {e}")
    except requests.Timeout as e:
        print(f" Error de tiempo de espera: {e}")
    except requests.RequestException as e:
        print(f" Error inesperado en la solicitud: {e}")
        print(f"Detalles de la excepción: {str(e)}")

    return False


while True:
    time.sleep(1.0)
    try:
        response = requests.get(esp32_url, stream=True)
        if response.status_code == 200:
            data = np.frombuffer(response.content, np.uint8)
            image = cv2.imdecode(data, cv2.IMREAD_COLOR)

            if image is None:
                print("Error: No se pudo decodificar la imagen.")
                continue

            cv2.imshow("Imagen Original", image)

            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imshow("Escala de Grises", gray_image)

            edges = cv2.Canny(gray_image, 100, 200)
            cv2.imshow("Bordes Detectados (Canny)", edges)

            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contornos_candidatos = []

            for contour in contours:
                if cv2.contourArea(contour) > 150:
                    epsilon = 0.025 * cv2.arcLength(contour, True)
                    aproximacion = cv2.approxPolyDP(contour, epsilon, True)
                    if len(aproximacion) == 4:
                        contornos_candidatos.append(aproximacion)

            debug_contours = image.copy()
            cv2.drawContours(debug_contours, contornos_candidatos, -1, (0, 255, 0), 2)
            cv2.imshow("Contornos Detectados", debug_contours)

            for rect in contornos_candidatos:
                x, y, w, h = cv2.boundingRect(rect)
                cropped_rect = gray_image[y:y+h, x:x+w]
                cv2.imshow("Recorte ROI", cropped_rect)

                rectangulo_enderezado = enderezar_imagen(image, rect)
                cv2.imshow("Rectángulo Enderezado", rectangulo_enderezado)

                gray_rect = cv2.cvtColor(rectangulo_enderezado, cv2.COLOR_BGR2GRAY)
                _, thresh = cv2.threshold(gray_rect, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                cv2.imshow("Binarización para OCR", thresh)

                texto = pytesseract.image_to_string(thresh, config='--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 -c classify_bln_numeric_mode=1')
                texto_limpio = ''.join(e for e in texto if e.isalnum() or e in [' ', '.', ','])

                if texto_limpio:
                    print(f"Texto detectado: {texto_limpio}")
                    enviar_matricula_a_entrada(texto_limpio)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("Error al obtener la imagen.")
    except Exception as e:
        print(f"Error: {e}")

cv2.destroyAllWindows()