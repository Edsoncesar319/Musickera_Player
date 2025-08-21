import os
import threading
import mimetypes
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from typing import Optional, Dict
import json
import re

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


def _download_youtube_playlist(url: str) -> dict:
    if YoutubeDL is None:
        return {"success": False, "error": "yt-dlp não está instalado. Adicione 'yt-dlp' ao requirements.txt e instale as dependências."}

    # Download best audio without requiring ffmpeg conversion
    # Browser can play m4a/webm/opus in most cases. If you want MP3, install ffmpeg and enable postprocessors below.
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'outtmpl': os.path.join(MUSIC_DIR, '%(title)s.%(ext)s'),
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
            ydl.download([url])
    except Exception as e:
        errors.append(str(e))

    success = len(downloaded) > 0 and len(errors) == 0
    result = {
        "success": success,
        "downloaded": downloaded,
        "errors": errors,
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


@app.route('/list_music', methods=['GET'])
def list_music():
    items = []
    for root, _, files in os.walk(MUSIC_DIR):
        for f in files:
            if f.lower().endswith(('.mp3', '.m4a', '.aac', '.ogg', '.opus', '.wav', '.flac', '.webm')):
                rel_path = os.path.relpath(os.path.join(root, f), os.path.dirname(__file__))
                full_path = os.path.join(root, f)
                tags = {'title': None, 'artist': None, 'album': None, 'year': None}
                cover_url = None
                if f.lower().endswith('.m4a'):
                    tags = _extract_mp4_tags(full_path)
                else:
                    # Outros formatos via mutagen genérica
                    gtags = _extract_generic_tags(full_path)
                    tags.update({k: v or tags.get(k) for k, v in gtags.items()})
                # Se já houver capa baixada, usa; senão tenta Deezer
                inferred = _infer_title_artist_from_filename(f)
                title = (tags.get('title') or inferred['title'] or '').strip()
                artist = (tags.get('artist') or inferred['artist'] or '').strip()
                # Se artista ainda vazio, tenta Deezer para enriquecer
                if not artist or not title:
                    enriched = _enrich_metadata_from_deezer(title, artist)
                    title = enriched.get('title') or title
                    artist = enriched.get('artist') or artist
                    if not tags.get('album'):
                        tags['album'] = enriched.get('album') or tags.get('album')
                    if not tags.get('year'):
                        tags['year'] = enriched.get('year') or tags.get('year')
                stem = os.path.splitext(os.path.basename(f))[0]
                safe_stem = re.sub(r'[^a-zA-Z0-9_-]+', '_', stem)[:80] or 'cover'
                existing_cover = os.path.join(COVERS_DIR, f"{safe_stem}.jpg")
                if os.path.exists(existing_cover):
                    cover_url = '/musics/covers/' + os.path.basename(existing_cover)
                else:
                    # Tenta reaproveitar cover do enriquecimento antes de baixar arquivo
                    enriched_cover = None
                    try:
                        enriched = _enrich_metadata_from_deezer(title, artist)
                        enriched_cover = enriched.get('cover')
                    except Exception:
                        enriched_cover = None
                    if enriched_cover:
                        try:
                            import requests
                            img = requests.get(enriched_cover, timeout=10).content
                            with open(existing_cover, 'wb') as fimg:
                                fimg.write(img)
                            cover_url = '/musics/covers/' + os.path.basename(existing_cover)
                        except Exception:
                            cover_url = _download_cover_from_deezer(title, artist, out_filename=safe_stem) or DEFAULT_COVER
                    else:
                        cover_url = _download_cover_from_deezer(title, artist, out_filename=safe_stem) or DEFAULT_COVER
                items.append({
                    'name': f,
                    'path': '/' + rel_path.replace('\\', '/'),
                    'title': title,
                    'artist': artist,
                    'album': tags.get('album') or '',
                    'year': tags.get('year') or '',
                    'cover': cover_url,
                })
    return jsonify({
        'music': sorted(items, key=lambda x: x['name'].lower()),
        'count': len(items)
    })

@app.route('/musics/<path:filename>')
def serve_music(filename: str):
    return send_from_directory(MUSIC_DIR, filename)


@app.route('/download_playlist', methods=['POST'])
def download_playlist():
    data = request.get_json(silent=True) or {}
    url = data.get('url', '').strip()
    background = bool(data.get('background', False))
    if not url:
        return jsonify({"success": False, "error": "URL é obrigatória."}), 400
    if not (url.startswith('http://') or url.startswith('https://')):
        return jsonify({"success": False, "error": "URL inválida. Cole um link completo começando com http(s)://"}), 400

    if background:
        result_container = {"result": None}

        def task():
            result_container["result"] = _download_youtube_playlist(url)

        threading.Thread(target=task, daemon=True).start()
        return jsonify({"success": True, "message": "Download iniciado em segundo plano."}), 202

    result = _download_youtube_playlist(url)
    status = 200 if result.get('success') else 500
    return jsonify(result), status


if __name__ == '__main__':
    port = int(os.environ.get('PORT', '5000'))
    app.run(host='0.0.0.0', port=port, debug=False)


