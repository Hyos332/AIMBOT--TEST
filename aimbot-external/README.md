# aimbot-external - AZULES CLARITOS + AZUL ELÉCTRICO

## 🎯 DETECTA MÚLTIPLES AZULES
- **#209ed9** (azul claro base)
- **#0056ff** (azul eléctrico intenso) ⚡
- **Azules claritos** (cielo, cyan, agua)
- **Azules medio-intensos**

## Instalación
1. Crea un entorno virtual:
   ```
   py -m venv venv
   venv\Scripts\activate
   ```

2. Instala dependencias:
   ```
   pip install -r requirements.txt
   ```

## Uso
- **EJECUTA COMO ADMINISTRADOR**
- Ejecuta: `python main.py`
- **Tecla G**: Se centra en cualquier azul detectado

## ✨ COLORES QUE DETECTA ✨
- ⚡ **#0056ff** (azul eléctrico intenso)
- 🔵 **#209ed9** (azul claro base)
- 🔵 **Azul cielo** (#87CEEB)
- 🔵 **Cyan claro** (#87CEFA)
- 🔵 **Azul agua** (#B0E0E6)
- 🔵 **Azules medio-intensos**

## Rangos HSV configurados
- **Rango 1**: H=215-225, S=80-255, V=200-255 (azul eléctrico #0056ff)
- **Rango 2**: H=180-220, S=40-255, V=120-255 (azul claro #209ed9)
- **Rango 3**: H=160-200, S=30-255, V=100-255 (cyan claro)
- **Rango 4**: H=200-240, S=60-255, V=150-255 (azul medio-intenso)
- **Rango 5**: H=170-190, S=30-255, V=100-255 (azul cielo)

## Avisos
- Solo para propósitos educativos
- Ejecutar como administrador
- Detecta desde azules claros hasta azules intensos