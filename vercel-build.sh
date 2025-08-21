#!/bin/bash

# Script de build personalizado para Vercel
echo "🚀 Iniciando build do Musickera Player..."

# Criar diretórios necessários
mkdir -p /tmp/musics
mkdir -p /tmp/covers

# Copiar arquivos estáticos se existirem
if [ -d "musics/covers" ]; then
    echo "📁 Copiando capas de álbuns..."
    cp -r musics/covers/* /tmp/covers/ 2>/dev/null || true
fi

# Verificar se a API está configurada corretamente
if [ -f "api/index.py" ]; then
    echo "✅ API configurada corretamente"
else
    echo "❌ Erro: api/index.py não encontrado"
    exit 1
fi

# Verificar dependências
if [ -f "api/requirements.txt" ]; then
    echo "📦 Instalando dependências Python..."
    pip install -r api/requirements.txt
else
    echo "❌ Erro: api/requirements.txt não encontrado"
    exit 1
fi

echo "✅ Build concluído com sucesso!"
