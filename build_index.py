#!/usr/bin/env python3  # Permite ejecutar el script directamente desde la terminal

import subprocess      # Para ejecutar comandos del sistema
import sys            # Para salir del script si es necesario
import time           # Para esperar entre intentos de conexión
import requests       # Para hacer peticiones HTTP y verificar Ollama
import shutil         # Para verificar si un ejecutable existe en el sistema
import os             # Para operaciones con archivos y carpetas

# Función para verificar si Ollama está corriendo en localhost:11434
def check_ollama_running():
    try:
        r = requests.get("http://localhost:11434")
        # Ollama responde 200 si está corriendo, 404 si no hay endpoint, ambos indican que el servidor está activo
        return r.status_code == 200 or r.status_code == 404
    except Exception:
        return False

# Función para intentar iniciar Ollama en segundo plano
def start_ollama():
    try:
        # Inicia 'ollama serve' en segundo plano, sin mostrar salida
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Iniciando Ollama...")
        # Espera hasta 10 segundos a que Ollama esté disponible
        for _ in range(10):
            if check_ollama_running():
                print("Ollama está corriendo.")
                return True
            time.sleep(1)
        print("No se pudo iniciar Ollama automáticamente.")
        return False
    except Exception as e:
        print(f"Error al intentar iniciar Ollama: {e}")
        return False

# Función para instalar Ollama usando Homebrew (solo Mac)
def install_ollama():
    print("Ollama no está instalado. Instalando con Homebrew...")
    try:
        subprocess.check_call(["brew", "install", "ollama"])
        print("Ollama instalado.")
        return True
    except Exception as e:
        print(f"No se pudo instalar Ollama automáticamente: {e}")
        return False

# --- Chequeo e inicio de Ollama ---
if not shutil.which("ollama"):
    # Si Ollama no está instalado, intenta instalarlo
    if not install_ollama():
        print("Por favor instala Ollama manualmente: https://ollama.com/download")
        sys.exit(1)

if not check_ollama_running():
    # Si Ollama no está corriendo, intenta iniciarlo
    if not start_ollama():
        print("Por favor ejecuta 'ollama serve' en otra terminal.")
        sys.exit(1)

# --- RAG con LlamaIndex y Ollama ---
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama

# Configura el modelo LLM y el modelo de embeddings de Ollama
Settings.llm = Ollama(model="llama3:8b")
Settings.embed_model = OllamaEmbedding(model_name="all-minilm")
Settings.chunk_size = 512
Settings.chunk_overlap = 50

# Lee la lista de archivos PDF en la carpeta ./leyes_guerrero
print("🔎 Leyendo archivos PDF de ./leyes_guerrero ...")
pdf_files = [f for f in os.listdir("./leyes_guerrero") if f.lower().endswith(".pdf")]
print(f"Se encontraron {len(pdf_files)} archivos PDF.")
for i, fname in enumerate(pdf_files, 1):
    print(f"  [{i}/{len(pdf_files)}] {fname}")

# Carga los documentos PDF usando LlamaIndex
print("📚 Cargando documentos...")
documents = SimpleDirectoryReader("./leyes_guerrero").load_data()
print(f"✅ {len(documents)} documentos cargados.")

# Construye el índice vectorial a partir de los documentos
print("⚡ Construyendo índice vectorial (esto puede tardar)...")
index = VectorStoreIndex.from_documents(documents)
print("✅ Índice construido.")

# Prepara el motor de consulta (query engine)
query_engine = index.as_query_engine(similarity_top_k=4)

# Bucle interactivo para hacer preguntas al índice
if __name__ == "__main__":
    print("\nRAG lista. Escribe tu pregunta (Ctrl+C para salir):")
    while True:
        try:
            pregunta = input("Pregunta: ")           # Solicita una pregunta al usuario
            print("⏳ Consultando...")               # Mensaje de espera
            respuesta = query_engine.query(pregunta) # Consulta el índice
            print(f"\nRespuesta:\n{respuesta}\n")    # Muestra la respuesta
        except KeyboardInterrupt:                    # Permite salir con Ctrl+C
            print("\nSaliendo.")
            break
