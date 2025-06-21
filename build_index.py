import subprocess
import sys
import time
import requests
import shutil
import os

def check_ollama_running():
    try:
        r = requests.get("http://localhost:11434")
        return r.status_code == 200 or r.status_code == 404
    except Exception:
        return False

def start_ollama():
    # Intenta iniciar ollama serve en segundo plano
    try:
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Iniciando Ollama...")
        # Espera a que levante
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
    if not install_ollama():
        print("Por favor instala Ollama manualmente: https://ollama.com/download")
        sys.exit(1)

if not check_ollama_running():
    if not start_ollama():
        print("Por favor ejecuta 'ollama serve' en otra terminal.")
        sys.exit(1)

# --- RAG con LlamaIndex y Ollama ---
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama

Settings.llm = Ollama(model="llama3:8b")
Settings.embed_model = OllamaEmbedding(model_name="all-minilm")
Settings.chunk_size = 512
Settings.chunk_overlap = 50

print("🔎 Leyendo archivos PDF de ./leyes_guerrero ...")
pdf_files = [f for f in os.listdir("./leyes_guerrero") if f.lower().endswith(".pdf")]
print(f"Se encontraron {len(pdf_files)} archivos PDF.")
for i, fname in enumerate(pdf_files, 1):
    print(f"  [{i}/{len(pdf_files)}] {fname}")

print("📚 Cargando documentos...")
documents = SimpleDirectoryReader("./leyes_guerrero").load_data()
print(f"✅ {len(documents)} documentos cargados.")

print("⚡ Construyendo índice vectorial (esto puede tardar)...")
index = VectorStoreIndex.from_documents(documents)
print("✅ Índice construido.")

query_engine = index.as_query_engine(similarity_top_k=4)

if __name__ == "__main__":
    print("\nRAG lista. Escribe tu pregunta (Ctrl+C para salir):")
    while True:
        try:
            pregunta = input("Pregunta: ")
            print("⏳ Consultando...")
            respuesta = query_engine.query(pregunta)
            print(f"\nRespuesta:\n{respuesta}\n")
        except KeyboardInterrupt:
            print("\nSaliendo.")
            break
