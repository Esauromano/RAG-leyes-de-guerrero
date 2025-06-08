import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# URLs del menú (excepto Inicio)
menu_urls = [
    "https://congresogro.gob.mx/legislacion/leyes-ingresos-2024.php",
    "https://congresogro.gob.mx/legislacion/tabla-valores-2024.php",
    "https://congresogro.gob.mx/legislacion/leyes-ordinarias.php",
    "https://congresogro.gob.mx/legislacion/leyes-organicas.php",
    "https://congresogro.gob.mx/legislacion/codigos.php",
    "https://congresogro.gob.mx/legislacion/LEY-REGLAMENTARIA-DEL-EJERCICIO-PROFESIONAL-PARA-EL-ESTADO-LIBRE-Y-SOBERANO-DE-DE-GUERRERO.pdf",
    "https://congresogro.gob.mx/legislacion/CONSTITUCION-GUERRERO-15-06-2022.pdf"
]

# Carpeta base
base_dir = "leyes_guerrero"
os.makedirs(base_dir, exist_ok=True)

def download_pdf(url, output_folder):
    try:
        filename = os.path.basename(urlparse(url).path)
        output_path = os.path.join(output_folder, filename)
        if os.path.exists(output_path):
            print(f"Ya existe: {filename}")
            return
        print(f"Descargando: {url}")
        response = requests.get(url)
        response.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(response.content)
    except Exception as e:
        print(f"Error al descargar {url}: {e}")

for section_url in menu_urls:
    print(f"\n⏳ Procesando sección: {section_url}")
    if section_url.endswith(".pdf"):
        download_pdf(section_url, base_dir)
        continue

    try:
        response = requests.get(section_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        pdf_links = [urljoin(section_url, a['href']) for a in soup.find_all("a", href=True) if a['href'].lower().endswith(".pdf")]

        if not pdf_links:
            print("⚠️  No se encontraron PDFs en esta sección.")
        for pdf_url in pdf_links:
            download_pdf(pdf_url, base_dir)
    except Exception as e:
        print(f"Error al procesar {section_url}: {e}")
