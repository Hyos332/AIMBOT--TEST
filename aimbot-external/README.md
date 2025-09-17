# aimbot-external (solo para pruebas locales)

## Instalación
1. Crea un entorno virtual (recomendado):
   ```
   python -m venv venv
   venv\Scripts\activate   (Windows)
   ```

2. Instala dependencias:
   ```
   pip install -r requirements.txt
   ```

## Uso
- Ajusta valores en `config.yaml` (fov, speed, hsv_lower, hsv_upper) o responde al prompt si no existe el archivo.
- Ejecuta:
   ```
   python main.py
   ```
- Mantén pulsado el botón izquierdo del ratón para que el script capture y haga correcciones en la mira.

## Avisos
- No uses en partidas online (riesgo de baneo).
- Ejecutar con privilegios puede ser necesario para interacción con algunos juegos.