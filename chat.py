#!/usr/bin/env python3  # Indica que el script debe ejecutarse con Python 3

from llama_index.core import StorageContext, load_index_from_storage  # Importa funciones para cargar el índice persistido
from llama_index.embeddings.ollama import OllamaEmbedding      # Importa el wrapper de embeddings de Ollama
from llama_index.llms.ollama import Ollama                    # Importa el wrapper del LLM de Ollama
from llama_index.core import Settings                         # Permite configurar los modelos globalmente

# Configura el LLM y los embeddings de Ollama con un timeout extendido
Settings.llm = Ollama(model="llama3:8b", request_timeout=300)  # 300 segundos de timeout
Settings.embed_model = OllamaEmbedding(model_name="all-minilm") # Usa el modelo de embeddings local de Ollama

INDEX_DIR = "./storage"  # Carpeta donde se guarda el índice vectorial

# Carga el índice existente desde disco usando el contexto de almacenamiento
storage_context = StorageContext.from_defaults(persist_dir=INDEX_DIR)
index = load_index_from_storage(storage_context)

# Activa el modo streaming
query_engine = index.as_query_engine(similarity_top_k=4, streaming=True)

if __name__ == "__main__":  # Solo ejecuta esto si el script es el principal
    print("\nRAG lista. Escribe tu pregunta (Ctrl+C para salir):")
    while True:  # Bucle infinito para el chat interactivo
        try:
            pregunta = input("Pregunta: ")  # Solicita una pregunta al usuario
            print("⏳ Consultando...\n")      # Muestra mensaje de espera
            # El método .query ahora devuelve un generador de tokens
            response_stream = query_engine.query(pregunta)
            for token in response_stream.response_gen:
                print(token, end="", flush=True)  # Muestra cada token conforme llega
            print("\n")
        except KeyboardInterrupt:  # Si el usuario presiona Ctrl+C
            print("\nSaliendo.")   # Muestra mensaje de salida
            break                  # Sale del bucle