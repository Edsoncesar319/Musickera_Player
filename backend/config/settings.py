"""
Configurações do Backend Musickêra
"""

import os
from pathlib import Path

# Configurações básicas
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
PORT = int(os.environ.get('PORT', 5000))
HOST = os.environ.get('HOST', '0.0.0.0')

# Diretórios
BASE_DIR = Path(__file__).parent.parent
MUSIC_DIR = os.environ.get('MUSIC_DIR', BASE_DIR / 'musics')
COVERS_DIR = os.environ.get('COVERS_DIR', MUSIC_DIR / 'covers')

# Criar diretórios se não existirem
os.makedirs(MUSIC_DIR, exist_ok=True)
os.makedirs(COVERS_DIR, exist_ok=True)

# Configurações de upload
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB
ALLOWED_EXTENSIONS = {
    'audio': {
        'mp3', 'm4a', 'aac', 'ogg', 'opus', 
        'wav', 'flac', 'webm', 'm4b'
    },
    'image': {
        'jpg', 'jpeg', 'png', 'webp', 'gif'
    }
}

# Configurações de API
API_VERSION = 'v1'
API_PREFIX = f'/api/{API_VERSION}'

# Configurações de CORS
CORS_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:8000',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:8000',,
    'https://musickera-plus.vercel.app'
]

# Configurações de cache
CACHE_TIMEOUT = 300  # 5 minutos
CACHE_DIR = BASE_DIR / 'cache'
os.makedirs(CACHE_DIR, exist_ok=True)

# Configurações de logging
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
LOG_FILE = BASE_DIR / 'logs' / 'server.log'
os.makedirs(LOG_FILE.parent, exist_ok=True)

# Configurações de segurança
SECRET_KEY = os.environ.get('SECRET_KEY', 'musickera-secret-key-change-in-production')
RATE_LIMIT = {
    'default': '100 per minute',
    'upload': '10 per minute'
}

# Configurações de metadados
METADATA_PROVIDERS = [
    'local',      # Metadados locais do arquivo
    'deezer',     # API do Deezer
    'musicbrainz' # MusicBrainz (futuro)
]

# Configurações de download
DOWNLOAD_TIMEOUT = 300  # 5 minutos
DOWNLOAD_CHUNK_SIZE = 8192  # 8KB
DOWNLOAD_RETRIES = 3

# Configurações de playlist
PLAYLIST_MAX_SIZE = 1000  # Máximo de músicas por playlist
PLAYLIST_NAME_MAX_LENGTH = 100

# Configurações de busca
SEARCH_MAX_RESULTS = 50
SEARCH_TIMEOUT = 10  # segundos

# Configurações de desenvolvimento
DEVELOPMENT_MODE = os.environ.get('DEVELOPMENT_MODE', 'True').lower() == 'true'

if DEVELOPMENT_MODE:
    # Configurações específicas para desenvolvimento
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    CORS_ORIGINS.append('*')  # Permitir todas as origens em desenvolvimento


