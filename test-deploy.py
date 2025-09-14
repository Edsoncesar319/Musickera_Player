#!/usr/bin/env python3
"""
Script de teste para verificar o deploy no Vercel
"""

import requests
import json
import sys
from urllib.parse import urljoin

def test_api_endpoints(base_url):
    """Testa todos os endpoints da API"""
    print(f"🧪 Testando API em: {base_url}")
    print("=" * 50)
    
    # Lista de endpoints para testar
    endpoints = [
        ("/api/health", "Health Check"),
        ("/api/musics", "Lista de Músicas"),
        ("/api/playlist", "Playlist"),
        ("/api/search?q=jota", "Busca de Músicas")
    ]
    
    results = []
    
    for endpoint, description in endpoints:
        try:
            url = urljoin(base_url, endpoint)
            print(f"📡 Testando: {description}")
            print(f"   URL: {url}")
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"   ✅ Status: {response.status_code}")
                data = response.json()
                print(f"   📊 Resposta: {json.dumps(data, indent=2, ensure_ascii=False)}")
                results.append((endpoint, True, "Sucesso"))
            else:
                print(f"   ❌ Status: {response.status_code}")
                print(f"   📄 Resposta: {response.text}")
                results.append((endpoint, False, f"Status {response.status_code}"))
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Erro: {str(e)}")
            results.append((endpoint, False, str(e)))
        
        print("-" * 30)
    
    return results

def test_frontend(base_url):
    """Testa o frontend"""
    print(f"🌐 Testando Frontend em: {base_url}")
    print("=" * 50)
    
    try:
        response = requests.get(base_url, timeout=10)
        
        if response.status_code == 200:
            print("✅ Frontend carregado com sucesso")
            print(f"📄 Tamanho da resposta: {len(response.text)} bytes")
            return True
        else:
            print(f"❌ Status: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro: {str(e)}")
        return False

def main():
    """Função principal"""
    print("🚀 Teste de Deploy - Musickera Player")
    print("=" * 50)
    
    # URL base do projeto (substitua pela sua URL do Vercel)
    base_url = "https://musickera-player.vercel.app"
    
    # Teste do frontend
    frontend_ok = test_frontend(base_url)
    print()
    
    # Teste da API
    api_results = test_api_endpoints(base_url)
    print()
    
    # Resumo dos resultados
    print("📋 RESUMO DOS TESTES")
    print("=" * 50)
    
    print(f"Frontend: {'✅ OK' if frontend_ok else '❌ FALHOU'}")
    
    api_success = sum(1 for _, success, _ in api_results if success)
    api_total = len(api_results)
    
    print(f"API: {api_success}/{api_total} endpoints funcionando")
    
    for endpoint, success, message in api_results:
        status = "✅" if success else "❌"
        print(f"  {status} {endpoint}: {message}")
    
    # Recomendações
    print("\n💡 RECOMENDAÇÕES")
    print("=" * 50)
    
    if not frontend_ok:
        print("❌ Frontend não está carregando")
        print("   - Verifique se o arquivo index.html está na raiz")
        print("   - Confirme as configurações no vercel.json")
    
    if api_success < api_total:
        print("❌ Alguns endpoints da API falharam")
        print("   - Verifique os logs no dashboard do Vercel")
        print("   - Teste localmente: python api/index.py")
        print("   - Confirme as dependências em api/requirements.txt")
    
    if frontend_ok and api_success == api_total:
        print("🎉 Deploy funcionando perfeitamente!")
        print("   - Frontend carregando corretamente")
        print("   - API respondendo em todos os endpoints")
        print("   - Aplicação pronta para uso!")

if __name__ == "__main__":
    main()
