import os
import threading
import mimetypes
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from typing import Optional, Dict
import json
import re
import time
import shutil
import requests
import base64
from io import BytesIO
from flask import Response

try:
    from yt_dlp import YoutubeDL
except Exception:
    YoutubeDL = None

try:
    from mutagen.mp4 import MP4
except Exception:
    MP4 = None


MUSIC_DIR = os.path.join(os.path.dirname(__file__), 'musics')
os.makedirs(MUSIC_DIR, exist_ok=True)

# Capa default e pasta de capas
COVERS_DIR = os.path.join(MUSIC_DIR, 'covers')
os.makedirs(COVERS_DIR, exist_ok=True)
DEFAULT_COVER = '/musics/default-cover.jpg'

app = Flask(__name__)
CORS(app)

# Ensure correct audio MIME types
mimetypes.add_type('audio/webm', '.webm')
mimetypes.add_type('audio/mp4', '.m4a')
mimetypes.add_type('audio/aac', '.aac')


def _get_playlist_folder(playlist_name: str) -> str:
    """Cria e retorna o caminho para a pasta da playlist."""
    # Remove caracteres inválidos do nome da playlist
    safe_name = re.sub(r'[<>:"/\\|?*]', '_', playlist_name)
    playlist_dir = os.path.join(MUSIC_DIR, safe_name)
    os.makedirs(playlist_dir, exist_ok=True)
    return playlist_dir


def _extract_playlist_name_from_url(url: str) -> str:
    """Extrai o nome da playlist do YouTube a partir da URL."""
    if YoutubeDL is None:
        return "Playlist"
    
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Se for uma playlist, extrai o nome
            if info.get('_type') == 'playlist':
                playlist_name = info.get('title', 'Playlist')
                # Remove caracteres inválidos para nome de pasta
                safe_name = re.sub(r'[<>:"/\\|?*]', '_', playlist_name)
                return safe_name
            else:
                # Se for um vídeo único, usa o nome do canal ou título do vídeo
                channel_name = info.get('uploader', '')
                video_title = info.get('title', '')
                if channel_name and video_title:
                    safe_name = re.sub(r'[<>:"/\\|?*]', '_', f"{channel_name} - {video_title}")
                    return safe_name
                elif video_title:
                    safe_name = re.sub(r'[<>:"/\\|?*]', '_', video_title)
                    return safe_name
                else:
                    return "Playlist"
    except Exception as e:
        print(f"Erro ao extrair nome da playlist: {e}")
        return "Playlist"


