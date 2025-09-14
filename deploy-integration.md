# Guia de Integração Frontend-Backend

## Resumo das Alterações Realizadas

### 1. Frontend (frontend/js/app.js e frontend/index.html)
- ✅ Atualizado `API_BASE_URL` para apontar para o backend deployado: `https://automatic-giggle-wr97449prwrrc97v7.github.dev`
- ✅ Substituído todas as chamadas hardcoded `http://localhost:5000` por `${API_BASE_URL}`
- ✅ Endpoints atualizados:
  - `/extract_playlist_name`
  - `/download_playlist`
  - `/list_playlists`
  - `/create_playlist`
  - `/list_music`
  - `/musics/*` (para arquivos de música)

### 2. Backend (backend/api/index.py)
- ✅ Adicionados endpoints faltantes para compatibilidade com o frontend:
  - `GET /list_playlists` - Lista playlists disponíveis
  - `GET /list_music` - Lista músicas de uma playlist
  - `POST /create_playlist` - Cria nova playlist
  - `POST /extract_playlist_name` - Extrai nome de playlist do YouTube
  - `POST /download_playlist` - Download de playlist do YouTube
- ✅ Implementação com dados estáticos para Vercel (serverless)

### 3. Configuração CORS
- ✅ Atualizado `backend/api/config.py` para incluir o domínio do frontend
- ✅ Atualizado `backend/config/settings.py` para incluir o domínio do frontend

### 4. Vercel Configuration (vercel.json)
- ✅ Atualizado roteamento para direcionar endpoints do frontend para o backend
- ✅ Adicionada rota para `/musics/*` para servir arquivos de música

## Como Testar a Integração

### 1. Teste Automático
Abra o arquivo `test-integration.html` no navegador para executar testes automáticos da integração.

### 2. Teste Manual
1. Acesse o frontend deployado
2. Verifique se as playlists são carregadas
3. Teste a criação de novas playlists
4. Verifique se as músicas são listadas corretamente

### 3. Verificação de Logs
- Abra o DevTools do navegador (F12)
- Vá para a aba Console
- Verifique se não há erros de CORS ou conexão
- Verifique se as chamadas para a API estão sendo feitas corretamente

## Endpoints Disponíveis

### Backend (https://automatic-giggle-wr97449prwrrc97v7.github.dev)
- `GET /api/health` - Health check da API
- `GET /api/musics` - Lista músicas (endpoint original)
- `GET /api/search` - Busca músicas
- `GET /api/playlist` - Lista playlists (endpoint original)
- `GET /list_playlists` - Lista playlists (compatibilidade)
- `GET /list_music` - Lista músicas (compatibilidade)
- `POST /create_playlist` - Cria playlist
- `POST /extract_playlist_name` - Extrai nome de playlist
- `POST /download_playlist` - Download de playlist
- `GET /musics/*` - Serve arquivos de música
- `GET /musics/covers/*` - Serve capas de álbuns

## Próximos Passos

1. **Deploy das Alterações**: Faça commit e push das alterações para o repositório
2. **Verificação**: Teste a integração usando o arquivo de teste
3. **Monitoramento**: Verifique logs de erro no Vercel
4. **Otimização**: Considere implementar cache para melhor performance

## Troubleshooting

### Erro de CORS
- Verifique se o domínio do frontend está na lista `CORS_ORIGINS`
- Verifique se o backend está retornando headers CORS corretos

### Erro 404
- Verifique se as rotas estão configuradas corretamente no `vercel.json`
- Verifique se os endpoints existem no backend

### Erro de Conexão
- Verifique se o backend está deployado e funcionando
- Teste o endpoint `/api/health` diretamente

## Arquivos Modificados

1. `frontend/js/app.js` - URL da API
2. `frontend/index.html` - URLs hardcoded
3. `backend/api/index.py` - Novos endpoints
4. `backend/api/config.py` - CORS
5. `backend/config/settings.py` - CORS
6. `vercel.json` - Roteamento
7. `test-integration.html` - Arquivo de teste (novo)
