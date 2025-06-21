import os
import json
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings, StorageContext, load_index_from_storage, Document
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from concurrent.futures import ThreadPoolExecutor, as_completed

INDEX_DIR = "./storage"
DONE_FILE = "indexed_files.json"

Settings.llm = Ollama(model="llama3:8b", request_timeout=120)
Settings.embed_model = OllamaEmbedding(model_name="all-minilm")
Settings.chunk_size = 512
Settings.chunk_overlap = 50

def load_pdf(path):
    try:
        docs = SimpleDirectoryReader(input_files=[path]).load_data()
        return docs, os.path.basename(path), None
    except Exception as e:
        return [], os.path.basename(path), e

# Cargar lista de archivos ya indexados
if os.path.exists(DONE_FILE):
    with open(DONE_FILE, "r") as f:
        indexed_files = set(json.load(f))
else:
    indexed_files = set()

if os.path.exists(INDEX_DIR):
    print("🔄 Cargando índice existente...")
    storage_context = StorageContext.from_defaults(persist_dir=INDEX_DIR)
    index = load_index_from_storage(storage_context)
else:
    print("🆕 Creando nuevo índice...")
    index = VectorStoreIndex([])

print("🔎 Leyendo archivos PDF de ./leyes_guerrero ...")
pdf_files = [f for f in os.listdir("./leyes_guerrero") if f.lower().endswith(".pdf")]
print(f"Se encontraron {len(pdf_files)} archivos PDF.")

# Filtrar los que ya están indexados
to_process = [f for f in pdf_files if f not in indexed_files]
print(f"Quedan {len(to_process)} archivos por indexar.")

MAX_PARALLEL = min(16, os.cpu_count() * 2)
print(f"📌 Usando {MAX_PARALLEL} hilos para carga de PDFs.")

with ThreadPoolExecutor(max_workers=MAX_PARALLEL) as executor:
    futures = [executor.submit(load_pdf, os.path.join("./leyes_guerrero", fname)) for fname in to_process]
    persist_interval = 100
    for i, future in enumerate(as_completed(futures), 1):
        docs, fname, err = future.result()
        if err:
            print(f"  [{i}/{len(to_process)}] {fname} ERROR: {err}")
        else:
            print(f"  [{i}/{len(to_process)}] {fname} cargado ({len(docs)} documento(s)), indexando...")
            for doc in docs:
                index.insert(doc)
            indexed_files.add(fname)
            # Guardar progreso incrementalmente cada N archivos
            if i % persist_interval == 0 or i == len(to_process):
                index.storage_context.persist(persist_dir=INDEX_DIR)
                with open(DONE_FILE, "w") as f:
                    json.dump(list(indexed_files), f)
            print(f"  {fname} indexado y guardado.")

print("✅ Todos los archivos pendientes han sido indexados y guardados.")

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