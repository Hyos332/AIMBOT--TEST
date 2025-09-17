# main.py
import os
import time
import yaml
import numpy as np
import cv2
from mss import mss
import win32api

# intento usar pydirectinput para mayor compatibilidad con juegos
try:
    import pydirectinput as move_lib
    HAVE_PYDIRECT = True
except Exception:
    try:
        import pyautogui as move_lib
        HAVE_PYDIRECT = False
    except Exception:
        move_lib = None
        HAVE_PYDIRECT = False

os.system("color 2")
os.system("cls")

print("     ___      .______    _______   ______   .______       ___          _______.")
print("    /   \\     |   _  \\  |       \\ /  __  \\  |   _  \\     /   \\        /       |")
print("   /  ^  \\    |  |_)  | |  .--.  |  |  |  | |  |_)  |   /  ^  \\      |   (----`")
print("  /  /_\\  \\   |      /  |  |  |  |  |  |  | |      /   /  /_\\  \\      \\   \\    ")
print(" /  _____  \\  |  |\\  \\.|  '--'  |  `--'  | |  |\\  \\./  _____  \\ .----)   |  ")
print("/__/     \\__\\ | _| `._| |_______/ \\______/  | _| `._|/__/     \\__\\|_______/    ")
print("                                                                                      ")

# carga config si existe
cfg_file = "config.yaml"
if os.path.exists(cfg_file):
    with open(cfg_file, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    fov = int(cfg.get("fov", 600))
    speed = float(cfg.get("speed", 1.5))
    
    # AZULES CLARITOS - RANGO AMPLIO QUE FUNCIONABA ANTES
    hsv_lower = np.array(cfg.get("hsv_lower", [85, 50, 100]))
    hsv_upper = np.array(cfg.get("hsv_upper", [130, 255, 255]))
else:
    # pide al usuario si no hay config
    fov = int(input("FOV (recomendado 600): ") or "600")
    speed = float(input("SPEED (recomendado 1.5): ") or "1.5")
    hsv_lower = np.array([85, 50, 100])
    hsv_upper = np.array([130, 255, 255])

if move_lib is None:
    print("ERROR: ni pydirectinput ni pyautogui están disponibles. Instala dependencias (requirements.txt).")
    raise SystemExit(1)

sct = mss()
screenshot = sct.monitors[1].copy()

# define captura cuadrada centrada con FOV MÁS GRANDE
screenshot['left'] = int((screenshot['width'] / 2) - (fov / 2))
screenshot['top'] = int((screenshot['height'] / 2) - (fov / 2))
screenshot['width'] = fov
screenshot['height'] = fov
center = fov / 2

os.system("cls")
print(" __        ______        ___       _______   _______  _______  ")
print("|  |      /  __  \\      /   \\     |       \\ |   ____||       \\ ")
print("|  |     |  |  |  |    /  ^  \\    |  .--.  ||  |__   |  .--.  |")
print("|  |     |  |  |  |   /  /_\\  \\   |  |  |  ||   __|  |  |  |  |")
print("|  `----.|  `--'  |  /  _____  \\  |  '--'  ||  |____ |  '--'  |")
print("|_______| \\______/  /__/     \\__\\ |_______/ |_______||_______/ ")
print("                                                               ")

def mousemove_local(x, y):
    """
    x: desplazamiento horizontal en píxeles
    y: desplazamiento vertical en píxeles
    """
    max_step = 300  # LÍMITE MÁS PEQUEÑO para movimientos más controlados
    xi = int(max(-max_step, min(max_step, round(x))))
    yi = int(max(-max_step, min(max_step, round(y))))
    
    print(f"Moviendo mouse X:{xi}, Y:{yi} píxeles...")
    
    try:
        move_lib.moveRel(xi, yi, duration=0)
        print(f"✓ Mouse movido correctamente")
    except Exception as e:
        print(f"✗ Error moviendo mouse: {e}")

kernel = np.ones((3,3), np.uint8)  # KERNEL MÁS PEQUEÑO para mayor precisión

print("Listo. Mantén pulsada la tecla G para que actúe el aimbot.")
print(f"FOV: {fov} píxeles")
print(f"VELOCIDAD: {speed}x")
print(f"RANGO HSV: {hsv_lower} a {hsv_upper}")
print("DETECTARÁ: AZULES CLARITOS (rango amplio)")
print("DIAGNÓSTICO: Presiona G y observa los mensajes...")

try:
    while True:
        if win32api.GetAsyncKeyState(0x47) < 0:  # tecla G
            print("✓ Tecla G detectada")
            img = np.array(sct.grab(screenshot))
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            
            # DETECCIÓN CON RANGO AMPLIO
            mask = cv2.inRange(hsv, hsv_lower, hsv_upper)
            pixel_count = cv2.countNonZero(mask)
            
            print(f"Píxeles detectados: {pixel_count}")
            
            if pixel_count > 100:  # UMBRAL MÁS ALTO para ser más selectivo
                print(f"✓ Azules claritos detectados! ({pixel_count} píxeles)")
                
                # PROCESAMIENTO MÁS PRECISO
                dilated = cv2.dilate(mask, kernel, iterations=2)  # MENOS dilatación
                thresh = cv2.threshold(dilated, 80, 255, cv2.THRESH_BINARY)[1]  # UMBRAL MÁS ALTO
                
                moments = cv2.moments(thresh)
                if moments["m00"] != 0:
                    # CÁLCULO DE CENTRO CON MAYOR PRECISIÓN
                    pixel_x = moments["m10"] / moments["m00"]
                    pixel_y = moments["m01"] / moments["m00"]
                    
                    print(f"✓ Centro encontrado en X:{pixel_x:.1f}, Y:{pixel_y:.1f}")
                    print(f"✓ Centro pantalla: X:{center}, Y:{center}")
                    
                    # CALCULAR MOVIMIENTO CON ZONA MUERTA
                    diff_x = pixel_x - center
                    diff_y = pixel_y - center
                    
                    # CALIBRACIÓN FINA - AJUSTE HACIA ARRIBA
                    calibration_x = 0    # Ajuste horizontal (si necesitas)
                    calibration_y = -5   # Ajuste hacia ARRIBA (negativo = arriba)
                    
                    # APLICAR CALIBRACIÓN
                    diff_x += calibration_x
                    diff_y += calibration_y
                    
                    # ZONA MUERTA - no mover si está muy cerca del centro
                    dead_zone = 10  # píxeles de tolerancia
                    if abs(diff_x) < dead_zone and abs(diff_y) < dead_zone:
                        print(f"✓ Ya está centrado (zona muerta: {dead_zone}px)")
                        continue
                    
                    move_x = diff_x * speed
                    move_y = diff_y * speed
                    
                    print(f"✓ Diferencia original: X:{pixel_x - center:.1f}, Y:{pixel_y - center:.1f}")
                    print(f"✓ Con calibración: X:{diff_x:.1f}, Y:{diff_y:.1f}")
                    print(f"✓ Movimiento final: X:{move_x:.1f}, Y:{move_y:.1f}")
                    
                    # MOVER MOUSE
                    mousemove_local(move_x, move_y)
                else:
                    print("✗ No se pudo calcular el centro")
            else:
                print(f"✗ Pocos píxeles detectados: {pixel_count} (necesita >100)")

        time.sleep(0.05)

except KeyboardInterrupt:
    print("\nInterrumpido por usuario. Saliendo...")