// Configuração inicial
const playlist = [];
let currentTrack = 0;
let isPlaying = false;
let audio = document.getElementById('playerAudio');
let repeatMode = 'none'; // 'none', 'one', 'all'

// Base de API/backend para recursos (configurável via window.API_BASE_URL ou localStorage)
const API_BASE_URL = (typeof window !== 'undefined' && (window.API_BASE_URL || localStorage.getItem('API_BASE_URL'))) || 'http://localhost:5000';

function resolveCoverUrl(coverPath) {
    const path = coverPath || 'musics/default-cover.jpg';
    if (!path) return '';
    const lower = String(path).toLowerCase();
    if (lower.startsWith('http://') || lower.startsWith('https://') || lower.startsWith('data:') || lower.startsWith('blob:')) {
        return path;
    }
    // Normaliza prefixo para caminhos como "/musics/..." ou "musics/..."
    const normalized = path.startsWith('/') ? path : `/${path}`;
    // Se referenciar diretório de músicas/capas, prefixa com API_BASE_URL
    if (normalized.startsWith('/musics/')) {
        return `${API_BASE_URL}${normalized}`;
    }
    return path;
}

// Configuração do IndexedDB
const dbName = 'MusickeraDB';
const dbVersion = 2;
let db;

// Função para inicializar o banco de dados
function initDB() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open(dbName, dbVersion);

        request.onerror = (event) => {
            console.error('Erro ao abrir o banco de dados:', event.target.error);
            reject(event.target.error);
        };

        request.onsuccess = (event) => {
            db = event.target.result;
            console.log('Banco de dados aberto com sucesso');
            resolve(db);
        };

        request.onupgradeneeded = (event) => {
            const db = event.target.result;
            
            if (!db.objectStoreNames.contains('musics')) {
                const musicStore = db.createObjectStore('musics', { keyPath: 'id', autoIncrement: true });
                musicStore.createIndex('title', 'title', { unique: false });
                musicStore.createIndex('artist', 'artist', { unique: false });
                musicStore.createIndex('album', 'album', { unique: false });
                musicStore.createIndex('fileName', 'fileName', { unique: false });
            } else {
                const musicStore = event.target.transaction.objectStore('musics');
                if (!musicStore.indexNames.contains('fileName')) {
                    musicStore.createIndex('fileName', 'fileName', { unique: false });
                }
            }
        };
    });
}

// Função para salvar uma música no banco de dados
async function saveMusicToDB(music) {
    return new Promise((resolve, reject) => {
        const transaction = db.transaction(['musics'], 'readwrite');
        const store = transaction.objectStore('musics');
        
        const request = store.add(music);
        
        request.onsuccess = () => {
            console.log('Música salva no banco de dados');
            resolve(request.result);
        };
        
        request.onerror = (event) => {
            console.error('Erro ao salvar música:', event.target.error);
            reject(event.target.error);
        };
    });
}

// Função para carregar todas as músicas do banco de dados
async function loadMusicsFromDB() {
    return new Promise((resolve, reject) => {
        const transaction = db.transaction(['musics'], 'readonly');
        const store = transaction.objectStore('musics');
        const request = store.getAll();
        
        request.onsuccess = () => {
            console.log('Músicas carregadas do banco de dados');
            resolve(request.result);
        };
        
        request.onerror = (event) => {
            console.error('Erro ao carregar músicas:', event.target.error);
            reject(event.target.error);
        };
    });
}

// Função para remover uma música do banco de dados
async function removeMusicFromDB(id) {
    return new Promise((resolve, reject) => {
        const transaction = db.transaction(['musics'], 'readwrite');
        const store = transaction.objectStore('musics');
        const request = store.delete(id);
        
        request.onsuccess = () => {
            console.log('Música removida do banco de dados');
            resolve();
        };
        
        request.onerror = (event) => {
            console.error('Erro ao remover música:', event.target.error);
            reject(event.target.error);
        };
    });
}

// Função para limpar todas as músicas do banco de dados
async function clearMusicDB() {
    return new Promise((resolve, reject) => {
        const transaction = db.transaction(['musics'], 'readwrite');
        const store = transaction.objectStore('musics');
        const request = store.clear();
        
        request.onsuccess = () => {
            console.log('Banco de dados limpo');
            resolve();
        };
        
        request.onerror = (event) => {
            console.error('Erro ao limpar banco de dados:', event.target.error);
            reject(event.target.error);
        };
    });
}

