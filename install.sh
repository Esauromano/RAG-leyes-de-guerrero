#!/bin/bash

# Modern, verbose, and user-friendly installer for RAG Leyes de Guerrero

set -e

# Colors
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
RED='\033[1;31m'
NC='\033[0m' # No Color

step() {
  echo -e "${BLUE}[$1/${TOTAL}]${NC} ${YELLOW}$2...${NC}"
}

success() {
  echo -e "${GREEN}✔ $1${NC}"
}

fail() {
  echo -e "${RED}✖ $1${NC}"
  exit 1
}

TOTAL=6
CURRENT=1

echo -e "${GREEN}🚀 Instalador de RAG Leyes de Guerrero${NC}"
echo "-----------------------------------------"

# Paso 1: Verificar Python
step $CURRENT "Verificando Python 3.9+"
if command -v python3 &>/dev/null; then
  PYV=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:3])))')
  if [[ "$PYV" < "3.9" ]]; then
    fail "Python 3.9+ requerido. Encontrado: $PYV"
  fi
  success "Python $PYV encontrado"
else
  fail "Python 3.9+ no encontrado. Instálalo antes de continuar."
fi
((CURRENT++))

# Paso 2: Crear entorno virtual
step $CURRENT "Creando entorno virtual (.venv)"
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
  success "Entorno virtual creado"
else
  success "Entorno virtual ya existe"
fi
((CURRENT++))

# Paso 3: Activar entorno virtual
step $CURRENT "Activando entorno virtual"
source .venv/bin/activate
success "Entorno virtual activado"
((CURRENT++))

# Paso 4: Instalar dependencias
step $CURRENT "Instalando dependencias de Python"
pip install --upgrade pip
pip install -r requirements.txt
success "Dependencias instaladas"
((CURRENT++))

# Paso 5: Verificar Ollama
step $CURRENT "Verificando instalación de Ollama"
if ! command -v ollama &>/dev/null; then
  echo -e "${YELLOW}Ollama no encontrado. Descárgalo de https://ollama.com/download e instálalo antes de continuar.${NC}"
  fail "Ollama no instalado"
else
  success "Ollama encontrado"
fi
((CURRENT++))

# Paso 6: Descargar modelo llama3:8b si no existe
step $CURRENT "Verificando modelo llama3:8b en Ollama"
if ! ollama list | grep -q "llama3:8b"; then
  echo -e "${YELLOW}Descargando modelo llama3:8b...${NC}"
  ollama pull llama3:8b
  success "Modelo llama3:8b descargado"
else
  success "Modelo llama3:8b ya está disponible"
fi

echo -e "${GREEN}\n🎉 Instalación completada con éxito.${NC}"
echo -e "${BLUE}Ahora puedes ejecutar:${NC} ${YELLOW}python 1by1.py${NC} o ${YELLOW}python congresogro-gob-mx-crawler.py${NC}"