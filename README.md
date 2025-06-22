# RAG Leyes de Guerrero

Este proyecto descarga, indexa y permite consultar leyes y reglamentos del estado de Guerrero usando técnicas de RAG (Retrieval-Augmented Generation) con Python y LlamaIndex.

## Requisitos

- Python 3.9+ (recomendado usar un entorno virtual)
- [Ollama](https://ollama.com/) (para LLM local)
- Paquetes Python:
  - llama_index
  - llama-index-ollama
  - llama-index-embeddings-ollama
  - beautifulsoup4
  - requests
  - PyPDF2
  - streamlit

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

4. **(Opcional) Instala Ollama y descarga los modelos:**
   - [Descarga Ollama](https://ollama.com/download) y ejecuta:
     ```sh
     ollama serve
     ollama pull llama3:8b
     ollama pull all-minilm
     ```

## Instalación automática (opción recomendada)

Puedes instalar todo automáticamente ejecutando el script:

```sh
bash install.sh
```

Este script:
- Verifica tu versión de Python
- Crea y activa un entorno virtual
- Instala todas las dependencias
- Verifica que Ollama esté instalado y el modelo llama3:8b descargado

¡Verás mensajes de progreso y sabrás exactamente qué pasos faltan!

---

Si prefieres la instalación manual, sigue los pasos detallados más arriba.

## Notas sobre Ollama

- El paquete `llama-index-ollama` permite usar modelos locales de Ollama como LLM y para embeddings en tu pipeline de RAG.
- Asegúrate de tener Ollama corriendo (`ollama serve`) antes de ejecutar los scripts de indexado o consulta.

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
python build_index.py
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