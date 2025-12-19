import requests
import time
import csv

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🕵️ GITHUB PROJECT HUNTER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Descrição: Busca repositórios no GitHub baseados em keywords.
# Objetivo: Encontrar ferramentas, scripts e templates para revender ou usar.
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def search_github(query, min_stars=100, limit=50):
    """Busca repositórios no GitHub."""
    print(f"🔍 Buscando por: '{query}' com no mínimo {min_stars} estrelas...")
    
    api_url = "https://api.github.com/search/repositories"
    params = {
        'q': f'{query} stars:>{min_stars}',
        'sort': 'stars',
        'order': 'desc',
        'per_page': limit
    }
    
    headers = {'Accept': 'application/vnd.github.v3+json'}
    
    try:
        response = requests.get(api_url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        items = data.get('items', [])
        print(f"✅ Encontrados {len(items)} projetos incríveis!\n")
        return items
        
    except Exception as e:
        print(f"❌ Erro na busca: {e}")
        return []

def save_results(repos, filename="github_gems.csv"):
    """Salva os resultados em CSV."""
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Nome', 'Estrelas', 'URL', 'Descrição'])
        
        for repo in repos:
            writer.writerow([
                repo['name'],
                repo['stargazers_count'],
                repo['html_url'],
                repo['description']
            ])
            print(f"⭐ {repo['stargazers_count']} | {repo['name']}")
            
    print(f"\n💾 Lista salva em: {filename}")

if __name__ == "__main__":
    # 🎯 O QUE VOCÊ QUER ENCONTRAR HOJE?
    # Exemplos: "whatsapp bot", "instagram automation", "web scraper", "landing page template"
    KEYWORD = "web scraping tool" 
    
    repos = search_github(KEYWORD, min_stars=500, limit=30)
    
    if repos:
        save_results(repos)
        print("\n🚀 DICA: Abra o CSV e procure por projetos que você pode vender como serviço!")