def _download_youtube_playlist(url: str, playlist_name: str = None) -> dict:
    if YoutubeDL is None:
        return {"success": False, "error": "yt-dlp não está instalado. Adicione 'yt-dlp' ao requirements.txt e instale as dependências."}

    # Se não foi fornecido um nome, extrai da URL
    if not playlist_name:
        playlist_name = _extract_playlist_name_from_url(url)

    # Cria pasta para a playlist
    playlist_dir = _get_playlist_folder(playlist_name)

    # Download best audio without requiring ffmpeg conversion
    # Browser can play m4a/webm/opus in most cases. If you want MP3, install ffmpeg and enable postprocessors below.
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'outtmpl': os.path.join(playlist_dir, '%(title)s.%(ext)s'),
        'ignoreerrors': True,
        'noprogress': True,
        'noplaylist': False,
        # Uncomment to force MP3 conversion (requires ffmpeg installed in PATH):
        # 'postprocessors': [{
        #     'key': 'FFmpegExtractAudio',
        #     'preferredcodec': 'mp3',
        #     'preferredquality': '192',
        # }],
    }

    downloaded = []
    errors = []
    playlist_thumbnail = None

    def hook(d):
        if d.get('status') == 'finished':
            filename = d.get('filename')
            if filename:
                downloaded.append(os.path.basename(filename))
                try:
                    _ensure_cover_for_file(filename)
                except Exception:
                    pass

    ydl_opts['progress_hooks'] = [hook]

    try:
        with YoutubeDL(ydl_opts) as ydl:
            # Primeiro, extrai informações da playlist para obter a thumbnail
            try:
                info = ydl.extract_info(url, download=False)
                if info and info.get('_type') == 'playlist':
                    # Tenta pegar thumbnail da playlist primeiro
                    playlist_thumbnail = info.get('thumbnails', [{}])[0].get('url') if info.get('thumbnails') else None
                    if not playlist_thumbnail:
                        # Tenta pegar thumbnail do primeiro vídeo
                        entries = info.get('entries', [])
                        if entries and len(entries) > 0:
                            first_video = entries[0]
                            if first_video and first_video.get('thumbnails'):
                                playlist_thumbnail = first_video['thumbnails'][0].get('url')
                            elif first_video and first_video.get('thumbnail'):
                                playlist_thumbnail = first_video['thumbnail']
                elif info and info.get('thumbnail'):
                    # Se for um vídeo único, usa sua thumbnail
                    playlist_thumbnail = info['thumbnail']
            except Exception as e:
                print(f"Erro ao extrair thumbnail da playlist: {e}")
            
            # Agora faz o download
            ydl.download([url])
    except Exception as e:
        errors.append(str(e))

    # Baixa a thumbnail da playlist se encontrou uma
    if playlist_thumbnail and not errors:
        try:
            print(f"🎯 Thumbnail encontrada: {playlist_thumbnail}")
            response = requests.get(playlist_thumbnail, timeout=10)
            if response.status_code == 200:
                safe_playlist = _safe_stem(playlist_name)
                cover_path = os.path.join(COVERS_DIR, f"{safe_playlist}.jpg")
                with open(cover_path, 'wb') as f:
                    f.write(response.content)
                print(f"✅ Thumbnail da playlist salva: {cover_path}")
            else:
                print(f"❌ Erro HTTP ao baixar thumbnail: {response.status_code}")
        except Exception as e:
            print(f"❌ Erro ao baixar thumbnail da playlist: {e}")
    else:
        print(f"⚠️ Nenhuma thumbnail encontrada para playlist: {playlist_name}")

    success = len(downloaded) > 0 and len(errors) == 0
    result = {
        "success": success,
        "downloaded": downloaded,
        "errors": errors,
        "playlist": playlist_name,
    }
    if not success:
        result["error"] = errors[0] if errors else "Falha no download"
    return result


def _infer_title_artist_from_filename(filename: str) -> Dict[str, str]:
    name = os.path.splitext(os.path.basename(filename))[0]
    # Patterns like "Artist - Title"
    if ' - ' in name:
        parts = name.split(' - ', 1)
        return {
            'artist': parts[0].strip(),
            'title': parts[1].strip()
        }
    return {'artist': '', 'title': name}


def _extract_mp4_tags(path: str) -> Dict[str, Optional[str]]:
    tags = {'title': None, 'artist': None, 'album': None, 'year': None}
    if MP4 is None:
        return tags
    try:
        audio = MP4(path)
        tags['title'] = (audio.tags.get('\xa9nam') or [None])[0]
        tags['artist'] = (audio.tags.get('\xa9ART') or [None])[0]
        tags['album'] = (audio.tags.get('\xa9alb') or [None])[0]
        tags['year'] = (audio.tags.get('\xa9day') or [None])[0]
    except Exception:
        pass
    return tags