// Busca uma música pelo nome do arquivo (para evitar duplicados)
async function getMusicByFileName(fileName) {
    return new Promise((resolve, reject) => {
        try {
            const transaction = db.transaction(['musics'], 'readonly');
            const store = transaction.objectStore('musics');
            const index = store.index('fileName');
            const request = index.get(fileName);

            request.onsuccess = () => resolve(request.result || null);
            request.onerror = (event) => reject(event.target.error);
        } catch (err) {
            reject(err);
        }
    });
}

// Função para deletar uma música do banco de dados
async function deleteMusicFromDB(id) {
    return new Promise((resolve, reject) => {
        try {
            const transaction = db.transaction(['musics'], 'readwrite');
            const store = transaction.objectStore('musics');
            const request = store.delete(id);
            
            request.onsuccess = () => {
                console.log('Música removida do banco de dados');
                resolve();
            };
            
            request.onerror = (event) => {
                console.error('Erro ao remover música do banco de dados:', event.target.error);
                reject(event.target.error);
            };
        } catch (err) {
            reject(err);
        }
    });
}

// Atualiza/insere música no DB
async function updateMusicInDB(music) {
    return new Promise((resolve, reject) => {
        const transaction = db.transaction(['musics'], 'readwrite');
        const store = transaction.objectStore('musics');
        const request = store.put(music);
        request.onsuccess = () => resolve();
        request.onerror = (event) => reject(event.target.error);
    });
}

// Função para converter ArrayBuffer em Blob URL
function arrayBufferToBlobUrl(arrayBuffer, mimeType) {
    try {
        if (!arrayBuffer || arrayBuffer.byteLength === 0) {
            throw new Error('ArrayBuffer vazio ou inválido');
        }
        
        const blob = new Blob([arrayBuffer], { type: mimeType || 'audio/mpeg' });
        const url = URL.createObjectURL(blob);
        
        if (!url) {
            throw new Error('Falha ao criar URL do blob');
        }
        
        return url;
    } catch (error) {
        console.error('Erro ao criar blob URL:', error);
        throw error;
    }
}

// Remove duplicados da playlist (e do IndexedDB quando aplicável)
async function dedupePlaylistAndDB() {
    const normalize = (s) => (s || '').toLowerCase().trim().replace(/\s+/g, ' ');
    const makeKey = (track) => {
        if (track.fileName) return `file:${normalize(track.fileName)}`;
        if (track.source === 'deezer' && track.deezerId) return `deezer:${track.deezerId}`;
        if (track.source === 'youtube' && track.youtubeId) return `yt:${track.youtubeId}`;
        return `meta:${normalize(track.artist)}|${normalize(track.title)}|${normalize(track.album)}`;
    };

    const seen = new Set();
    const toRemove = [];
    playlist.forEach((t, idx) => {
        const key = makeKey(t);
        if (seen.has(key)) {
            toRemove.push(idx);
        } else {
            seen.add(key);
        }
    });

    if (toRemove.length === 0) return;

    for (let i = toRemove.length - 1; i >= 0; i--) {
        const idx = toRemove[i];
        const track = playlist[idx];
        if (track && track.id) {
            try { await removeMusicFromDB(track.id); } catch (e) { console.error('Falha ao remover duplicado do DB:', e); }
        }
        playlist.splice(idx, 1);
        if (currentTrack >= idx && currentTrack > 0) currentTrack--;
    }

    sortPlaylist();
    updatePlaylistHTML();
    if (playlist.length > 0) {
        loadTrack();
    }
}

// Função para atualizar informações do player
function updatePlayerInfo(track) {
    if (track.source === 'deezer') {
        return;
    }
    
    document.querySelector('.track-title').textContent = track.title;
    document.querySelector('.artist-name').textContent = track.artist;
    document.querySelector('.album-name').textContent = track.album;
    document.querySelector('.album-cover').src = resolveCoverUrl(track.cover);
    document.querySelector('.album-cover').alt = `${track.title} - ${track.artist}`;
    document.querySelector('.duration').textContent = track.duration;
    const yearEl = document.querySelector('.Ano');
    if (yearEl) yearEl.textContent = track.year ? `Ano: ${track.year}` : '';
    
    // Atualiza a lista de reprodução
    const trackItems = document.querySelectorAll('.track-item');
    trackItems.forEach((item, index) => {
        item.classList.toggle('active', index === currentTrack);
    });
}

