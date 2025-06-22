#!/usr/bin/env python3  # Indica que el script debe ejecutarse con Python 3

from llama_index.core import StorageContext, load_index_from_storage  # Importa funciones para cargar el índice persistido
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core import Settings

INDEX_DIR = "./storage"  # Carpeta donde se guarda el índice vectorial

Settings.llm = Ollama(model="llama3:8b")
Settings.embed_model = OllamaEmbedding(model_name="all-minilm")

# Carga el índice existente desde disco usando el contexto de almacenamiento
storage_context = StorageContext.from_defaults(persist_dir=INDEX_DIR)
index = load_index_from_storage(storage_context)

# Crea el motor de consulta (query engine) con los parámetros deseados
query_engine = index.as_query_engine(similarity_top_k=4)

if __name__ == "__main__":  # Solo ejecuta esto si el script es el principal
    print("\nRAG lista. Escribe tu pregunta (Ctrl+C para salir):")
    while True:  # Bucle infinito para el chat interactivo
        try:
            pregunta = input("Pregunta: ")  # Solicita una pregunta al usuario
            print("⏳ Consultando...")      # Muestra mensaje de espera
            respuesta = query_engine.query(pregunta)  # Consulta el índice con la pregunta
            print(f"\nRespuesta:\n{respuesta}\n")     # Muestra la respuesta
        except KeyboardInterrupt:  # Si el usuario presiona Ctrl+C
            print("\nSaliendo.")   # Muestra mensaje de salida
            break