"""
Utilitários para o Backend Musickêra
"""

import os
import re
import mimetypes
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote, unquote

def sanitize_filename(filename: str) -> str:
    """
    Sanitiza o nome do arquivo removendo caracteres perigosos
    """
    # Remove caracteres perigosos
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove espaços extras
    filename = re.sub(r'\s+', ' ', filename).strip()
    # Limita o tamanho
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255-len(ext)] + ext
    return filename

def get_file_extension(filename: str) -> str:
    """
    Retorna a extensão do arquivo em minúsculas
    """
    return Path(filename).suffix.lower()

def is_allowed_file(filename: str, allowed_extensions: set) -> bool:
    """
    Verifica se o arquivo tem uma extensão permitida
    """
    return get_file_extension(filename) in allowed_extensions

def get_mime_type(filename: str) -> str:
    """
    Retorna o MIME type do arquivo
    """
    ext = get_file_extension(filename)
    mime_type = mimetypes.guess_type(filename)[0]
    
    # Mapeamento personalizado para tipos de áudio
    audio_mime_types = {
        '.mp3': 'audio/mpeg',
        '.m4a': 'audio/mp4',
        '.aac': 'audio/aac',
        '.ogg': 'audio/ogg',
        '.opus': 'audio/opus',
        '.wav': 'audio/wav',
        '.flac': 'audio/flac',
        '.webm': 'audio/webm'
    }
    
    return audio_mime_types.get(ext, mime_type or 'application/octet-stream')

def format_file_size(size_bytes: int) -> str:
    """
    Formata o tamanho do arquivo em formato legível
    """
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"

def format_duration(seconds: int) -> str:
    """
    Formata a duração em segundos para formato MM:SS
    """
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes:02d}:{remaining_seconds:02d}"

def extract_metadata_from_filename(filename: str) -> Dict[str, str]:
    """
    Extrai metadados básicos do nome do arquivo
    """
    # Remove a extensão
    name_without_ext = Path(filename).stem
    
    # Padrões comuns de nomes de arquivo
    patterns = [
        r'^(.+?)\s*-\s*(.+?)$',  # Artista - Título
        r'^(.+?)\s*_\s*(.+?)$',  # Artista_Título
        r'^(.+?)\s*\.\s*(.+?)$', # Artista.Título
    ]
    
    for pattern in patterns:
        match = re.match(pattern, name_without_ext)
        if match:
            artist = match.group(1).strip()
            title = match.group(2).strip()
            return {
                'artist': artist,
                'title': title,
                'album': 'Desconhecido'
            }
    
    # Se não encontrar padrão, usa o nome completo como título
    return {
        'artist': 'Desconhecido',
        'title': name_without_ext,
        'album': 'Desconhecido'
    }

def generate_file_hash(file_path: str) -> str:
    """
    Gera um hash MD5 do arquivo
    """
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def create_playlist_directory(playlist_name: str, base_dir: str) -> str:
    """
    Cria um diretório para a playlist
    """
    safe_name = sanitize_filename(playlist_name)
    playlist_dir = Path(base_dir) / safe_name
    playlist_dir.mkdir(parents=True, exist_ok=True)
    return str(playlist_dir)

def get_relative_path(file_path: str, base_dir: str) -> str:
    """
    Retorna o caminho relativo do arquivo em relação ao diretório base
    """
    try:
        return str(Path(file_path).relative_to(base_dir))
    except ValueError:
        return file_path

def url_encode_path(path: str) -> str:
    """
    Codifica o caminho para uso em URLs
    """
    return quote(path, safe='')

def url_decode_path(path: str) -> str:
    """
    Decodifica o caminho de URLs
    """
    return unquote(path)

def validate_playlist_name(name: str) -> Tuple[bool, str]:
    """
    Valida o nome da playlist
    """
    if not name or not name.strip():
        return False, "Nome da playlist não pode estar vazio"
    
    if len(name) > 100:
        return False, "Nome da playlist muito longo (máximo 100 caracteres)"
    
    # Verifica caracteres perigosos
    if re.search(r'[<>:"/\\|?*]', name):
        return False, "Nome da playlist contém caracteres inválidos"
    
    return True, ""

def get_file_info(file_path: str) -> Dict[str, any]:
    """
    Retorna informações básicas do arquivo
    """
    path = Path(file_path)
    stat = path.stat()
    
    return {
        'name': path.name,
        'size': stat.st_size,
        'size_formatted': format_file_size(stat.st_size),
        'modified': stat.st_mtime,
        'extension': get_file_extension(path.name),
        'mime_type': get_mime_type(path.name)
    }

def split_path(path: str) -> List[str]:
    """
    Divide um caminho em partes
    """
    return [part for part in Path(path).parts if part]

def join_paths(*paths: str) -> str:
    """
    Junta caminhos de forma segura
    """
    return str(Path(*paths))

def ensure_directory_exists(directory: str) -> None:
    """
    Garante que o diretório existe
    """
    Path(directory).mkdir(parents=True, exist_ok=True)

def is_safe_path(path: str, base_dir: str) -> bool:
    """
    Verifica se o caminho é seguro (não tenta acessar diretórios superiores)
    """
    try:
        resolved_path = Path(path).resolve()
        base_path = Path(base_dir).resolve()
        return str(resolved_path).startswith(str(base_path))
    except (ValueError, RuntimeError):
        return False