// Função para próxima faixa
function nextTrack() {
    currentTrack = (currentTrack + 1) % playlist.length;
    loadTrack();
    document.querySelector('.control-button:nth-child(2)').textContent = isPlaying ? '⏸' : '⏯';
}

// Função para faixa anterior
function previousTrack() {
    currentTrack = (currentTrack - 1 + playlist.length) % playlist.length;
    loadTrack();
    document.querySelector('.control-button:nth-child(2)').textContent = isPlaying ? '⏸' : '⏯';
}

// Função para carregar faixa
function loadTrack() {
    const track = playlist[currentTrack];
    
    console.log('Carregando faixa:', track);
    
    if (!track) {
        console.error('Nenhuma faixa encontrada para reproduzir');
        return;
    }
    
    if (track.source === 'deezer') {
        // Para músicas do Deezer, carrega o player incorporado
        const playerContainer = document.querySelector('.player-container');
        const coverUrl = resolveCoverUrl(track.cover);
        const embedHtml = `
            <div class="now-playing">
                <img src="${coverUrl}" alt="${track.title}" class="album-cover">
                <div class="track-info">
                    <h2 class="track-title">${track.title}</h2>
                    <p class="artist-name">${track.artist}</p>
                    <p class="album-name">${track.album}</p>
                </div>
            </div>
            <div class="deezer-embed">
                <iframe scrolling="no" frameborder="0" allowTransparency="true" 
                    src="https://www.deezer.com/plugins/player?format=classic&autoplay=${isPlaying ? 1 : 0}&playlist=true&width=700&height=350&color=007FEB&layout=dark&size=medium&type=tracks&id=${track.deezerId}&app_id=1"
                    width="700" height="350">
                </iframe>
            </div>
        `;
        playerContainer.innerHTML = embedHtml;
    } else if (track.source === 'youtube') {
        // For YouTube Music, create an embedded player
        const playerContainer = document.querySelector('.player-container');
        const coverUrl = resolveCoverUrl(track.cover);
        const embedHtml = `
            <div class="now-playing">
                <img src="${coverUrl}" alt="${track.title}" class="album-cover">
                <div class="track-info">
                    <h2 class="track-title">${track.title}</h2>
                    <p class="artist-name">${track.artist}</p>
                </div>
            </div>
            <div class="youtube-embed">
                <iframe 
                    width="100%" 
                    height="350" 
                    src="https://www.youtube.com/embed/${track.youtubeId}?autoplay=${isPlaying ? 1 : 0}&enablejsapi=1" 
                    frameborder="0" 
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                    allowfullscreen>
                </iframe>
            </div>
        `;
        playerContainer.innerHTML = embedHtml;
    } else {
        // Para músicas locais, usa o player padrão
        try {
            console.log('Processando música local:', {
                title: track.title,
                hasFile: !!track.file,
                hasFileArrayBuffer: !!track.fileArrayBuffer,
                fileType: track.fileType,
                fileName: track.fileName
            });

            // Verifica se o arquivo existe
            if (!track.file && !track.fileArrayBuffer) {
                console.error('Arquivo de música não encontrado:', track);
                alert('Arquivo de música não encontrado. Tente recarregar a página.');
                return;
            }

            // Cria URL do blob se necessário
            if (!track.file && track.fileArrayBuffer) {
                try {
                    console.log('Criando blob URL para:', track.fileName);
                    const blob = new Blob([track.fileArrayBuffer], { 
                        type: track.fileType || 'audio/mpeg' 
                    });
                    track.file = URL.createObjectURL(blob);
                    console.log('Blob URL criado:', track.file);
                } catch (e) {
                    console.error('Falha ao criar URL do blob para a faixa:', e);
                    alert('Erro ao processar o arquivo de música. Tente fazer upload novamente.');
                    return;
                }
            }

            // Verifica se o arquivo é um URL válido
            if (typeof track.file === 'string' && !track.file.startsWith('blob:') && !track.file.startsWith('http')) {
                console.error('URL do arquivo inválido:', track.file);
                alert('URL do arquivo inválido. Tente recarregar a página.');
                return;
            }

            console.log('Definindo src do áudio:', track.file);
            
            // Carrega o áudio
            audio.src = track.file;
            audio.load();
            
            // Atualiza as informações do player
            updatePlayerInfo(track);
            
            // Reproduz se estiver no estado de reprodução
            if (isPlaying) {
                console.log('Tentando reproduzir áudio...');
                audio.play().catch(error => {
                    console.error('Erro ao reproduzir áudio:', error);
                    console.error('Detalhes do erro:', {
                        name: error.name,
                        message: error.message,
                        code: audio.error ? audio.error.code : 'N/A'
                    });
                    alert('Erro ao reproduzir a música. Verifique se o arquivo existe e o formato é suportado (.mp3/.m4a/.webm).');
                });
            }
        } catch (error) {
            console.error('Erro ao carregar faixa:', error);
            alert('Erro ao carregar a música. Verifique se o arquivo está correto.');
        }
    }
}

