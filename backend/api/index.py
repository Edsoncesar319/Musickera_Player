import os
import json
import re
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from typing import Optional, Dict
import mimetypes
from config import config

# Configuração para Vercel
app = Flask(__name__)
app.config.from_object(config['production'])

# Configurar CORS com origens específicas
CORS(app, origins=app.config['CORS_ORIGINS'])

# Ensure correct audio MIME types
mimetypes.add_type('audio/webm', '.webm')
mimetypes.add_type('audio/mp4', '.m4a')
mimetypes.add_type('audio/aac', '.aac')

# Para Vercel, vamos usar variáveis de ambiente ou valores padrão
MUSIC_DIR = os.environ.get('MUSIC_DIR', '/tmp/musics')
COVERS_DIR = os.environ.get('COVERS_DIR', '/tmp/covers')

@app.route('/api/musics', methods=['GET'])
def get_musics():
    """Lista todas as músicas disponíveis"""
    try:
        # Para Vercel, vamos retornar uma lista estática das músicas
        # ou implementar uma solução baseada em banco de dados
        musics = [
            {
                "id": 1,
                "title": "Acima do Sol (Ao Vivo)",
                "artist": "Jota Quest",
                "filename": "Acima do Sol (Ao Vivo).m4a",
                "cover": "/musics/covers/Acima_do_Sol_Ao_Vivo_.jpg",
                "duration": "3:45"
            },
            {
                "id": 2,
                "title": "Epitáfio",
                "artist": "Titãs",
                "filename": "Epitáfio.m4a",
                "cover": "/musics/covers/Epit_fio.jpg",
                "duration": "4:15"
            },
            {
                "id": 3,
                "title": "Fácil",
                "artist": "Jota Quest",
                "filename": "Fácil.m4a",
                "cover": "/musics/covers/F_cil.jpg",
                "duration": "3:30"
            },
            {
                "id": 4,
                "title": "Jackie Tequila",
                "artist": "Jota Quest",
                "filename": "Jackie Tequila.m4a",
                "cover": "/musics/covers/Jackie_Tequila.jpg",
                "duration": "4:20"
            },
            {
                "id": 5,
                "title": "Resposta",
                "artist": "Jota Quest",
                "filename": "Resposta.m4a",
                "cover": "/musics/covers/Resposta.jpg",
                "duration": "3:55"
            },
            {
                "id": 6,
                "title": "Só Hoje (Acústico)",
                "artist": "Jota Quest",
                "filename": "Só Hoje (Acústico).m4a",
                "cover": "/musics/covers/S_Hoje_Ac_stico_.jpg",
                "duration": "4:10"
            },
            {
                "id": 7,
                "title": "Te Ver",
                "artist": "Jota Quest",
                "filename": "Te Ver.mp4",
                "cover": "/musics/covers/Te_Ver.jpg",
                "duration": "3:40"
            },
            {
                "id": 8,
                "title": "Tempos Modernos (Estúdio)",
                "artist": "Jota Quest",
                "filename": "Tempos Modernos (Estúdio).m4a",
                "cover": "/musics/covers/Tempos_Modernos_Est_dio_.jpg",
                "duration": "4:05"
            },
            {
                "id": 9,
                "title": "Vamos Fugir",
                "artist": "Jota Quest",
                "filename": "Vamos Fugir.m4a",
                "cover": "/musics/covers/Vamos_Fugir.jpg",
                "duration": "3:50"
            },
            {
                "id": 10,
                "title": "Vou Deixar",
                "artist": "Jota Quest",
                "filename": "Vou Deixar.m4a",
                "cover": "/musics/covers/Vou_Deixar.jpg",
                "duration": "4:00"
            }
        ]
        
        return jsonify({
            "success": True,
            "musics": musics,
            "total": len(musics)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/search', methods=['GET'])
def search_musics():
    """Busca músicas por termo"""
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify({
            "success": False,
            "error": "Termo de busca é obrigatório"
        }), 400
    
    try:
        # Implementar busca nas músicas
        all_musics = [
            {
                "id": 1,
                "title": "Acima do Sol (Ao Vivo)",
                "artist": "Jota Quest",
                "filename": "Acima do Sol (Ao Vivo).m4a",
                "cover": "/musics/covers/Acima_do_Sol_Ao_Vivo_.jpg",
                "duration": "3:45"
            },
            # ... outras músicas
        ]
        
        # Filtrar por termo de busca
        results = []
        for music in all_musics:
            if (query in music['title'].lower() or 
                query in music['artist'].lower()):
                results.append(music)
        
        return jsonify({
            "success": True,
            "results": results,
            "query": query,
            "total": len(results)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Verificação de saúde da API"""
    return jsonify({
        "status": "healthy",
        "service": "Musickera API",
        "version": "1.0.0"
    })

@app.route('/api/playlist', methods=['GET'])
def get_playlist():
    """Retorna playlist padrão"""
    try:
        playlist = [
            {
                "id": 1,
                "name": "Jota Quest Hits",
                "description": "Melhores músicas do Jota Quest",
                "musics": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            }
        ]
        
        return jsonify({
            "success": True,
            "playlists": playlist
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Rota para servir arquivos estáticos (músicas e capas)
@app.route('/musics/<path:filename>')
def serve_music(filename):
    """Serve arquivos de música"""
    try:
        # Para Vercel, você pode usar um CDN ou armazenamento externo
        # Por enquanto, retornamos um erro informando que precisa de configuração
        return jsonify({
            "success": False,
            "error": "Para produção, configure um CDN ou armazenamento externo para as músicas"
        }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/musics/covers/<path:filename>')
def serve_cover(filename):
    """Serve capas de álbuns"""
    try:
        # Se estivermos rodando localmente e o diretório existir, servir arquivo local
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        local_covers = os.path.join(project_root, 'musics', 'covers')
        covers_base = local_covers if os.path.isdir(local_covers) else COVERS_DIR
        if os.path.isdir(covers_base):
            return send_from_directory(covers_base, filename)
        # Para Vercel, você pode usar um CDN ou armazenamento externo
        return jsonify({
            "success": False,
            "error": "Para produção, configure um CDN ou armazenamento externo para as capas"
        }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Para Vercel serverless
app.debug = False

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