def _extract_generic_tags(path: str) -> Dict[str, Optional[str]]:
    """Extrai tags usando mutagen.File(easy=True) para múltiplos formatos."""
    tags = {'title': None, 'artist': None, 'album': None, 'year': None}
    try:
        from mutagen import File as MFile
        mf = MFile(path, easy=True)
        if not mf or not getattr(mf, 'tags', None):
            return tags
        def first(tagkey_list):
            for key in tagkey_list:
                if key in mf.tags and mf.tags.get(key):
                    val = mf.tags.get(key)
                    if isinstance(val, (list, tuple)):
                        return val[0]
                    return val
            return None
        tags['title'] = first(['title', 'TIT2']) or tags['title']
        tags['artist'] = first(['artist', 'TPE1']) or tags['artist']
        tags['album'] = first(['album', 'TALB']) or tags['album']
        # Ano pode vir em 'date', 'year', 'TDRC'
        year_val = first(['date', 'year', 'TDRC'])
        if isinstance(year_val, str):
            # extrai AAAA
            import re as _re
            m = _re.search(r'(\\d{4})', year_val)
            tags['year'] = m.group(1) if m else year_val
        else:
            tags['year'] = year_val
    except Exception:
        pass
    return tags


def _download_cover_from_deezer(title: str, artist: str, out_filename: Optional[str] = None) -> Optional[str]:
    """Tenta obter capa via Deezer API e salvar em musics/covers.
    Se out_filename (basename sem extensão) for informado, usa esse nome.
    Retorna URL relativa começando com /musics/.
    """
    try:
        import requests
        query = f"{artist} {title}".strip()
        if not query:
            query = title
        if not query:
            return None
        r = requests.get('https://api.deezer.com/search', params={'q': query}, timeout=10)
        data = r.json()
        track = (data.get('data') or [None])[0]
        if not track:
            return None
        cover_url = track.get('album', {}).get('cover_xl') or track.get('album', {}).get('cover')
        if not cover_url:
            return None
        img = requests.get(cover_url, timeout=10).content
        if out_filename:
            safe_name = re.sub(r'[^a-zA-Z0-9_-]+', '_', out_filename)[:80] or 'cover'
        else:
            safe_name = re.sub(r'[^a-zA-Z0-9_-]+', '_', f"{artist}_{title}")[:80] or 'cover'
        cover_file = os.path.join(COVERS_DIR, f"{safe_name}.jpg")
        with open(cover_file, 'wb') as f:
            f.write(img)
        rel = '/musics/covers/' + os.path.basename(cover_file)
        return rel
    except Exception:
        return None


def _enrich_metadata_from_deezer(title: str, artist: str) -> Dict[str, Optional[str]]:
    """Busca metadados no Deezer (title, artist, album, year, cover)."""
    enriched = {'title': None, 'artist': None, 'album': None, 'year': None, 'cover': None}
    try:
        import requests
        query = f"{artist} {title}".strip() or title
        if not query:
            return enriched
        r = requests.get('https://api.deezer.com/search', params={'q': query}, timeout=10)
        data = r.json()
        track = (data.get('data') or [None])[0]
        if not track:
            return enriched
        enriched['title'] = track.get('title')
        enriched['artist'] = track.get('artist', {}).get('name')
        enriched['album'] = track.get('album', {}).get('title')
        enriched['cover'] = track.get('album', {}).get('cover_xl') or track.get('album', {}).get('cover')
        # busca album para pegar release_date
        album_id = track.get('album', {}).get('id')
        if album_id:
            try:
                album_resp = requests.get(f'https://api.deezer.com/album/{album_id}', timeout=10)
                album_json = album_resp.json()
                release_date = album_json.get('release_date')
                if release_date:
                    import re as _re
                    m = _re.search(r'(\d{4})', release_date)
                    if m:
                        enriched['year'] = m.group(1)
            except Exception:
                pass
    except Exception:
        return enriched
    return enriched


