import json
import os
import psycopg

WEB_DIR = r"C:\temp\opensource-hunter-web"
DB_URL = "postgresql://postgres:postgres@localhost:5432/reporadar"

# 1. Carrega as 560 ferramentas curadas originais
tools_path = os.path.join(WEB_DIR, "tools.json")
with open(tools_path, "r", encoding="utf-8") as f:
    curated_tools = json.load(f)

print(f"[1/4] Ferramentas Curadas Carregadas: {len(curated_tools)}")

# 2. Busca os repositórios do PostgreSQL local
pg_tools = []
try:
    with psycopg.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT DISTINCT ON (r.id) r.full_name, r.description, COALESCE(s.stars, 0), r.html_url, r.primary_language
                FROM repos r
                LEFT JOIN repo_snapshots s ON r.id = s.repo_id
                WHERE r.description IS NOT NULL AND length(r.description) > 5
                ORDER BY r.id, s.stars DESC NULLS LAST
            """)
            rows = cur.fetchall()
            for row in rows:
                name, desc, stars, url, lang = row
                pg_tools.append({
                    "nome": name,
                    "caso_uso": desc[:280].strip(),
                    "origem": "Índice Global GitHub",
                    "link_ig": None,
                    "github_search": url or f"https://github.com/{name}",
                    "estrelas": int(stars or 0),
                    "linguagem": lang or "N/A"
                })
    print(f"[2/4] Repositórios Únicos do PostgreSQL: {len(pg_tools)}")
except Exception as e:
    print(f"Aviso ao ler PostgreSQL: {e}")

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

for t in curated_tools:
    cat, emoji = categorizar(t["nome"], t.get("caso_uso", ""))
    t["categoria"] = cat
    t["emoji"] = emoji
    t.setdefault("origem", "Curadoria Borin (Instagram)")
    t.setdefault("estrelas", 0)
    t.setdefault("linguagem", "Curadoria VIP")

for t in pg_tools:
    cat, emoji = categorizar(t["nome"], t.get("caso_uso", ""))
    t["categoria"] = cat
    t["emoji"] = emoji

merged_tools = curated_tools + pg_tools
print(f"[3/4] Total Combinado de Ferramentas: {len(merged_tools)}")

# Salva tools.json e CSV
with open(os.path.join(WEB_DIR, "tools.json"), "w", encoding="utf-8") as f:
    json.dump(merged_tools, f, ensure_ascii=False)

import csv
with open(os.path.join(WEB_DIR, "catalogo_mobile.csv"), "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Nome", "Caso de Uso", "Categoria", "Linguagem", "Estrelas", "Origem", "Link Instagram", "GitHub / URL"])
    for t in merged_tools:
        writer.writerow([
            t.get("nome", ""),
            t.get("caso_uso", ""),
            t.get("categoria", ""),
            t.get("linguagem", ""),
            t.get("estrelas", 0),
            t.get("origem", ""),
            t.get("link_ig", ""),
            t.get("github_search", "")
        ])

tools_json_str = json.dumps(merged_tools, ensure_ascii=False)

# 4. Gera index.html de Alta Performance com Paginação Infinita
html_code = f"""<!DOCTYPE html>
<html lang="pt-BR" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenSource Hunter | Rodrigo Borin</title>
    <meta name="description" content="Catálogo Mestre e Motor de Busca de {len(merged_tools):,} Ferramentas Open Source e Inteligência Artificial por Rodrigo Borin.">
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    fontFamily: {{
                        sans: ['"Plus Jakarta Sans"', 'sans-serif'],
                        mono: ['"JetBrains Mono"', 'monospace'],
                    }},
                    colors: {{
                        brand: {{
                            50: '#eef2ff',
                            100: '#e0e7ff',
                            400: '#818cf8',
                            500: '#6366f1',
                            600: '#4f46e5',
                            700: '#4338ca',
                        }},
                        dark: {{
                            950: '#070b14',
                            900: '#0b1120',
                            850: '#0f172a',
                            800: '#1e293b',
                            750: '#283548',
                            700: '#334155',
                        }}
                    }}
                }}
            }}
        }}
    </script>
    <style>
        .no-scrollbar::-webkit-scrollbar {{ display: none; }}
        .no-scrollbar {{ -ms-overflow-style: none; scrollbar-width: none; }}
        .glass-panel {{
            background: rgba(15, 23, 42, 0.85);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
        }}
    </style>
