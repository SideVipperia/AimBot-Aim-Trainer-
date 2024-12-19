import cv2
import time
from pynput.mouse import Controller, Button
from PIL import ImageGrab
import numpy as np
import os

# Initialisation de la souris
mouse = Controller()

# Nombre de clics maximum
nbr = 0

# Charger l'image modèle
chemin_dossier = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(chemin_dossier, "Image.png")
image_template = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

if image_template is None:
    raise FileNotFoundError(f"Impossible de charger l'image : {image_path}")

# Fonction pour l'assistance à la visée
def AimAssiste():
    global nbr

    # Capture d'écran
    screenshot = ImageGrab.grab()
    screenshot = np.array(screenshot)

    # Convertir en format BGR pour OpenCV si nécessaire
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

    # Trouver la position de l'image modèle dans la capture d'écran
    result = cv2.matchTemplate(screenshot, image_template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Si une correspondance suffisante est trouvée
    if max_val >= 0.5:
        template_height, template_width = image_template.shape[:2]
        center_x = max_loc[0] + template_width // 2
        center_y = max_loc[1] + template_height // 2

        # Déplacer la souris et effectuer un clic
        mouse.position = (center_x, center_y)
        mouse.click(Button.left, 1)
        print(f"Clic effectué sur ({center_x}, {center_y})")
        nbr += 1

# Boucle principale
time.sleep(1)
while nbr < 100:
    AimAssiste()
    time.sleep(0.1)  # Pause pour réduire l'utilisation CPU

print("Programme terminé.")
