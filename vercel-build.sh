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

# Verificar sintaxe Python
echo "🔍 Verificando sintaxe Python..."
python -m py_compile api/index.py
if [ $? -eq 0 ]; then
    echo "✅ Sintaxe Python válida"
else
    echo "❌ Erro de sintaxe Python"
    exit 1
fi

# Verificar se o arquivo de configuração existe
if [ -f "api/config.py" ]; then
    echo "✅ Arquivo de configuração encontrado"
else
    echo "❌ Erro: api/config.py não encontrado"
    exit 1
fi

echo "✅ Build concluído com sucesso!"