// Função para alternar play/pause
function togglePlay() {
    const track = playlist[currentTrack];
    
    if (!track) {
        console.error('Nenhuma faixa selecionada para reproduzir');
        return;
    }
    
    if (track.source === 'deezer') {
        // Para músicas do Deezer, recarrega o iframe com o novo estado de autoplay
        loadTrack();
    } else if (track.source === 'youtube') {
        // For YouTube Music, recarrega o iframe com o novo estado de autoplay
        loadTrack();
    } else {
        try {
            if (isPlaying) {
                audio.pause();
                const icon = document.getElementById('playPauseIcon');
                if (icon) icon.textContent = 'play_arrow';
            } else {
                // Verifica se o áudio está pronto para reprodução
                if (audio.readyState < 2) {
                    console.log('Áudio ainda não está pronto, aguardando...');
                    audio.addEventListener('canplay', function playWhenReady() {
                        audio.removeEventListener('canplay', playWhenReady);
                        audio.play().catch(error => {
                            console.error('Erro ao reproduzir áudio:', error);
                            alert('Erro ao reproduzir a música. Verifique se o arquivo existe.');
                        });
                    });
                } else {
                    audio.play().catch(error => {
                        console.error('Erro ao reproduzir áudio:', error);
                        alert('Erro ao reproduzir a música. Verifique se o arquivo existe.');
                    });
                }
                const icon = document.getElementById('playPauseIcon');
                if (icon) icon.textContent = 'pause';
            }
        } catch (error) {
            console.error('Erro ao controlar reprodução:', error);
            alert('Erro ao controlar a reprodução da música.');
        }
    }
    isPlaying = !isPlaying;
}

// Função para formatar tempo
function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    seconds = Math.floor(seconds % 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
}

// Função para formatar duração
function formatDuration(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
}

// Função para ordenar a playlist
function sortPlaylist() {
    playlist.sort((a, b) => {
        // Primeiro ordena por artista
        const artistCompare = a.artist.localeCompare(b.artist, 'pt-BR');
        if (artistCompare !== 0) return artistCompare;
        
        // Se for o mesmo artista, ordena por álbum
        const albumCompare = a.album.localeCompare(b.album, 'pt-BR');
        if (albumCompare !== 0) return albumCompare;
        
        // Se for o mesmo álbum, ordena por título
        return a.title.localeCompare(b.title, 'pt-BR');
    });

    // Atualiza os números das faixas
    playlist.forEach((track, index) => {
        track.trackNumber = index + 1;
    });

    updatePlaylistHTML();
    savePlaylistThrottled();
}

