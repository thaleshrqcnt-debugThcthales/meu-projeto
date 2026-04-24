#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Arquivo .env criado. Configure sua ANTHROPIC_API_KEY em .env antes de continuar."
fi

if [ ! -d ".venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv .venv
fi

source .venv/bin/activate
echo "Instalando dependências..."
pip install -r requirements.txt -q

mkdir -p app/data app/exports app/uploads

echo ""
echo "======================================="
echo " FLOW EDITOR — Sistema Operacional"
echo " Projetos Culturais"
echo "======================================="
echo " Acesse: http://127.0.0.1:8000"
echo "======================================="
echo ""

uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
