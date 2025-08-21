# 🚀 Guia de Deploy - Musickera Player

## 📋 Pré-requisitos

- Conta no [GitHub](https://github.com)
- Conta no [Vercel](https://vercel.com)
- Git instalado no seu computador

## 🔄 Passo a Passo para Deploy

### 1. Fork do Repositório

1. Acesse: [https://github.com/Edsoncesar319/Musickera_Player.git](https://github.com/Edsoncesar319/Musickera_Player.git)
2. Clique no botão **"Fork"** (canto superior direito)
3. Escolha sua conta GitHub para fazer o fork
4. Aguarde a criação do fork

### 2. Deploy no Vercel

1. **Acesse o Vercel**
   - Vá para [vercel.com](https://vercel.com)
   - Faça login com sua conta GitHub

2. **Crie um Novo Projeto**
   - Clique em **"New Project"**
   - Selecione o repositório forkado do Musickera_Player
   - Clique em **"Import"**

3. **Configure o Projeto**
   - **Project Name**: `musickera-player` (ou o nome que preferir)
   - **Framework Preset**: Deixe como **"Other"**
   - **Root Directory**: Deixe vazio (padrão)
   - **Build Command**: Deixe vazio
   - **Output Directory**: Deixe vazio

4. **Configure as Variáveis de Ambiente**
   - Clique em **"Environment Variables"**
   - Adicione as seguintes variáveis:
     ```
     MUSIC_DIR=/tmp/musics
     COVERS_DIR=/tmp/covers
     ```

5. **Deploy**
   - Clique em **"Deploy"**
   - Aguarde o processo de build e deploy

### 3. Configuração Pós-Deploy

1. **Verifique o Deploy**
   - Após o deploy, você receberá uma URL (ex: `https://musickera-player.vercel.app`)
   - Teste a aplicação acessando a URL

2. **Teste as Funcionalidades**
   - Frontend: A interface deve carregar normalmente
   - API: Teste os endpoints em `/api/health`, `/api/musics`

3. **Configuração de Domínio Personalizado (Opcional)**
   - No painel do Vercel, vá em **"Settings"** > **"Domains"**
   - Adicione seu domínio personalizado se desejar

## 🔧 Estrutura do Deploy

```
📁 Musickera_Player/
├── 🌐 index.html          # Frontend (servido como estático)
├── ⚙️ vercel.json         # Configuração do Vercel
├── 🔌 api/
│   ├── 🐍 index.py        # Backend serverless
│   └── 📦 requirements.txt # Dependências Python
└── 📚 README.md           # Documentação
```

## 🌐 Endpoints da API

### ✅ Funcionando em Produção
- `GET /api/health` - Status da API
- `GET /api/musics` - Lista de músicas
- `GET /api/search?q=termo` - Busca de músicas
- `GET /api/playlist` - Lista de playlists

### ⚠️ Requer Configuração Adicional
- `/musics/*` - Arquivos de música (CDN necessário)
- `/musics/covers/*` - Capas de álbum (CDN necessário)

## 🎯 Próximos Passos para Produção

### 1. Configurar CDN para Músicas
Para servir as músicas em produção, você pode:

- **AWS S3 + CloudFront**
- **Google Cloud Storage + CDN**
- **Azure Blob Storage + CDN**
- **Cloudinary** (para músicas e imagens)

### 2. Banco de Dados
Para funcionalidades avançadas:

- **MongoDB Atlas** (gratuito)
- **Supabase** (PostgreSQL)
- **PlanetScale** (MySQL)

### 3. Autenticação
Para usuários e playlists pessoais:

- **Auth0**
- **Firebase Auth**
- **Supabase Auth**

## 🐛 Troubleshooting

### Problema: "API não responde"
**Solução**: Verifique se as variáveis de ambiente estão configuradas no Vercel

### Problema: "Erro 500 na API"
**Solução**: Verifique os logs no painel do Vercel em **"Functions"**

### Problema: "Músicas não carregam"
**Solução**: Configure um CDN ou armazenamento externo para os arquivos

## 📞 Suporte

- **Issues**: [GitHub Issues](https://github.com/Edsoncesar319/Musickera_Player/issues)
- **Documentação**: [README.md](README.md)
- **Vercel Docs**: [vercel.com/docs](https://vercel.com/docs)

## 🎉 Deploy Concluído!

Após seguir todos os passos, sua aplicação estará rodando com:
- ✅ Frontend responsivo e moderno
- ✅ Backend serverless funcionando
- ✅ API endpoints ativos
- ✅ Deploy automático a cada push
- ✅ HTTPS e CDN global

**URL da sua aplicação**: `https://[seu-projeto].vercel.app`