// Função para atualizar HTML da playlist
function updatePlaylistHTML() {
    if (window.__renderScheduled) return;
    window.__renderScheduled = true;
    requestAnimationFrame(() => {
        window.__renderScheduled = false;
        const trackList = document.querySelector('.track-list');
        const clearButton = document.querySelector('.clear-playlist');
        
        // Atualiza a lista de músicas
        trackList.innerHTML = playlist.map((track, index) => `
            <li class="track-item ${index === currentTrack ? 'active' : ''}" 
                onclick="playTrack(${index})">
                <span class="track-number">${(index + 1).toString().padStart(2, '0')}</span>
                <img src="${resolveCoverUrl(track.cover || 'musics/default-cover.jpg')}" loading="lazy" alt="capa" style="width:40px;height:40px;border-radius:6px;object-fit:cover;margin-right:8px;">
                <div class="track-info-small">
                    <div class="track-title-small">${track.title}</div>
                    <div class="artist-name-small">${track.artist}</div>
                </div>
                <span class="track-duration">${track.duration}</span>
                <button class="remove-track" onclick="event.stopPropagation(); removeTrack(${index})">×</button>
            </li>
        `).join('');
        
        // Mostra ou esconde o botão de limpar playlist
        clearButton.style.display = playlist.length > 0 ? 'block' : 'none';
        
        adjustFontSize();
    });
}

// Função para ajustar tamanho da fonte
function adjustFontSize() {
    const trackItems = document.querySelectorAll('.track-item');
    
    trackItems.forEach(item => {
        const title = item.querySelector('.track-title-small');
        const artist = item.querySelector('.artist-name-small');
        const container = item.querySelector('.track-info-small');
        
        if (title && artist && container) {
            const containerWidth = container.offsetWidth;
            const titleLength = title.textContent.length;
            const artistLength = artist.textContent.length;
            
            // Ajusta o tamanho da fonte do título
            if (titleLength > 30) {
                title.style.fontSize = '0.85em';
            } else if (titleLength > 20) {
                title.style.fontSize = '0.9em';
            } else {
                title.style.fontSize = '1em';
            }
            
            // Ajusta o tamanho da fonte do artista
            if (artistLength > 25) {
                artist.style.fontSize = '0.75em';
            } else if (artistLength > 15) {
                artist.style.fontSize = '0.8em';
            } else {
                artist.style.fontSize = '0.9em';
            }
        }
    });
}

// Função para tocar uma música específica
function playTrack(index) {
    currentTrack = index;
    loadTrack();
    if (!isPlaying) {
        togglePlay();
    }
}

// Função para remover uma música da playlist
async function removeTrack(index) {
    if (index === currentTrack) {
        // Se estiver removendo a música atual, para a reprodução
        audio.pause();
        isPlaying = false;
    }
    
    const track = playlist[index];
    if (track.id) {
        try {
            await removeMusicFromDB(track.id);
        } catch (error) {
            console.error('Erro ao remover música do banco de dados:', error);
        }
    }
    
    playlist.splice(index, 1);
    
    if (currentTrack >= index && currentTrack > 0) {
        currentTrack--;
    }
    
    sortPlaylist();
    updatePlaylistHTML();
    
    if (playlist.length > 0) {
        loadTrack();
    } else {
        document.querySelector('.track-title').textContent = "Nenhuma música";
        document.querySelector('.artist-name').textContent = "";
        document.querySelector('.album-name').textContent = "";
        document.querySelector('.album-cover').src = resolveCoverUrl('musics/default-cover.jpg');
        document.querySelector('.progress-bar').style.width = "0%";
        document.querySelector('.current-time').textContent = "0:00";
        document.querySelector('.duration').textContent = "0:00";
    }
}

// Função para limpar toda a playlist
async function clearPlaylist() {
    if (confirm("Tem certeza que deseja limpar toda a playlist?")) {
        try {
            await clearMusicDB();
            
            audio.pause();
            isPlaying = false;
            
            playlist.length = 0;
            currentTrack = 0;
            
            updatePlaylistHTML();
            
            document.querySelector('.track-title').textContent = "Nenhuma música";
            document.querySelector('.artist-name').textContent = "";
            document.querySelector('.album-name').textContent = "";
            document.querySelector('.album-cover').src = resolveCoverUrl('musics/default-cover.jpg');
            document.querySelector('.progress-bar').style.width = "0%";
            document.querySelector('.current-time').textContent = "0:00";
            document.querySelector('.duration').textContent = "0:00";
        } catch (error) {
            console.error('Erro ao limpar banco de dados:', error);
            alert('Erro ao limpar a playlist');
        }
    }
}

// Função para salvar a playlist no localStorage
function savePlaylist() {
    const playlistData = playlist.map(track => ({
        ...track,
        file: track.file // Salva a URL do arquivo
    }));
    localStorage.setItem('musickeraPlaylist', JSON.stringify(playlistData));
}

