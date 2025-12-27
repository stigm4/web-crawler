import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import time
import argparse
import sys
import os

# --- COLORES ---
CELESTE = '\033[96m'
RESET = '\033[0m'

# --- BANNER ACTUALIZADO ---
BANNER = f"""{CELESTE}
                                                                                                    
 sssssss  A  sssssss     ssssssssssssssssssssssssss  A ss   ssssssssssssssssxssssssssssssss
 sssssss AAA   sssss AAA   ssssssssssssss   sssssss AA ss A ssshttpssssssssss NA A   ssssss
 swebos  A AAA   sss  A AA   sosos   sss  A ssosos  A  s  A ssososososososso   AAAAA   soso
 ssssss WA   AAx   s  A  AAA  ssss A   s AA    sss AA ss AA ssssssss      ssss AA   AA ssss
 sssss  AA s    AA s AA   AAA sss  AAA s EA  A     AA ss AA sssssss  AAAA  ss  AA   AA ssss
 ssx   AA  ssss    s jAAAA  A s   oA A   AA  AAA   A  ss AA ssoso   AA  AA    AA   AA  ssos
 ssxaAAAA  sssssssss AAAAA    s AAAAAAAAAAA  EA   A  sss AA sssss AAAAAAAAAA  AA  AA  sssss
 ssx   AAa  ssssssss AA  AAA     AA   A  AA  AAA AA  sss AA sssss  A          AA  AA sssoss
 ssssx   AA   ss   s AA    AAA  AA  s AA AA AA A A  sso  Ax        Af sssssss AAAAA  ssssso
 ssssss   AAA    A s AA ss  A  AA  ss  AAAAAA  AAA sss   AAAAAAAAA A    sssss AaAA  ssossss
 ssosssss   AA AA  s  A sss   AAA  sss AAAA    AA  sss SAA          AAA   sos A  A  ssssoss
 dataosssss  AA   ss  A ssss AA   ssos   AAA s    ssos     xsssssss   AAA sss    A  sssssso
 ssssssoss  AA  sssss   ssos    ssssssss     ssssssssssssssssssssssss     ssssss   xssossss
 ssossssss A   xssosssssssssssssssosssssssssssssssosss.orgssososossssssssssossssssssssssoss
 ssssossos   sssssssosssosssssssoshttpossssssosossssososososssssssossssssssssossssssossssso
 
                                                                          v1.0 por stigma
{RESET}"""

# Dominios de redes sociales y plataformas comunes para ignorar
REDES_SOCIALES_POR_DEFECTO = [
    'facebook.com', 'instagram.com', 'twitter.com', 'x.com', 'linkedin.com', 
    'youtube.com', 'youtu.be', 'tiktok.com', 'pinterest.com', 'reddit.com', 
    'whatsapp.com', 'wa.me', 'telegram.org', 't.me', 'snapchat.com', 
    'tumblr.com', 'twitch.tv', 'discord.com', 'discord.gg', 'quora.com', 
    'flickr.com', 'vimeo.com', 'medium.com', 'behance.net', 'dribbble.com',
    'github.com', 'bitbucket.org', 'gitlab.com', 'slack.com', 'threads.net'
]

def obtener_dominio(url):
    dominio = urlparse(url).netloc.lower()
    if dominio.startswith("www."):
        return dominio[4:]
    return dominio

def cargar_exclusiones(ruta_archivo):
    exclusiones = set(REDES_SOCIALES_POR_DEFECTO)
    if ruta_archivo and os.path.exists(ruta_archivo):
        try:
            with open(ruta_archivo, 'r') as f:
                for linea in f:
                    limpia = linea.strip().lower()
                    if limpia:
                        exclusiones.add(limpia)
            print(f"[*] Exclusiones adicionales cargadas desde: {ruta_archivo}")
        except Exception as e:
            print(f"[!] Error al leer exclusiones: {e}")
    return exclusiones

def es_valida(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def crawler(url_inicial, archivo_salida, exclusiones, limite, delay):
    dominio_principal = obtener_dominio(url_inicial)
    if not dominio_principal:
        print("Error: La URL inicial no es válida.")
        return

    urls_por_visitar = [url_inicial]
    urls_visitadas = set()
    dominios_encontrados = set()
    paginas_procesadas = 0

    print(f"\n{CELESTE}{'='*75}{RESET}")
    print(f" OBJETIVO: {url_inicial}")
    print(f" LÍMITE: {limite} páginas | DELAY: {delay}s")
    print(f"{CELESTE}{'='*75}{RESET}\n")

    try:
        while urls_por_visitar and paginas_procesadas < limite:
            url_actual = urls_por_visitar.pop(0)
            if url_actual in urls_visitadas:
                continue

            print(f"[{paginas_procesadas+1}] Rastreando: {url_actual}")
            
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'}
                respuesta = requests.get(url_actual, headers=headers, timeout=10)
                urls_visitadas.add(url_actual)
                paginas_procesadas += 1

                if "text/html" not in respuesta.headers.get('Content-Type', ''):
                    continue

                soup = BeautifulSoup(respuesta.text, 'html.parser')
                for a_tag in soup.find_all("a", href=True):
                    href = a_tag.get("href")
                    url_completa = urljoin(url_actual, href)
                    
                    if es_valida(url_completa):
                        dom = obtener_dominio(url_completa)
                        if dom:
                            # Filtrar redes sociales y el dominio base (opcional)
                            if not any(excl in dom for excl in exclusiones):
                                dominios_encontrados.add(dom)
                            
                            # Recursividad: solo seguir links del mismo sitio
                            if dom == dominio_principal and url_completa not in urls_visitadas:
                                if url_completa not in urls_por_visitar:
                                    urls_por_visitar.append(url_completa)
                time.sleep(delay)
            except Exception as e:
                print(f"    [!] Error en {url_actual}: {e}")

    except KeyboardInterrupt:
        print(f"\n{CELESTE}[!] Escaneo interrumpido. Guardando datos...{RESET}")

    try:
        with open(archivo_salida, "w") as f:
            for d in sorted(list(dominios_encontrados)):
                f.write(d + "\n")
        print(f"\n{CELESTE}{'='*75}{RESET}")
        print(f" COMPLETADO: {len(dominios_encontrados)} dominios únicos extraídos.")
        print(f" RESULTADOS: {archivo_salida}")
        print(f"{CELESTE}{'='*75}{RESET}")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=BANNER + "\nCrawler profesional para extraer dominios únicos ignorando redes sociales.",
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False
    )
    
    parser.add_argument("-h", "--help", action="help", help="Muestra el banner y la ayuda.")
    parser.add_argument("-u", "--url", required=True, help="URL inicial (ej: https://target.com)")
    parser.add_argument("-o", "--output", default="dominios.txt", help="Archivo de salida (default: dominios.txt)")
    parser.add_argument("-e", "--excludes", help="Archivo .txt con dominios extra a ignorar.")
    parser.add_argument("-l", "--limit", type=int, default=100, help="Límite de páginas a navegar (default: 100)")
    parser.add_argument("-d", "--delay", type=float, default=1.0, help="Segundos entre peticiones (default: 1.0)")

    if len(sys.argv) == 1:
        print(BANNER)
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    # Mostrar banner siempre al iniciar
    print(BANNER)
    
    # Cargar lista de ignorados e iniciar
    excl = cargar_exclusiones(args.excludes)
    crawler(args.url, args.output, excl, args.limit, args.delay)
