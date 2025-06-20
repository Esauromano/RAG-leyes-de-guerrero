import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

clasificaciones = [
    "acuerdos", "acuerdos-abrogados", "codigos", "codigos-abrogados",
    "constitucion-federal-y-estatal", "convenios", "decreto", "decretos-abrogados",
    "decretos-entidades-paraestatales", "decretos-establecimientos-publicos-de-bienestar-social",
    "decretos-expropiatorios", "ley-de-ingresos-del-estado-de-guerrero-para-el-ejercicio-fiscal-2023",
    "leyes-abrogadas", "leyes-ordinarias", "leyes-organicas", "leyes-reglamentarias",
    "lineamientos", "lineamientos-abrogados", "planes", "programas", "protocolo",
    "reglamentos", "reglamentos-abrogados", "reglamentos-de-leyes",
    "reglamentos-de-organismos-publicos-autonomos", "reglamentos-interiores-de-entidades-paraestatales",
    "reglamentos-interiores-de-establecimientos-publicos-de-bienestar-social",
    "reglamentos-interiores-de-organos-administrativos-desconcentrados",
    "reglamentos-interiores-de-dependencias", "reglas-de-operacion", "reglas-de-operacion-abrogadas"
]

base_url = "https://www.guerrero.gob.mx/leyes-y-reglamentos/"
output_folder = "leyes_guerrero"
os.makedirs(output_folder, exist_ok=True)

def download_pdf(url, output_folder):
    filename = os.path.basename(urlparse(url).path)
    output_path = os.path.join(output_folder, filename)
    if os.path.exists(output_path):
        print(f"Ya existe: {filename}")
        return False
    print(f"Descargando: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"Error al descargar {url}: {e}")
        return False

for clasificacion in clasificaciones:
    print(f"\n🔎 Procesando clasificación: {clasificacion}")
    params = {"clasificacion": clasificacion}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        tabla = soup.find("tbody", class_="lista-leyes")
        if not tabla:
            print("⚠️  No se encontró la tabla de leyes para esta clasificación.")
            continue
        enlaces = tabla.find_all("a", href=True)
        pdf_links = [a["href"] for a in enlaces if a["href"].lower().endswith(".pdf")]
        archivos_existentes = set(os.listdir(output_folder))
        pendientes = []
        descargados = 0
        omitidos = 0
        for pdf_url in pdf_links:
            filename = os.path.basename(urlparse(pdf_url).path)
            if filename in archivos_existentes:
                print(f"Ya existe: {filename}")
                omitidos += 1
                continue
            pendientes.append(filename)
            if download_pdf(pdf_url, output_folder):
                descargados += 1
        print(f"Resumen {clasificacion}: {descargados} nuevos, {omitidos} ya existían.")
        if pendientes:
            print("Archivos pendientes en esta clasificación:")
            for p in pendientes:
                print(f"  - {p}")
        else:
            print("Todos los archivos de esta clasificación ya están descargados.")
    except Exception as e:
        print(f"Error al procesar {clasificacion}: {e}")
