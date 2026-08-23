import psycopg
import json
import os

DB_URL = "postgresql://postgres:postgres@localhost:5432/reporadar"
WEB_DIR = r"C:\temp\opensource-hunter-web"

# 1. Carrega as 536 ferramentas curadas originais
tools_path = os.path.join(WEB_DIR, "tools.json")
with open(tools_path, "r", encoding="utf-8") as f:
    curated_tools = json.load(f)

print(f"1. Ferramentas Curadas Originais: {len(curated_tools)}")

# 2. Busca os repositórios do PostgreSQL local
pg_tools = []
with psycopg.connect(DB_URL) as conn:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT DISTINCT ON (r.id) r.full_name, r.description, COALESCE(s.stars, 0), r.html_url, r.primary_language, r.topics
            FROM repos r
            LEFT JOIN repo_snapshots s ON r.id = s.repo_id
            WHERE r.description IS NOT NULL AND length(r.description) > 5
            ORDER BY r.id, s.stars DESC NULLS LAST
        """)
        rows = cur.fetchall()
        for row in rows:
            name, desc, stars, url, lang, topics = row
            pg_tools.append({
                "nome": name,
                "caso_uso": desc[:250].strip(),
                "origem": "Índice Global (GitHub)",
                "link_ig": None,
                "github_search": url or f"https://github.com/{name}",
                "estrelas": stars,
                "linguagem": lang or "N/A"
            })

print(f"2. Repositórios Únicos do PostgreSQL: {len(pg_tools)}")

# 3. Categorizador Inteligente
def categorizar(nome, caso_uso):
    texto = (nome + " " + (caso_uso or "")).lower()
    if any(k in texto for k in ["mcp", "code", "coding", "turborepo", "strix", "cli", "terminal", "ide", "programação", "pentest", "desenvolvedor", "compiler", "parser", "typescript", "rust"]):
        return "Dev, Coding & MCP", "💻"
    elif any(k in texto for k in ["agent", "agente", "multi-agent", "mirofish", "miroshark", "deerflow", "eigent", "openworker", "conway", "langchain", "langsmith", "orquestração", "swarm"]):
        return "Multi-Agentes & Frameworks", "🤖"
    elif any(k in texto for k in ["tts", "audio", "áudio", "voz", "voxtral", "elevenlabs", "pocket tts", "kyutai", "deepgram", "livekit", "fala", "speech", "asr", "whisper"]):
        return "Voz, Áudio & TTS", "🎙️"
    elif any(k in texto for k in ["video", "vídeo", "3d", "sam 3d", "vision", "imagem", "veo", "imagine", "luma", "openart", "pika", "lingbot", "avatar", "render", "blender", "cad", "gis", "map"]):
        return "Vídeo, Visão, 3D & GIS", "👁️"
    elif any(k in texto for k in ["crawlee", "scrape", "scraping", "n8n", "zapier", "pipefy", "workflow", "automação", "apify", "crawler", "bot", "fluxo", "automation"]):
        return "Automação & Scraping", "⚡"
    elif any(k in texto for k in ["ads", "marketing", "meta ads", "vendas", "funil", "tráfego", "lead", "negócio", "imobiliário", "receita", "sms", "crm", "real estate"]):
        return "Marketing, CRM & Negócios", "📈"
    elif any(k in texto for k in ["llm", "claude", "gemini", "kimi", "qwen", "glm", "openrouter", "airllm", "perplexity", "deepseek", "mistral", "anthropic", "gpt", "model", "embedding", "vector", "transformer"]):
        return "Modelos LLM & IA", "🧠"
    else:
        return "Geral & Produtividade", "🛠️"

# Normaliza Curadoria
for t in curated_tools:
    cat, emoji = categorizar(t["nome"], t.get("caso_uso", ""))
    t["categoria"] = cat
    t["emoji"] = emoji
    t.setdefault("origem", "Curadoria Borin (Instagram)")
    t.setdefault("estrelas", 0)
    t.setdefault("linguagem", "Curated")

# Normaliza PG Tools
for t in pg_tools:
    cat, emoji = categorizar(t["nome"], t.get("caso_uso", ""))
    t["categoria"] = cat
    t["emoji"] = emoji

# Combina com as Curadas no topo
merged = curated_tools + pg_tools
print(f"3. Total Combinado Final: {len(merged)} ferramentas!")

# Salva tools.json mesclado
with open(os.path.join(WEB_DIR, "tools_master.json"), "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False)

file_size_mb = os.path.getsize(os.path.join(WEB_DIR, "tools_master.json")) / (1024 * 1024)
print(f"4. Tamanho do JSON bruto: {file_size_mb:.2f} MB (será compactado para < 600 KB na Vercel/CDN)")
