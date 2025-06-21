# RAG Leyes de Guerrero

Este proyecto descarga, indexa y permite consultar leyes y reglamentos del estado de Guerrero usando técnicas de RAG (Retrieval-Augmented Generation) con Python y LlamaIndex.

## Requisitos

- Python 3.9+ (recomendado usar un entorno virtual)
- [Ollama](https://ollama.com/) (para LLM local, opcional si usas OpenAI)
- Paquetes Python (ver abajo)

## Instalación

1. **Clona el repositorio:**
   ```sh
   git clone https://github.com/Esauromano/RAG-leyes-de-guerrero.git
   cd RAG-leyes-de-guerrero
   ```

2. **Crea y activa un entorno virtual (opcional pero recomendado):**
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Instala las dependencias:**
   ```sh
   pip install -r requirements.txt
   ```

4. **(Opcional) Instala Ollama y descarga el modelo:**
   - [Descarga Ollama](https://ollama.com/download) y ejecuta:
     ```sh
     ollama serve
     ollama pull llama3:8b
     ```

## Descarga de PDFs

Para descargar todos los PDFs de leyes y reglamentos ejecuta:

```sh
python congresogro-gob-mx-crawler.py
```
o
```sh
python guerrerogob-mx-Crawler.py
```

Los archivos se guardarán en la carpeta `leyes_guerrero`.

## Indexación de documentos

Para indexar los PDFs y construir el RAG ejecuta:

```sh
python 1by1.py
```

Este script:
- Indexa los PDFs de la carpeta `leyes_guerrero`
- Guarda el índice en la carpeta `storage`
- Permite reanudar si el proceso se interrumpe

## Consulta interactiva

Al terminar la indexación, el script te permitirá hacer preguntas en la terminal, por ejemplo:

```
RAG lista. Escribe tu pregunta (Ctrl+C para salir):
Pregunta: ¿Cuál es la ley más reciente sobre turismo?
```

## Notas

- Si quieres volver a indexar desde cero, borra la carpeta `storage` y el archivo `indexed_files.json`.
- Puedes ajustar el número de hilos de carga en `1by1.py` modificando la variable `MAX_PARALLEL`.
- Si usas OpenAI en vez de Ollama, ajusta la configuración en el script.

## Estructura del proyecto

```
/leyes_guerrero         # PDFs descargados
/storage                # Índice vectorial persistente
/indexed_files.json     # Registro de PDFs ya indexados
congresogro-gob-mx-crawler.py
guerrerogob-mx-Crawler.py
1by1.py
requirements.txt
```