// Salva a playlist com limitação de frequência para evitar excesso de gravações
let __saveScheduled = false;
function savePlaylistThrottled() {
    if (__saveScheduled) return;
    __saveScheduled = true;
    setTimeout(() => {
        __saveScheduled = false;
        try {
            savePlaylist();
        } catch (e) {
            console.error('Falha ao salvar playlist:', e);
        }
    }, 500);
}

// Função para carregar a playlist do localStorage
function loadPlaylist() {
    const savedPlaylist = localStorage.getItem('musickeraPlaylist');
    if (savedPlaylist) {
        const parsedPlaylist = JSON.parse(savedPlaylist);
        playlist.length = 0; // Limpa a playlist atual
        parsedPlaylist.forEach(track => {
            playlist.push(track);
        });
        updatePlaylistHTML();
        if (playlist.length > 0) {
            currentTrack = 0;
            loadTrack();
        }
    }
}

// Função para alternar modo de repetição
function toggleRepeat() {
    const repeatButton = document.getElementById('repeatButton');
    const repeatIcon = document.getElementById('repeatIcon');
    switch (repeatMode) {
        case 'none':
            repeatMode = 'one';
            repeatButton.classList.add('active');
            if (repeatIcon) repeatIcon.textContent = 'repeat_one';
            break;
        case 'one':
            repeatMode = 'all';
            repeatButton.classList.add('active');
            if (repeatIcon) repeatIcon.textContent = 'repeat';
            break;
        case 'all':
            repeatMode = 'none';
            repeatButton.classList.remove('active');
            if (repeatIcon) repeatIcon.textContent = 'repeat';
            break;
    }
}

// Inicialização quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    // Event Listeners
    document.querySelector('.progress-container').addEventListener('click', function(e) {
        const rect = this.getBoundingClientRect();
        const pos = (e.clientX - rect.left) / rect.width;
        audio.currentTime = pos * audio.duration;
    });

    document.querySelector('.volume-slider').addEventListener('input', function(e) {
        audio.volume = e.target.value / 100;
    });

    audio.addEventListener('timeupdate', function() {
        const progress = (audio.currentTime / audio.duration) * 100;
        document.querySelector('.progress-bar').style.width = progress + '%';
        document.querySelector('.current-time').textContent = formatTime(audio.currentTime);
    });

    audio.addEventListener('ended', function() {
        if (repeatMode === 'one') {
            audio.currentTime = 0;
            audio.play();
        } else if (repeatMode === 'all') {
            nextTrack();
        } else {
            if (currentTrack < playlist.length - 1) {
                nextTrack();
            }
        }
    });

    audio.addEventListener('error', function(e) {
        console.error('Erro no áudio:', e);
        const errorCode = audio.error ? audio.error.code : 'unknown';
        let errorMessage = 'Erro ao carregar a música.';
        
        switch(errorCode) {
            case 1:
                errorMessage = 'Erro ao carregar a música. O arquivo pode estar corrompido.';
                break;
            case 2:
                errorMessage = 'Erro de rede. Verifique sua conexão com a internet.';
                break;
            case 3:
                errorMessage = 'Formato de arquivo não suportado. Use .mp3, .m4a ou .webm.';
                break;
            case 4:
                errorMessage = 'Arquivo de música não encontrado.';
                break;
            default:
                errorMessage = 'Erro ao carregar a música. Verifique se o arquivo existe.';
        }
        
        alert(errorMessage);
    });

    // Adiciona o evento de redimensionamento
    window.addEventListener('resize', adjustFontSize);

    // Inicializa o player
    initDB().then(() => {
        loadPlaylist();
        updatePlaylistHTML();
        if (playlist.length > 0) {
            currentTrack = 0;
            loadTrack();
        }
    }).catch(error => {
        console.error('Erro ao inicializar o player:', error);
    });
});

// Exporta funções para uso global
window.playTrack = playTrack;
window.togglePlay = togglePlay;
window.nextTrack = nextTrack;
window.previousTrack = previousTrack;
window.toggleRepeat = toggleRepeat;
window.removeTrack = removeTrack;
window.clearPlaylist = clearPlaylist;