def _ensure_cover_for_file(audio_path: str) -> Optional[str]:
    """Garante que exista uma imagem de capa para um arquivo de áudio.
    Usa o nome base do arquivo como nome da capa. Retorna URL relativa se existir/baixar."""
    try:
        stem = os.path.splitext(os.path.basename(audio_path))[0]
        safe_stem = re.sub(r'[^a-zA-Z0-9_-]+', '_', stem)[:80] or 'cover'
        target = os.path.join(COVERS_DIR, f"{safe_stem}.jpg")
        if os.path.exists(target):
            return '/musics/covers/' + os.path.basename(target)

        title = None
        artist = None
        if audio_path.lower().endswith('.m4a'):
            tags = _extract_mp4_tags(audio_path)
            title = tags.get('title')
            artist = tags.get('artist')
        if not title or not artist:
            inferred = _infer_title_artist_from_filename(os.path.basename(audio_path))
            title = title or inferred['title']
            artist = artist or inferred['artist']

        return _download_cover_from_deezer(title or '', artist or '', out_filename=safe_stem)
    except Exception:
        return None


def _safe_stem(name: str) -> str:
    try:
        return re.sub(r'[^a-zA-Z0-9_-]+', '_', name).strip('_')[:80] or 'cover'
    except Exception:
        return 'cover'


def _get_or_create_playlist_cover(playlist_name: str) -> str:
    """Retorna a URL relativa da capa da playlist. Se não existir, tenta criar
    a partir da capa da primeira música com arte disponível. Caso contrário, usa default."""
    try:
        safe_playlist = _safe_stem(playlist_name)
        target_path = os.path.join(COVERS_DIR, f"{safe_playlist}.jpg")
        if os.path.exists(target_path):
            print(f"✅ Capa da playlist encontrada: {target_path}")
            return '/musics/covers/' + os.path.basename(target_path)

        print(f"🔍 Procurando capa para playlist: {playlist_name}")
        # Procura a primeira música da playlist com capa
        playlist_dir = os.path.join(MUSIC_DIR, playlist_name)
        if not os.path.isdir(playlist_dir):
            print(f"❌ Diretório da playlist não encontrado: {playlist_dir}")
            return DEFAULT_COVER

        for file_name in os.listdir(playlist_dir):
            if file_name.lower().endswith(('.mp3', '.m4a', '.aac', '.ogg', '.opus', '.wav', '.flac', '.webm')):
                audio_path = os.path.join(playlist_dir, file_name)
                print(f"🎵 Verificando música: {file_name}")
                rel_cover = _ensure_cover_for_file(audio_path)  # '/musics/covers/<file>.jpg' or None
                if rel_cover and rel_cover.startswith('/musics/covers/'):
                    src = os.path.join(COVERS_DIR, os.path.basename(rel_cover))
                    if os.path.exists(src):
                        try:
                            shutil.copyfile(src, target_path)
                            print(f"✅ Capa copiada de música para playlist: {target_path}")
                            return '/musics/covers/' + os.path.basename(target_path)
                        except Exception as e:
                            print(f"❌ Erro ao copiar capa: {e}")
                            # Se falhar ao copiar, apenas retorna a capa existente da música
                            return rel_cover
        # Nenhuma capa encontrada nas músicas
        print(f"⚠️ Nenhuma capa encontrada para playlist: {playlist_name}")
        return DEFAULT_COVER
    except Exception as e:
        print(f"❌ Erro em _get_or_create_playlist_cover: {e}")
        return DEFAULT_COVER


@app.route('/list_playlists', methods=['GET'])
def list_playlists():
    """Lista todas as playlists disponíveis."""
    playlists = []
    
    # Lista diretórios dentro de musics/ (excluindo covers)
    for item in os.listdir(MUSIC_DIR):
        item_path = os.path.join(MUSIC_DIR, item)
        if os.path.isdir(item_path) and item != 'covers':
            # Conta quantas músicas tem na playlist
            music_count = 0
            for file in os.listdir(item_path):
                if file.lower().endswith(('.mp3', '.m4a', '.aac', '.ogg', '.opus', '.wav', '.flac', '.webm')):
                    music_count += 1
            
            playlists.append({
                'name': item,
                'path': f'/musics/{item}',
                'music_count': music_count,
                'cover': _get_or_create_playlist_cover(item)
            })
    
    return jsonify({
        'playlists': sorted(playlists, key=lambda x: x['name'].lower()),
        'count': len(playlists)
    })


