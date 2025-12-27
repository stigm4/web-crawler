# 🕸️ Web Domain Crawler v1.0
![Web-Crawler](https://raw.githubusercontent.com/stigm4/project-images/refs/heads/main/crawler.png).

**Web Domain Crawler** es una herramienta de reconocimiento (OSINT) y auditoría web escrita en Python. Su objetivo principal es mapear la superficie de ataque o la estructura de enlaces de un sitio web, extrayendo todos los dominios únicos externos e internos, mientras filtra activamente el "ruido" de las redes sociales.



## ✨ Características Principales
- **⚡ Filtrado de Redes Sociales**: Lista negra integrada con más de 30 plataformas (Facebook, X, TikTok, Discord, etc.).
- **🔄 Recursividad Inteligente**: Explora enlaces internos automáticamente para encontrar dominios ocultos en páginas secundarias.
- **🛡️ Evasión Básica**: Utiliza Headers de un navegador real (`User-Agent`) para evitar bloqueos inmediatos.
- **📂 Exclusiones Externas**: Soporta un archivo `excludes.txt` para que el usuario ignore dominios especificados.
- **🎨 Interfaz Estilizada**: Banner ASCII personalizado en color celeste y reportes de progreso en tiempo real.
- **💾 Persistencia**: Si detienes el escaneo con `Ctrl+C`, el script guarda automáticamente lo que haya encontrado hasta el momento.
  
---

## 🛠️ Arquitectura y Funcionamiento
El crawler funciona siguiendo este flujo:
1. **Normalización**: Limpia la URL objetivo y extrae el dominio base.
2. **Extracción**: Descarga el código HTML y localiza todas las etiquetas `<a>`.
3. **Validación**: Convierte links relativos en absolutos y verifica que sean URLs válidas.
4. **Clasificación**: 
   - Si el link es del **mismo dominio**, lo añade a la cola para seguir "escarbando".
   - Si el link es **externo**, extrae el dominio y lo guarda (si no está en la lista negra).
5. **Prevención de Bucles**: Mantiene un registro de URLs visitadas para no entrar en ciclos infinitos.

---

## 🔧 Instalación y Setup

### 1. Preparar el entorno
Se recomienda el uso de un entorno virtual para mantener limpio tu sistema:
```bash
# Crear entorno
python -m venv venv

# Activar (Windows)
.\venv\Scripts\activate

# Activar (Linux/Mac)
source venv/bin/activate
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```
---

## 🚀 Uso
### Comando Básico
```bash
python web-crawler.py -u https://ejemplo.com -o resultados.txt -l 50
```
### Escaneo Avanzado con Exclusiones
Si quieres ignorar dominios como google.com o amazon.com, crea un archivo excludes.txt y ejecútalo así:
```bash
python web-crawler.py -u https://sitio-objetivo.com -o salida.txt -e excludes.txt -l 200 -d 0.5
```
### Argumentos:
* `-u, --url`: URL inicial (TARGET).
* `-o, --output`: Nombre del archivo de salida (Default: dominios.txt).
* `-e, --excludes`: Archivo con dominios extra a ignorar.
* `-l, --limit`: Límite de páginas a rastrear (Default: 100).
* `-d, --delay`: Segundos entre peticiones (Default: 1.0).

## 📝 Ejemplo de excludes.txt
Puedes crear este archivo para omitir dominios que no te interesen:
```text
google.com
gstatic.com
doubleclick.net
amazon.es
```
---
## ⚖️ Aviso Legal (Disclaimer)
Esta herramienta fue creada con fines educativos y de auditoría ética. El autor no se hace responsable del mal uso de este software. Realizar peticiones masivas a un sitio web sin autorización puede ser considerado una actividad hostil. Respeta siempre el archivo robots.txt y los términos de servicio del sitio objetivo.

---

Desarrollado con ❤️ por estigma.
