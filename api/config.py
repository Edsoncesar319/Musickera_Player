import os

# Configurações para Vercel
class Config:
    # Configurações básicas
    DEBUG = False
    TESTING = False
    
    # Configurações de CORS
    CORS_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:5000",
        "https://musickera-player.vercel.app",
        "https://*.vercel.app"
    ]
    
    # Configurações de diretórios
    MUSIC_DIR = os.environ.get('MUSIC_DIR', '/tmp/musics')
    COVERS_DIR = os.environ.get('COVERS_DIR', '/tmp/covers')
    
    # Configurações de upload
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB
    ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg', 'm4a', 'aac'}
    
    # Configurações de segurança
    SECRET_KEY = os.environ.get('SECRET_KEY', 'musickera-secret-key-2024')

class DevelopmentConfig(Config):
    DEBUG = True
    CORS_ORIGINS = ["*"]

class ProductionConfig(Config):
    DEBUG = False

# Configuração baseada no ambiente
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