@app.route('/check_music_changes', methods=['GET'])
def check_music_changes():
    """Verifica apenas mudanças nos arquivos de música sem processar metadados."""
    playlist_name = request.args.get('playlist', '')
    last_check = request.args.get('last_check', '0')
    
    try:
        last_check_time = float(last_check)
    except ValueError:
        last_check_time = 0
    
    items = []
    
    if playlist_name:
        playlist_dir = os.path.join(MUSIC_DIR, playlist_name)
        if not os.path.exists(playlist_dir):
            return jsonify({"error": "Playlist não encontrada"}), 404
        search_dir = playlist_dir
    else:
        search_dir = MUSIC_DIR
    
    for root, _, files in os.walk(search_dir):
        if 'covers' in root:
            continue
            
        for f in files:
            if f.lower().endswith(('.mp3', '.m4a', '.aac', '.ogg', '.opus', '.wav', '.flac', '.webm')):
                full_path = os.path.join(root, f)
                modified_time = os.path.getmtime(full_path)
                
                # Só inclui arquivos modificados desde a última verificação
                if modified_time > last_check_time:
                    rel_path = os.path.relpath(full_path, os.path.dirname(__file__))
                    playlist = os.path.basename(os.path.dirname(full_path)) if os.path.dirname(full_path) != MUSIC_DIR else "Geral"
                    
                    items.append({
                        'name': f,
                        'path': '/' + rel_path.replace('\\', '/'),
                        'playlist': playlist,
                        'size': os.path.getsize(full_path),
                        'modified': modified_time,
                        'action': 'modified' if os.path.exists(full_path) else 'deleted'
                    })
    
    return jsonify({
        'changes': items,
        'count': len(items),
        'current_time': time.time()
    })