</head>
<body class="bg-dark-950 text-slate-100 min-h-screen flex flex-col font-sans selection:bg-brand-500 selection:text-white">

    <!-- Top Navigation Bar -->
    <header class="sticky top-0 z-50 glass-panel border-b border-dark-800 px-4 py-3 sm:px-6">
        <div class="max-w-7xl mx-auto flex items-center justify-between gap-4">
            <div class="flex items-center space-x-3">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-600 to-indigo-400 flex items-center justify-center shadow-lg shadow-indigo-500/20 ring-1 ring-white/20">
                    <span class="text-xl">🏹</span>
                </div>
                <div>
                    <div class="flex items-center space-x-2">
                        <h1 class="font-extrabold text-lg sm:text-xl tracking-tight text-white">OpenSource Hunter</h1>
                        <span class="text-[10px] uppercase font-bold tracking-widest bg-brand-500/20 text-brand-400 border border-brand-500/30 px-2 py-0.5 rounded-full">v2.5 Mega</span>
                    </div>
                    <p class="text-xs text-slate-400 font-medium">rodrigoborin.com • <span class="text-emerald-400 font-semibold" id="totalHeaderCount">{len(merged_tools):,} Ferramentas</span></p>
                </div>
            </div>

            <!-- View Modes (Tabs) -->
            <div class="flex items-center bg-dark-900 border border-dark-750 p-1 rounded-xl text-xs font-semibold">
                <button onclick="switchTab('catalogo')" id="tabBtnCatalogo" class="tab-btn px-3 py-1.5 rounded-lg bg-brand-600 text-white shadow-sm transition">
                    🧭 Acervo Mestre ({len(merged_tools):,})
                </button>
                <button onclick="switchTab('github')" id="tabBtnGithub" class="tab-btn px-3 py-1.5 rounded-lg text-slate-400 hover:text-white transition">
                    🌐 GitHub Live
                </button>
                <button onclick="switchTab('obsidian')" id="tabBtnObsidian" class="tab-btn px-3 py-1.5 rounded-lg text-slate-400 hover:text-white transition">
                    📓 Obsidian Vault
                </button>
            </div>
        </div>

        <!-- Search Bar -->
        <div class="max-w-7xl mx-auto mt-3" id="searchBarContainer">
            <div class="relative flex items-center">
                <input type="text" id="mainSearchInput" placeholder="Buscar entre {len(merged_tools):,} ferramentas por nome, caso de uso, LLM, MCP, Python, Rust..." 
                    class="w-full bg-dark-900 border border-dark-750 text-white placeholder-slate-400 text-sm sm:text-base rounded-xl pl-11 pr-24 py-3 focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent transition shadow-inner">
                <div class="absolute left-3.5 text-slate-400">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                    </svg>
                </div>
                <button onclick="clearSearch()" id="clearSearchBtn" class="hidden absolute right-3 text-xs bg-dark-750 hover:bg-dark-700 text-slate-300 px-2.5 py-1.5 rounded-lg transition font-medium">
                    Limpar
                </button>
            </div>
        </div>

        <!-- Category Pills -->
        <div class="max-w-7xl mx-auto mt-3 flex space-x-2 overflow-x-auto no-scrollbar pb-1 text-xs" id="categoryPillBar">
            <button onclick="filterCategory('TODAS')" class="cat-pill active px-3.5 py-2 rounded-xl bg-brand-600 text-white whitespace-nowrap font-semibold transition shadow-sm">
                Todas ({len(merged_tools):,})
            </button>
        </div>
    </header>

    <!-- Main Content Container -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 mt-6 flex-1 w-full">

        <!-- TAB 1: Acervo Mestre de Ferramentas -->
        <section id="catalogoSection">
            <div class="flex items-center justify-between text-xs text-slate-400 mb-4 px-1">
                <span id="resultsInfo" class="font-medium">Carregando acervo...</span>
                <div class="flex items-center space-x-2">
                    <span class="inline-block w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    <span class="text-slate-400">Sincronizado: PostgreSQL + Instagram + GitHub</span>
                </div>
            </div>

            <div id="toolsGrid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                <!-- Injetado dinamicamente via JS -->
            </div>

            <div id="loadMoreContainer" class="py-8 text-center hidden">
                <button onclick="loadMore()" class="bg-dark-900 hover:bg-dark-800 text-brand-400 border border-dark-750 px-6 py-2.5 rounded-xl text-xs font-bold transition shadow-lg">
                    Carregar Mais Ferramentas (+60)
                </button>
            </div>
        </section>

        <!-- TAB 2: GitHub Live Radar -->
        <section id="githubSection" class="hidden">
            <div class="bg-dark-900 border border-dark-800 rounded-2xl p-6 mb-6">
                <h2 class="text-lg font-bold text-white mb-1 flex items-center gap-2">
                    <span>🌐</span> OpenSource Hunter Live Radar
                </h2>
                <p class="text-xs text-slate-400 mb-4">Pesquise diretamente em tempo real em mais de 200 milhões de repositórios do GitHub.</p>
                <div class="flex gap-2">
                    <input type="text" id="githubQueryInput" placeholder="Ex: AI agent, MCP server, web scraper, computer vision, GIS..."
                        class="flex-1 bg-dark-950 border border-dark-750 text-white text-sm rounded-xl px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-brand-500">
                    <button onclick="searchLiveGithub()" class="bg-brand-600 hover:bg-brand-500 text-white text-xs font-bold px-5 py-2.5 rounded-xl transition shadow-md">
                        Buscar no GitHub
                    </button>
                </div>
            </div>

            <div id="githubResultsGrid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                <!-- Resultados da busca live do GitHub -->
            </div>
        </section>

        <!-- TAB 3: Obsidian Vault Exporter Hub -->
        <section id="obsidianSection" class="hidden">
            <div class="bg-dark-900 border border-dark-800 rounded-2xl p-6 mb-6">
                <h2 class="text-xl font-bold text-white mb-2 flex items-center gap-2">
                    <span>📓</span> Obsidian Vault Exporter
                </h2>
                <p class="text-sm text-slate-300 mb-4 leading-relaxed">
                    Exporte o acervo mestre de <strong>{len(merged_tools):,} ferramentas e repositórios</strong> estruturados com metadados, tags e links direto para o seu Obsidian Vault.
                </p>
                <div class="flex flex-wrap gap-3">
                    <a href="/catalogo_mobile.csv" download class="bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold py-2.5 px-5 rounded-xl transition flex items-center gap-2 shadow-lg shadow-emerald-600/20">
                        <span>📊</span> Baixar Planilha Mestre Completa (.CSV)
                    </a>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4" id="obsidianCategoriesList">
                <!-- Injetado dinamicamente -->
            </div>
        </section>

    </main>

    <!-- Modal de Exportação de Nota Obsidian -->
    <div id="obsidianModal" class="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm hidden items-center justify-center p-4">
        <div class="bg-dark-900 border border-dark-750 w-full max-w-2xl rounded-2xl p-6 shadow-2xl flex flex-col max-h-[85vh]">
            <div class="flex items-center justify-between pb-3 border-b border-dark-800">
                <div class="flex items-center space-x-2">
                    <span class="text-2xl">📓</span>
                    <div>
                        <h3 class="font-bold text-white text-base" id="modalToolName">Nome da Ferramenta</h3>
                        <p class="text-xs text-brand-400">Nota Técnica Formatada para Obsidian</p>
                    </div>
                </div>
                <button onclick="closeObsidianModal()" class="text-slate-400 hover:text-white text-lg p-1">✕</button>
            </div>
            
            <div class="my-4 flex-1 overflow-y-auto bg-dark-950 p-4 rounded-xl border border-dark-800">
                <pre class="text-xs font-mono text-slate-300 whitespace-pre-wrap" id="modalNoteContent"></pre>
            </div>

            <div class="flex justify-end space-x-3 pt-3 border-t border-dark-800">
                <button onclick="copyModalContent()" id="copyBtn" class="bg-dark-800 hover:bg-dark-750 text-slate-200 text-xs font-semibold py-2 px-4 rounded-xl transition border border-dark-700">
                    📋 Copiar Markdown
                </button>
                <button onclick="downloadModalNote()" class="bg-brand-600 hover:bg-brand-500 text-white text-xs font-bold py-2 px-4 rounded-xl transition">
                    💾 Baixar Arquivo .md
                </button>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer class="mt-16 border-t border-dark-800/80 py-8 px-4 text-center text-xs text-slate-500 bg-dark-950">
        <p class="font-medium text-slate-400">OpenSource Hunter & AI Hub • Rodrigo Borin</p>
        <p class="mt-1">Deploy automatizado via Vercel • Sincronizado com PostgreSQL Local & Obsidian</p>
    </footer>

    <!-- Scripts de Interatividade e Paginação de Alta Performance -->
    <script>
        const allTools = {tools_json_str};
        let currentTab = 'catalogo';
        let currentCategory = 'TODAS';
        let searchQuery = '';
        let currentSelectedTool = null;
        let visibleCount = 60;
        let filteredToolsCache = [];

        // Categorias e contagem
        const categoryCounts = {{}};
        allTools.forEach(t => {{
            categoryCounts[t.categoria] = (categoryCounts[t.categoria] || 0) + 1;
        }});

        // Montar Pills de Categoria
        const pillBar = document.getElementById('categoryPillBar');
        Object.keys(categoryCounts).sort().forEach(cat => {{
            const btn = document.createElement('button');
            btn.className = "cat-pill px-3.5 py-2 rounded-xl bg-dark-900 text-slate-300 border border-dark-750 whitespace-nowrap font-medium hover:bg-dark-800 transition";
            btn.innerHTML = `${{cat}} (${{categoryCounts[cat].toLocaleString()}})`;
            btn.onclick = () => filterCategory(cat);
            pillBar.appendChild(btn);
        }});

        function switchTab(tab) {{
            currentTab = tab;
            document.querySelectorAll('.tab-btn').forEach(btn => {{
                btn.className = "tab-btn px-3 py-1.5 rounded-lg text-slate-400 hover:text-white transition";
            }});
            
            document.getElementById('catalogoSection').classList.add('hidden');
            document.getElementById('githubSection').classList.add('hidden');
            document.getElementById('obsidianSection').classList.add('hidden');
            document.getElementById('categoryPillBar').classList.add('hidden');

            if (tab === 'catalogo') {{
                document.getElementById('tabBtnCatalogo').className = "tab-btn px-3 py-1.5 rounded-lg bg-brand-600 text-white shadow-sm transition";
                document.getElementById('catalogoSection').classList.remove('hidden');
                document.getElementById('categoryPillBar').classList.remove('hidden');
                document.getElementById('searchBarContainer').classList.remove('hidden');
                renderCatalogo();
            }} else if (tab === 'github') {{
                document.getElementById('tabBtnGithub').className = "tab-btn px-3 py-1.5 rounded-lg bg-brand-600 text-white shadow-sm transition";
                document.getElementById('githubSection').classList.remove('hidden');
                document.getElementById('searchBarContainer').classList.add('hidden');
                if (document.getElementById('githubResultsGrid').children.length === 0) {{
                    searchLiveGithub('AI agents open source');
                }}
            }} else if (tab === 'obsidian') {{
                document.getElementById('tabBtnObsidian').className = "tab-btn px-3 py-1.5 rounded-lg bg-brand-600 text-white shadow-sm transition";
                document.getElementById('obsidianSection').classList.remove('hidden');
                document.getElementById('searchBarContainer').classList.add('hidden');
                renderObsidianHub();
            }}
        }}

        function filterCategory(cat) {{
            currentCategory = cat;
            visibleCount = 60;
            document.querySelectorAll('.cat-pill').forEach(btn => {{
                if ((cat === 'TODAS' && btn.innerText.includes('Todas')) || btn.innerText.startsWith(cat)) {{
                    btn.className = "cat-pill active px-3.5 py-2 rounded-xl bg-brand-600 text-white whitespace-nowrap font-semibold transition shadow-sm";
                }} else {{
                    btn.className = "cat-pill px-3.5 py-2 rounded-xl bg-dark-900 text-slate-300 border border-dark-750 whitespace-nowrap font-medium hover:bg-dark-800 transition";
                }}
            }});
            renderCatalogo();
        }}

        function renderCatalogo() {{
            const grid = document.getElementById('toolsGrid');
            grid.innerHTML = '';

            const query = searchQuery.toLowerCase().trim();
            filteredToolsCache = allTools.filter(t => {{
                const matchCat = currentCategory === 'TODAS' || t.categoria === currentCategory;
                const matchSearch = query === '' || 
                    t.nome.toLowerCase().includes(query) || 
                    (t.caso_uso && t.caso_uso.toLowerCase().includes(query)) ||
                    (t.linguagem && t.linguagem.toLowerCase().includes(query));
                return matchCat && matchSearch;
            }});

            document.getElementById('resultsInfo').innerText = `Mostrando ${{Math.min(visibleCount, filteredToolsCache.length).toLocaleString()}} de ${{filteredToolsCache.length.toLocaleString()}} ferramentas encontradas`;

            const loadMoreBtn = document.getElementById('loadMoreContainer');
            if (filteredToolsCache.length > visibleCount) {{
                loadMoreBtn.classList.remove('hidden');
            }} else {{
                loadMoreBtn.classList.add('hidden');
            }}

            if (filteredToolsCache.length === 0) {{
                grid.innerHTML = `
                    <div class="col-span-full py-16 text-center text-slate-400">
                        <div class="text-4xl mb-2">🔍</div>
                        <p class="font-bold text-base text-white">Nenhum projeto encontrado</p>
                        <p class="text-xs text-slate-400 mt-1">Tente outros termos ou limpe o filtro de categoria.</p>
                    </div>
                `;
                return;
            }}

            const toShow = filteredToolsCache.slice(0, visibleCount);
            toShow.forEach(t => {{
                const card = document.createElement('div');
                card.className = "bg-dark-900 border border-dark-800 hover:border-brand-500/50 rounded-2xl p-5 flex flex-col justify-between transition-all duration-200 hover:-translate-y-1 hover:shadow-xl hover:shadow-indigo-500/5";

                const isVip = t.origem && t.origem.includes('Curadoria');
                const originBadge = isVip ? 
                    `<span class="bg-amber-500/10 text-amber-400 border border-amber-500/20 text-[10px] font-bold px-2 py-0.5 rounded-md">⭐ Curadoria Borin</span>` :
                    `<span class="bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 text-[10px] font-semibold px-2 py-0.5 rounded-md">🌐 ${{t.linguagem || 'GitHub'}}</span>`;

                const starsBadge = t.estrelas > 0 ? 
                    `<span class="text-[11px] font-bold text-amber-400 bg-amber-400/10 px-2 py-0.5 rounded-md border border-amber-400/20">⭐ ${{t.estrelas.toLocaleString()}}</span>` : '';

                const igBtn = t.link_ig ? `
                    <a href="${{t.link_ig}}" target="_blank" class="bg-pink-500/10 hover:bg-pink-500/20 text-pink-400 border border-pink-500/25 text-xs font-semibold py-2 px-3 rounded-xl transition flex items-center justify-center gap-1.5" title="Ver no Instagram">
                        <span>📱</span>
                        <span>Post</span>
                    </a>
                ` : '';

                const githubUrl = t.github_search || `https://github.com/${{t.nome}}`;

                card.innerHTML = `
                    <div>
                        <div class="flex items-start justify-between gap-2 mb-2.5">
                            <div class="flex items-center space-x-2 min-w-0">
                                <span class="text-xl flex-shrink-0">${{t.emoji || '🛠️'}}</span>
                                <h3 class="font-bold text-white text-sm sm:text-base truncate tracking-tight" title="${{t.nome}}">${{t.nome}}</h3>
                            </div>
                            <div class="flex items-center space-x-1.5 flex-shrink-0">
                                ${{starsBadge}}
                            </div>
                        </div>

                        <div class="flex items-center space-x-2 mb-3">
                            ${{originBadge}}
                            <span class="text-[10px] text-slate-400">${{t.categoria}}</span>
                        </div>

                        <p class="text-xs text-slate-300 leading-relaxed line-clamp-3 mb-4 font-normal">
                            ${{t.caso_uso || 'Sem descrição detalhada.'}}
                        </p>
                    </div>

                    <div class="grid grid-cols-2 gap-2 pt-3 border-t border-dark-800">
                        ${{igBtn ? igBtn : `
                            <a href="${{githubUrl}}" target="_blank" class="bg-dark-800 hover:bg-dark-750 text-slate-200 border border-dark-700 text-xs font-semibold py-2 px-3 rounded-xl transition flex items-center justify-center gap-1.5">
                                <span>🐙</span>
                                <span>GitHub</span>
                            </a>
                        `}}
                        <button onclick="openObsidianModal('${{encodeURIComponent(JSON.stringify(t))}}')" class="bg-brand-600/10 hover:bg-brand-600 text-brand-400 hover:text-white border border-brand-500/20 hover:border-transparent text-xs font-bold py-2 px-3 rounded-xl transition flex items-center justify-center gap-1.5">
                            <span>📓</span>
                            <span>Nota .md</span>
                        </button>
                    </div>
                `;
                grid.appendChild(card);
            }});
        }}

        function loadMore() {{
            visibleCount += 60;
            renderCatalogo();
        }}

        // Infinite Scroll Listener
        window.addEventListener('scroll', () => {{
            if (currentTab === 'catalogo' && (window.innerHeight + window.scrollY) >= document.body.offsetHeight - 500) {{
                if (visibleCount < filteredToolsCache.length) {{
                    visibleCount += 30;
                    renderCatalogo();
                }}
            }}
        }});

        // Input Search Listener com Debounce
        let searchDebounce;
        document.getElementById('mainSearchInput').addEventListener('input', (e) => {{
            clearTimeout(searchDebounce);
            searchDebounce = setTimeout(() => {{
                searchQuery = e.target.value;
                visibleCount = 60;
                document.getElementById('clearSearchBtn').classList.toggle('hidden', !searchQuery);
                renderCatalogo();
            }}, 150);
        }});

        function clearSearch() {{
            document.getElementById('mainSearchInput').value = '';
            searchQuery = '';
            visibleCount = 60;
            document.getElementById('clearSearchBtn').classList.add('hidden');
            renderCatalogo();
        }}

        function openObsidianModal(encodedJson) {{
            const t = JSON.parse(decodeURIComponent(encodedJson));
            currentSelectedTool = t;
            document.getElementById('modalToolName').innerText = t.nome;
            
            const noteMd = `---
title: "${{t.nome}}"
tags:
  - opensource
  - ${{t.categoria.toLowerCase().replace(/[^a-z0-9]/g, '-')}}
categoria: "${{t.categoria}}"
linguagem: "${{t.linguagem || 'N/A'}}"
estrelas: ${{t.estrelas || 0}}
data_registro: "${{new Date().toISOString().split('T')[0]}}"
---

# ${{t.emoji || '🛠️'}} ${{t.nome}}

> **Caso de Uso Principal:** ${{t.caso_uso || 'N/A'}}

## 📌 Metadados
- **Origem:** ${{t.origem || 'OpenSource Hunter'}}
- **Categoria:** ${{t.categoria}}
- **Linguagem Principal:** ${{t.linguagem || 'N/A'}}
- **Estrelas GitHub:** ⭐ ${{t.estrelas || 0}}

## 🔗 Links Oficiais
- **Repositório / Link:** [Acessar Link Oficial](${{t.github_search || 'https://github.com/' + t.nome}})
${{t.link_ig ? '- **Post de Referência no Instagram:** [Ver Post](' + t.link_ig + ')' : ''}}

---
*Gerado automaticamente pelo OpenSource Hunter (Rodrigo Borin).*
`;
            document.getElementById('modalNoteContent').innerText = noteMd;
            document.getElementById('obsidianModal').classList.remove('hidden');
            document.getElementById('obsidianModal').classList.add('flex');
        }}

        function closeObsidianModal() {{
            document.getElementById('obsidianModal').classList.add('hidden');
            document.getElementById('obsidianModal').classList.remove('flex');
        }}

        function copyModalContent() {{
            const text = document.getElementById('modalNoteContent').innerText;
            navigator.clipboard.writeText(text).then(() => {{
                const btn = document.getElementById('copyBtn');
                btn.innerText = '✅ Copiado!';
                setTimeout(() => btn.innerText = '📋 Copiar Markdown', 2000);
            }});
        }}

        function downloadModalNote() {{
            if (!currentSelectedTool) return;
            const text = document.getElementById('modalNoteContent').innerText;
            const filename = `${{currentSelectedTool.nome.replace(/[^a-zA-Z0-9_-]/g, '_')}}.md`;
            const blob = new Blob([text], {{ type: 'text/markdown;charset=utf-8' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            a.click();
            URL.revokeObjectURL(url);
        }}

        // Inicialização
        renderCatalogo();
    </script>
</body>
</html>
"""

with open(os.path.join(WEB_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(html_code)

html_size_mb = os.path.getsize(os.path.join(WEB_DIR, "index.html")) / (1024 * 1024)
print(f"[4/4] index.html gerado com sucesso! Tamanho final: {html_size_mb:.2f} MB")
