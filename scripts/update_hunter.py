import os
import sys
import json
import requests
from datetime import datetime, timedelta

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY", "")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

def fetch_trending_repos():
    print("🔍 Buscando repositórios em alta no GitHub (AI, MCP, Agents, LLM)...")
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"

    # Últimos 7 dias
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    queries = [
        f"topic:mcp created:>{seven_days_ago} stars:>20",
        f"topic:multi-agent created:>{seven_days_ago} stars:>30",
        f"topic:llm created:>{seven_days_ago} stars:>50",
        f"topic:ai-agent created:>{seven_days_ago} stars:>50",
    ]

    discovered = []
    for q in queries:
        url = f"https://api.github.com/search/repositories?q={q}&sort=stars&order=desc&per_page=10"
        try:
            r = requests.get(url, headers=headers, timeout=15)
            if r.status_code == 200:
                items = r.json().get("items", [])
                for item in items:
                    discovered.append({
                        "name": item.get("name", ""),
                        "full_name": item.get("full_name", ""),
                        "description": item.get("description", "") or "",
                        "html_url": item.get("html_url", ""),
                        "stars": item.get("stargazers_count", 0),
                        "language": item.get("language", "") or "Geral"
                    })
        except Exception as e:
            print(f"Aviso ao buscar query '{q}': {e}")
            
    return discovered

def process_with_nvidia(repo):
    if not NVIDIA_API_KEY:
        return None

    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""Analise este repositório do GitHub e retorne um JSON estrito no formato abaixo:
Nome: {repo['name']}
Descrição: {repo['description']}
URL: {repo['html_url']}

Formato de Resposta (JSON estrito apenas, sem markdown):
{{
  "nome": "Nome limpo da ferramenta",
  "caso_uso": "Resumo de 1 frase clara em português de para que serve e benefícios",
  "categoria": "Uma de: Dev, Coding & MCP | Multi-Agentes & Frameworks | Voz, Áudio & TTS | Vídeo, Visão & 3D | Automação & Scraping | Marketing, Ads & Funis | Modelos LLM & Infra | Geral & Produtividade",
  "emoji": "Um emoji representativo"
}}"""

    payload = {
        "model": "meta/llama-3.1-70b-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 150
    }

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=20)
        if r.status_code == 200:
            content = r.json()["choices"][0]["message"]["content"].strip()
            # Limpa possíveis crases de markdown
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            data = json.loads(content.strip())
            data["busca_github"] = f"https://github.com/{repo['full_name']}"
            data["link_post"] = f"https://github.com/{repo['full_name']}"
            return data
    except Exception as e:
        print(f"Erro ao processar {repo['name']} com NVIDIA: {e}")
    return None

def main():
    tools_file = "tools.json"
    if not os.path.exists(tools_file):
        print(f"Arquivo {tools_file} não encontrado.")
        return

    with open(tools_file, "r", encoding="utf-8") as f:
        existing_tools = json.load(f)

    existing_names = {t["nome"].lower().strip() for t in existing_tools}
    existing_urls = {t.get("busca_github", "").lower().strip() for t in existing_tools}

    print(f"📊 Total atual de ferramentas no catálogo: {len(existing_tools)}")
    
    trending = fetch_trending_repos()
    print(f"🔍 Repositórios descobertos no GitHub: {len(trending)}")

    added_count = 0
    for repo in trending:
        name_clean = repo["name"].lower().strip()
        url_clean = repo["html_url"].lower().strip()

        if name_clean in existing_names or url_clean in existing_urls:
            continue

        print(f"🧠 Processando com NVIDIA Llama 3.1 70B: {repo['full_name']} ({repo['stars']} ⭐)...")
        tool_data = process_with_nvidia(repo)
        if tool_data and tool_data.get("nome"):
            existing_tools.insert(0, tool_data)
            existing_names.add(name_clean)
            added_count += 1
            print(f"✅ Adicionada: {tool_data['nome']} [{tool_data['categoria']}]")

    print(f"🎉 Novas ferramentas adicionadas com sucesso: {added_count}")

    if added_count > 0:
        with open(tools_file, "w", encoding="utf-8") as f:
            json.dump(existing_tools, f, ensure_ascii=False, indent=2)

        # Regenera index.html
        os.system("python build_app.py")
        print("🚀 index.html reconstruído com sucesso para deploy!")

if __name__ == "__main__":
    main()