@app.route('/list_music', methods=['GET'])
def list_music():
    """Lista músicas de uma playlist específica ou todas as músicas."""
    playlist_name = request.args.get('playlist', '')
    # Default: when a specific playlist is requested and client didn't specify, prefer instant load
    raw_skip = request.args.get('skip_metadata', None)
    if raw_skip is None:
        skip_metadata = bool(playlist_name)
    else:
        skip_metadata = str(raw_skip).lower() == 'true'
    items = []
    
    if playlist_name:
        # Lista músicas de uma playlist específica
        playlist_dir = os.path.join(MUSIC_DIR, playlist_name)
        if not os.path.exists(playlist_dir):
            return jsonify({"error": "Playlist não encontrada"}), 404
        
        search_dir = playlist_dir
    else:
        # Lista todas as músicas de todas as playlists
        search_dir = MUSIC_DIR
    
    for root, _, files in os.walk(search_dir):
        # Pula a pasta covers
        if 'covers' in root:
            continue
            
        for f in files:
            if f.lower().endswith(('.mp3', '.m4a', '.aac', '.ogg', '.opus', '.wav', '.flac', '.webm')):
                rel_path = os.path.relpath(os.path.join(root, f), os.path.dirname(__file__))
                full_path = os.path.join(root, f)
                
                # Determina a playlist baseada no diretório
                playlist = os.path.basename(os.path.dirname(full_path)) if os.path.dirname(full_path) != MUSIC_DIR else "Geral"
                
                # Se skip_metadata=True, retorna apenas informações básicas
                if skip_metadata:
                    # tenta mapear capa rapidamente pelo nome do arquivo
                    stem = os.path.splitext(os.path.basename(f))[0]
                    safe_stem = re.sub(r'[^a-zA-Z0-9_-]+', '_', stem)[:80] or 'cover'
                    existing_cover = os.path.join(COVERS_DIR, f"{safe_stem}.jpg")
                    cover_url = ('/musics/covers/' + os.path.basename(existing_cover)) if os.path.exists(existing_cover) else DEFAULT_COVER
                    items.append({
                        'name': f,
                        'path': '/' + rel_path.replace('\\', '/'),
                        'playlist': playlist,
                        'cover': cover_url,
                        'size': os.path.getsize(full_path),
                        'modified': os.path.getmtime(full_path)
                    })
                    continue
                
                # Processamento completo de metadados (apenas quando necessário)
                tags = {'title': None, 'artist': None, 'album': None, 'year': None}
                cover_url = None
                
                # Extrai metadados básicos do arquivo
                if f.lower().endswith('.m4a'):
                    tags = _extract_mp4_tags(full_path)
                else:
                    gtags = _extract_generic_tags(full_path)
                    tags.update({k: v or tags.get(k) for k, v in gtags.items()})
                
                # Infere título e artista do nome do arquivo
                inferred = _infer_title_artist_from_filename(f)
                title = (tags.get('title') or inferred['title'] or '').strip()
                artist = (tags.get('artist') or inferred['artist'] or '').strip()
                
                # Só busca no Deezer se realmente necessário (título ou artista vazios)
                if not artist or not title:
                    try:
                        enriched = _enrich_metadata_from_deezer(title, artist)
                        title = enriched.get('title') or title
                        artist = enriched.get('artist') or artist
                        if not tags.get('album'):
                            tags['album'] = enriched.get('album') or tags.get('album')
                        if not tags.get('year'):
                            tags['year'] = enriched.get('year') or tags.get('year')
                    except Exception:
                        pass  # Ignora erros do Deezer para não travar o carregamento
                
                # Verifica se já existe cover
                stem = os.path.splitext(os.path.basename(f))[0]
                safe_stem = re.sub(r'[^a-zA-Z0-9_-]+', '_', stem)[:80] or 'cover'
                existing_cover = os.path.join(COVERS_DIR, f"{safe_stem}.jpg")
                if os.path.exists(existing_cover):
                    cover_url = '/musics/covers/' + os.path.basename(existing_cover)
                else:
                    cover_url = DEFAULT_COVER  # Não baixa cover automaticamente
                
                items.append({
                    'name': f,
                    'path': '/' + rel_path.replace('\\', '/'),
                    'title': title,
                    'artist': artist,
                    'album': tags.get('album') or '',
                    'year': tags.get('year') or '',
                    'cover': cover_url,
                    'playlist': playlist,
                    'size': os.path.getsize(full_path),
                    'modified': os.path.getmtime(full_path)
                })
    
    return jsonify({
        'music': sorted(items, key=lambda x: x['name'].lower()),
        'count': len(items)
    })


@app.route('/create_playlist', methods=['POST'])
def create_playlist():
    """Cria uma nova playlist."""
    data = request.get_json(silent=True) or {}
    playlist_name = data.get('name', '').strip()
    
    if not playlist_name:
        return jsonify({"error": "Nome da playlist é obrigatório"}), 400
    
    try:
        playlist_dir = _get_playlist_folder(playlist_name)
        return jsonify({
            "success": True,
            "playlist": playlist_name,
            "path": playlist_dir
        })
    except Exception as e:
        return jsonify({"error": f"Erro ao criar playlist: {str(e)}"}), 500


@app.route('/upload_to_playlist', methods=['POST'])
def upload_to_playlist():
    """Upload de arquivos para uma playlist específica."""
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400
    
    playlist_name = request.form.get('playlist', 'Geral')
    files = request.files.getlist('file')
    
    uploaded = []
    errors = []
    
    playlist_dir = _get_playlist_folder(playlist_name)
    
    for file in files:
        if file.filename == '':
            continue
            
        if file and file.filename.lower().endswith(('.mp3', '.m4a', '.aac', '.ogg', '.opus', '.wav', '.flac', '.webm')):
            try:
                # Salva o arquivo na pasta da playlist
                filename = os.path.join(playlist_dir, file.filename)
                file.save(filename)
                uploaded.append(file.filename)
                
                # Tenta baixar capa
                try:
                    _ensure_cover_for_file(filename)
                except Exception:
                    pass
                    
            except Exception as e:
                errors.append(f"Erro ao salvar {file.filename}: {str(e)}")
        else:
            errors.append(f"Formato não suportado: {file.filename}")
    
    return jsonify({
        "success": len(uploaded) > 0,
        "uploaded": uploaded,
        "errors": errors,
        "playlist": playlist_name
    })


