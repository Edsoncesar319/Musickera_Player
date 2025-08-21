# Musickera - Player de Música Web

Um player de música web moderno e responsivo com suporte a upload de músicas, playlist e controles de reprodução.

## 🚀 Funcionalidades

- **Player de Música**
  - Reprodução de músicas MP3, WAV e OGG
  - Controles de play/pause, próximo/anterior
  - Barra de progresso interativa
  - Controle de volume
  - Modos de repetição (nenhum, uma música, todas)
  - Modo tela cheia

- **Playlist**
  - Lista de reprodução organizada
  - Busca de músicas
  - Upload de novas músicas
  - Visualização de capas de álbum
  - Informações de artista e álbum

- **Upload de Músicas**
  - Suporte a múltiplos arquivos
  - Barra de progresso de upload
  - Validação de tipos de arquivo
  - Tratamento de erros
  - Atualização automática da playlist

## 🛠️ Tecnologias Utilizadas

### Frontend
- HTML5
- CSS3 (com animações e gradientes)
- JavaScript (Vanilla)
- Design responsivo
- Animações CSS
- Gradientes e efeitos visuais

### Backend
- Python 3.x
- Flask (Framework web)
- Flask-CORS (Cross-Origin Resource Sharing)
- Werkzeug (Utilitários web)

## 📦 Estrutura do Projeto

```
musickera/
├── index.html          # Interface do usuário
├── server.py          # Servidor backend local
├── api/               # API para deploy (Vercel)
│   ├── index.py      # Endpoints da API
│   └── requirements.txt # Dependências da API
├── vercel.json        # Configuração do Vercel
├── requirements.txt   # Dependências Python locais
├── musics/           # Pasta de músicas
│   ├── *.m4a        # Arquivos de música
│   └── covers/      # Capas de álbum
└── README.md         # Documentação
```

## 🚀 Deploy para Produção

### Deploy no Vercel (Recomendado)

1. **Fork do Repositório**
   - Acesse [https://github.com/Edsoncesar319/Musickera_Player.git](https://github.com/Edsoncesar319/Musickera_Player.git)
   - Clique em "Fork" para criar sua cópia

2. **Conecte ao Vercel**
   - Acesse [vercel.com](https://vercel.com)
   - Faça login com sua conta GitHub
   - Clique em "New Project"
   - Importe o repositório forkado

3. **Configure as Variáveis de Ambiente**
   ```bash
   MUSIC_DIR=/tmp/musics
   COVERS_DIR=/tmp/covers
   ```

4. **Deploy Automático**
   - O Vercel detectará automaticamente a configuração
   - A API será deployada em `/api/*`
   - O frontend será servido como arquivos estáticos

### Deploy Manual no GitHub

1. **Clone o Repositório**
   ```bash
   git clone https://github.com/Edsoncesar319/Musickera_Player.git
   cd Musickera_Player
   ```

2. **Configure o Git**
   ```bash
   git config user.name "Seu Nome"
   git config user.email "seu.email@exemplo.com"
   ```

3. **Adicione e Commit as Mudanças**
   ```bash
   git add .
   git commit -m "Configuração para deploy com backend"
   ```

4. **Push para o Repositório**
   ```bash
   git push origin main
   ```

## 🔧 Instalação Local

1. Clone o repositório:
```bash
git clone https://github.com/Edsoncesar319/Musickera_Player.git
cd Musickera_Player
```

2. Instale as dependências Python:
```bash
pip install -r requirements.txt
```

3. Inicie o servidor local:
```bash
python server.py
```

4. Abra o arquivo `index.html` no navegador ou acesse `http://localhost:5000`

## 💻 Uso

### Player de Música
- Clique no botão play/pause para controlar a reprodução
- Use os botões de próximo/anterior para navegar entre músicas
- Ajuste o volume usando o controle deslizante
- Clique na barra de progresso para pular para um ponto específico
- Use o botão de repetição para alternar entre os modos de repetição
- Clique no botão de tela cheia para expandir o player

### Playlist
- Clique em uma música para reproduzi-la
- Use a barra de busca para filtrar músicas
- Clique no botão de upload para adicionar novas músicas
- As músicas são organizadas automaticamente por artista e álbum

### Upload de Músicas
- Clique no botão "Upload"
- Selecione um ou mais arquivos de música
- Aguarde o upload ser concluído
- As novas músicas aparecerão automaticamente na playlist

## 🌐 API Endpoints

### Produção (Vercel)
- `GET /api/musics` - Lista todas as músicas
- `GET /api/search?q=termo` - Busca músicas
- `GET /api/health` - Verificação de saúde
- `GET /api/playlist` - Lista playlists

### Local
- `GET /musics` - Lista músicas locais
- `POST /upload` - Upload de músicas
- `GET /musics/<filename>` - Download de música

## 🔒 Segurança

- Validação de tipos de arquivo
- Nomes de arquivo seguros
- Permissões de arquivo configuradas
- Limite de tamanho de upload (100MB)
- CORS configurado para desenvolvimento

## 🐛 Logs e Debug

- Logs detalhados no arquivo `server.log`
- Mensagens de erro no console do navegador
- Feedback visual para erros de upload
- Status de upload em tempo real

## 📝 Notas de Desenvolvimento

### Backend Local (server.py)
- Servidor Flask na porta 5000
- Suporte a CORS para desenvolvimento
- Rotas para upload e listagem de músicas
- Tratamento de erros e logging
- Configuração de permissões de arquivo

### Backend Produção (api/index.py)
- API serverless para Vercel
- Endpoints otimizados para produção
- Respostas JSON padronizadas
- Tratamento de erros robusto

### Frontend (index.html)
- Interface moderna e responsiva
- Animações suaves
- Controles de reprodução intuitivos
- Sistema de upload com feedback visual
- Busca em tempo real

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## ✨ Créditos

- Desenvolvido com ❤️ para amantes de música
- Interface inspirada em players modernos
- Animações e efeitos visuais personalizados
- Deploy otimizado para Vercel

## 🔗 Links Úteis

- **Repositório Original**: [https://github.com/Edsoncesar319/Musickera_Player.git](https://github.com/Edsoncesar319/Musickera_Player.git)
- **Demo Online**: [musickeraPlus.vercel.app](https://musickeraPlus.vercel.app)
- **Vercel**: [vercel.com](https://vercel.com) 
