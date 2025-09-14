# Musickêra - Player de Música

Um player de música moderno e responsivo com suporte a múltiplas plataformas (Deezer, YouTube Music, Sua Música) e gerenciamento de playlists locais.

## 🏗️ Estrutura do Projeto

```
playmusic-main/
├── frontend/                 # Camada de Front-end
│   ├── assets/              # Recursos estáticos
│   │   └── favicon.ico
│   ├── css/                 # Estilos CSS
│   │   └── styles.css
│   ├── js/                  # JavaScript
│   │   └── app.js
│   └── index.html           # Página principal
├── backend/                 # Camada de Back-end
│   ├── src/                 # Código fonte
│   ├── config/              # Configurações
│   ├── utils/               # Utilitários
│   ├── api/                 # API para Vercel
│   │   ├── index.py
│   │   └── requirements.txt
│   ├── musics/              # Biblioteca de músicas
│   │   ├── covers/          # Capas dos álbuns
│   │   └── [playlists]/     # Pastas de playlists
│   ├── server.py            # Servidor principal
│   ├── requirements.txt     # Dependências Python
│   ├── test_playlists.py    # Testes de playlists
│   └── remove_duplicates.py # Utilitário para remover duplicados
├── README.md               # Documentação principal
├── DEPLOY.md              # Guia de deploy
├── LICENSE                # Licença
└── vercel.json            # Configuração Vercel
```

## 🚀 Funcionalidades

### Front-end
- **Interface Moderna**: Design responsivo com tema escuro
- **Player Avançado**: Controles de reprodução, volume e progresso
- **Busca Inteligente**: Integração com Deezer, YouTube Music e Sua Música
- **Gerenciamento de Playlists**: Criação, edição e organização de playlists
- **Upload de Arquivos**: Suporte a múltiplos formatos de áudio
- **IndexedDB**: Armazenamento local para melhor performance
- **Controles de Volume**: Master, canais individuais e balance

### Back-end
- **API RESTful**: Endpoints para gerenciamento de músicas e playlists
- **Download de Playlists**: Integração com YouTube Music via yt-dlp
- **Processamento de Metadados**: Extração automática de informações de áudio
- **Sistema de Playlists**: Organização por pastas
- **CORS**: Suporte para requisições cross-origin
- **Deploy Vercel**: Configuração para deploy serverless

## 🛠️ Tecnologias

### Front-end
- **HTML5**: Estrutura semântica
- **CSS3**: Estilos modernos com Flexbox e Grid
- **JavaScript ES6+**: Funcionalidades avançadas
- **IndexedDB**: Banco de dados local
- **Web Audio API**: Controles de áudio avançados

### Back-end
- **Python 3.8+**: Linguagem principal
- **Flask**: Framework web
- **yt-dlp**: Download de conteúdo do YouTube
- **mutagen**: Processamento de metadados de áudio
- **Flask-CORS**: Suporte a CORS

## 📦 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- Node.js (opcional, para desenvolvimento front-end)

### Back-end
```bash
cd backend
pip install -r requirements.txt
python server.py
```

### Front-end
```bash
cd frontend
# Abra index.html em um navegador moderno
# Ou use um servidor local:
python -m http.server 8000
```

## 🔧 Configuração

### Variáveis de Ambiente
```bash
# Backend
MUSIC_DIR=/path/to/musics
COVERS_DIR=/path/to/covers
PORT=5000

# Frontend
API_BASE_URL=http://localhost:5000
```

### Estrutura de Pastas de Música
```
musics/
├── covers/              # Capas dos álbuns
├── Playlist 1/         # Playlist organizada
├── Playlist 2/         # Outra playlist
└── Geral/              # Músicas gerais
```

## 🎵 Formatos Suportados

- **Áudio**: MP3, M4A, AAC, OGG, OPUS, WAV, FLAC, WebM
- **Metadados**: ID3, MP4 tags
- **Covers**: JPG, PNG, WebP

## 🔌 APIs Integradas

- **Deezer API**: Busca e streaming de músicas
- **YouTube Music**: Download de playlists e vídeos
- **Sua Música**: Busca de conteúdo brasileiro

## 🚀 Deploy

### Vercel (Recomendado)
```bash
# Configure o vercel.json
vercel --prod
```

### Heroku
```bash
# Configure o Procfile
git push heroku main
```

### Local
```bash
# Backend
python server.py

# Frontend
python -m http.server 8000
```

## 📱 Responsividade

O aplicativo é totalmente responsivo e funciona em:
- **Desktop**: Interface completa com todos os controles
- **Tablet**: Layout adaptado para telas médias
- **Mobile**: Interface otimizada para touch

## 🔒 Segurança

- **CORS**: Configurado para permitir requisições do front-end
- **Validação**: Verificação de tipos de arquivo
- **Sanitização**: Limpeza de nomes de arquivo
- **Rate Limiting**: Proteção contra spam

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🆘 Suporte

- **Issues**: Use o GitHub Issues para reportar bugs
- **Discussions**: Use o GitHub Discussions para perguntas
- **Wiki**: Documentação detalhada no Wiki do projeto

## 🔄 Changelog

### v2.0.0
- ✅ Separação completa de front-end e back-end
- ✅ Estrutura organizada de pastas
- ✅ CSS e JavaScript em arquivos separados
- ✅ Melhor organização do código
- ✅ Documentação atualizada

### v1.0.0
- ✅ Player de música básico
- ✅ Integração com Deezer
- ✅ Sistema de playlists
- ✅ Upload de arquivos 