@app.route('/musics/default-cover.jpg')
def serve_default_cover():
	"""Serve a visible SVG default cover to avoid 404s and show a clear placeholder."""
	try:
		svg = (
			'<?xml version="1.0" encoding="UTF-8"?>\n'
			'<svg xmlns="http://www.w3.org/2000/svg" width="600" height="600" viewBox="0 0 600 600">\n'
			'<defs>\n'
			'	<linearGradient id="g" x1="0" y1="0" x2="1" y2="1">\n'
			'		<stop offset="0%" stop-color="#0d2d1f"/>\n'
			'		<stop offset="100%" stop-color="#0b1f16"/>\n'
			'	</linearGradient>\n'
			'</defs>\n'
			'<rect width="600" height="600" fill="url(#g)"/>\n'
			'<g fill="none" stroke="#1db954" stroke-width="18" stroke-linecap="round" stroke-linejoin="round" opacity="0.9" transform="translate(120,120)">\n'
			'	<path d="M180 12v240c0 44-36 80-80 80s-80-36-80-80 36-80 80-80c16 0 31 5 44 13V52l136-28v152c0 44-36 80-80 80-11 0-22-2-32-7"/>\n'
			'</g>\n'
			'<g font-family="Segoe UI, Roboto, Arial" font-size="38" font-weight="600" fill="#cfe9d9" opacity="0.9">\n'
			'	<text x="50%" y="560" text-anchor="middle">Musickêra</text>\n'
			'</g>\n'
			'</svg>'
		)
		return Response(svg, mimetype='image/svg+xml')
	except Exception:
		return Response(b'', mimetype='image/svg+xml')

@app.route('/musics/<path:filename>')
def serve_music(filename: str):
    return send_from_directory(MUSIC_DIR, filename)


@app.route('/extract_playlist_name', methods=['POST'])
def extract_playlist_name():
    """Extrai o nome da playlist do YouTube sem fazer download."""
    data = request.get_json(silent=True) or {}
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({"error": "URL é obrigatória."}), 400
    
    if not (url.startswith('http://') or url.startswith('https://')):
        return jsonify({"error": "URL inválida. Cole um link completo começando com http(s)://"}), 400

    try:
        playlist_name = _extract_playlist_name_from_url(url)
        return jsonify({
            "success": True,
            "playlist_name": playlist_name
        })
    except Exception as e:
        return jsonify({"error": f"Erro ao extrair nome da playlist: {str(e)}"}), 500


@app.route('/download_playlist', methods=['POST'])
def download_playlist():
    data = request.get_json(silent=True) or {}
    url = data.get('url', '').strip()
    playlist_name = data.get('playlist', 'Playlist').strip()
    background = bool(data.get('background', False))
    if not url:
        return jsonify({"success": False, "error": "URL é obrigatória."}), 400
    if not (url.startswith('http://') or url.startswith('https://')):
        return jsonify({"success": False, "error": "URL inválida. Cole um link completo começando com http(s)://"}), 400

    if background:
        result_container = {"result": None}

        def task():
            result_container["result"] = _download_youtube_playlist(url, playlist_name)

        threading.Thread(target=task, daemon=True).start()
        return jsonify({"success": True, "message": "Download iniciado em segundo plano."}), 202

    result = _download_youtube_playlist(url, playlist_name)
    status = 200 if result.get('success') else 500
    return jsonify(result), status


if __name__ == '__main__':
    port = int(os.environ.get('PORT', '5000'))
    app.run(host='0.0.0.0', port=port, debug=False)


