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
    fov = int(cfg.get("fov", 200))
    speed = float(cfg.get("speed", 0.5))
    hsv_lower = np.array(cfg.get("hsv_lower", [140,111,160]))
    hsv_upper = np.array(cfg.get("hsv_upper", [148,154,194]))
else:
    # pide al usuario si no hay config
    fov = int(input("FOV: "))
    speed = float(input("SPEED: "))
    hsv_lower = np.array([140,111,160])
    hsv_upper = np.array([148,154,194])

if move_lib is None:
    print("ERROR: ni pydirectinput ni pyautogui están disponibles. Instala dependencias (requirements.txt).")
    raise SystemExit(1)

sct = mss()
screenshot = sct.monitors[1].copy()

# define captura cuadrada centrada
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

def mousemove_local(x):
    """
    x: desplazamiento horizontal en píxeles (float o int).
    Usamos move_lib (pydirectinput o pyautogui) para mover relativo.
    """
    # convertimos a entero y aplicamos un tope razonable para evitar saltos enormes
    max_step = 1000
    xi = int(max(-max_step, min(max_step, round(x))))
    # pydirectinput y pyautogui tienen moveRel(x, y)
    try:
        move_lib.moveRel(xi, 0, duration=0)
    except Exception:
        # fallback: intentar moveTo relativo aproximado
        try:
            cx, cy = move_lib.position()
            move_lib.moveTo(cx + xi, cy, duration=0)
        except Exception:
            pass

kernel = np.ones((3,3), np.uint8)

print("Listo. Mantén pulsado el clic izquierdo para que actúe el aimbot (captura + movimiento).")

try:
    while True:
        # comprobamos si click izquierdo está presionado (0x01)
        if win32api.GetAsyncKeyState(0x01) < 0:
            img = np.array(sct.grab(screenshot))
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, hsv_lower, hsv_upper)
            dilated = cv2.dilate(mask, kernel, iterations=5)
            thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]

            # comprobación robusta antes de momentos
            moments = cv2.moments(thresh)
            if moments["m00"] != 0:
                pixel_x = int(moments["m10"] / moments["m00"])
                # si quieres también el Y:
                # pixel_y = int(moments["m01"] / moments["m00"])

                aimzao = pixel_x + 2
                diff_x = int(aimzao - center)
                alvo = diff_x * speed

                # mueve el ratón localmente en X
                mousemove_local(alvo)

        # pequeño sleep para reducir CPU (ajusta si necesitas más fluidez)
        time.sleep(0.002)

except KeyboardInterrupt:
    print("\nInterrumpido por usuario. Saliendo...")