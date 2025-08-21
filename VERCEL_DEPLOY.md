# 🚀 Guia de Deploy no Vercel - Solução de Problemas

## Problemas Comuns e Soluções

### 1. Erro de Build
**Problema**: Build falha durante o deploy automático

**Solução**:
- ✅ Verifique se o arquivo `api/index.py` existe
- ✅ Confirme que `api/requirements.txt` está correto
- ✅ Certifique-se de que o `vercel.json` está configurado

### 2. Erro de CORS
**Problema**: Erro de CORS em produção

**Solução**:
- ✅ Configure as origens permitidas no `api/config.py`
- ✅ Adicione seu domínio Vercel na lista de origens

### 3. Erro de Dependências
**Problema**: Dependências Python não encontradas

**Solução**:
- ✅ Use versões específicas no `requirements.txt`
- ✅ Evite versões com `>=` ou `<=`

### 4. Erro de Timeout
**Problema**: Função serverless expira

**Solução**:
- ✅ Configure `maxDuration` no `vercel.json`
- ✅ Otimize o código para ser mais rápido

## Configurações Atualizadas

### vercel.json
```json
{
  "version": 2,
  "buildCommand": "bash vercel-build.sh",
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "15mb"
      }
    }
  ],
  "functions": {
    "api/index.py": {
      "maxDuration": 30,
      "runtime": "python3.9"
    }
  }
}
```

### api/requirements.txt
```
Flask==3.0.3
Flask-CORS==4.0.1
Werkzeug==3.0.1
```

## Passos para Deploy

1. **Fork do Repositório**
   ```bash
   git clone https://github.com/Edsoncesar319/Musickera_Player.git
   ```

2. **Conectar ao Vercel**
   - Acesse [vercel.com](https://vercel.com)
   - Faça login com GitHub
   - Clique em "New Project"
   - Importe o repositório

3. **Configurar Variáveis de Ambiente**
   - `MUSIC_DIR=/tmp/musics`
   - `COVERS_DIR=/tmp/covers`

4. **Deploy Automático**
   - O Vercel detectará automaticamente a configuração
   - A API será deployada em `/api/*`
   - O frontend será servido como arquivos estáticos

## Verificação de Deploy

### 1. Teste a API
```bash
curl https://seu-projeto.vercel.app/api/health
```

### 2. Teste o Frontend
```bash
curl https://seu-projeto.vercel.app/
```

### 3. Verifique os Logs
- Acesse o dashboard do Vercel
- Vá em "Functions" para ver os logs da API
- Verifique "Deployments" para logs de build

## Troubleshooting

### Build Falha
1. Verifique os logs no dashboard do Vercel
2. Teste localmente: `python api/index.py`
3. Verifique sintaxe Python: `python -m py_compile api/index.py`

### API Não Responde
1. Verifique se a função está sendo chamada
2. Teste o endpoint `/api/health`
3. Verifique configurações de CORS

### Arquivos Estáticos Não Carregam
1. Verifique se estão na pasta correta
2. Confirme as rotas no `vercel.json`
3. Teste URLs diretas dos arquivos

## Configurações Recomendadas

### Para Produção
- Use `config['production']` no código
- Configure domínios específicos no CORS
- Ative HTTPS
- Configure cache para arquivos estáticos

### Para Desenvolvimento
- Use `config['development']` no código
- Permita CORS de qualquer origem
- Ative logs detalhados

## Suporte

Se ainda houver problemas:
1. Verifique os logs no dashboard do Vercel
2. Teste localmente primeiro
3. Consulte a documentação do Vercel
4. Abra uma issue no GitHub

## Links Úteis

- [Documentação Vercel](https://vercel.com/docs)
- [Vercel Python Runtime](https://vercel.com/docs/runtimes#official-runtimes/python)
- [Flask no Vercel](https://vercel.com/guides/deploying-flask-with-vercel)
