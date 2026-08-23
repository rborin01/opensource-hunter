import json
import os

tools_path = "tools.json" if os.path.exists("tools.json") else r"G:\Meu Drive\Suno\AERON GENESIS\catalogo_opensource_limpo.json"
with open(tools_path, "r", encoding="utf-8") as f:
    tools = json.load(f)

def categorizar(nome, caso_uso):
    texto = (nome + " " + caso_uso).lower()
    if any(k in texto for k in ["mcp", "code", "coding", "turborepo", "strix", "cli", "terminal", "ide", "programação", "pentest", "desenvolvedor"]):
        return "Dev, Coding & MCP", "💻"
    elif any(k in texto for k in ["agent", "agente", "multi-agent", "mirofish", "miroshark", "deerflow", "eigent", "openworker", "conway", "langchain", "langsmith", "orquestração"]):
        return "Multi-Agentes & Frameworks", "🤖"
    elif any(k in texto for k in ["tts", "audio", "áudio", "voz", "voxtral", "elevenlabs", "pocket tts", "kyutai", "deepgram", "livekit", "fala", "speech", "asr"]):
        return "Voz, Áudio & TTS", "🎙️"
    elif any(k in texto for k in ["video", "vídeo", "3d", "sam 3d", "vision", "imagem", "veo", "imagine", "luma", "openart", "pika", "lingbot", "avatar", "render"]):
        return "Vídeo, Visão & 3D", "👁️"
    elif any(k in texto for k in ["crawlee", "scrape", "scraping", "n8n", "zapier", "pipefy", "workflow", "automação", "apify", "crawler", "bot", "fluxo"]):
        return "Automação & Scraping", "⚡"
    elif any(k in texto for k in ["ads", "marketing", "meta ads", "vendas", "funil", "tráfego", "lead", "negócio", "imobiliário", "receita", "sms"]):
        return "Marketing, Ads & Funis", "📈"
    elif any(k in texto for k in ["llm", "claude", "gemini", "kimi", "qwen", "glm", "openrouter", "airllm", "perplexity", "deepseek", "mistral", "anthropic", "gpt", "model"]):
        return "Modelos LLM & Infra", "🧠"
    else:
        return "Geral & Produtividade", "🛠️"

for t in tools:
    cat, emoji = categorizar(t["nome"], t["caso_uso"])
    t["categoria"] = cat
    t["emoji"] = emoji

tools_json_str = json.dumps(tools, ensure_ascii=False)

html_code = f"""<!DOCTYPE html>
<html lang="pt-BR" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenSource Hunter | Rodrigo Borin</title>
    <meta name="description" content="Catálogo Mestre e Motor de Busca de Ferramentas Open Source, Inteligência Artificial e Repositórios GitHub por Rodrigo Borin.">
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
                        <span class="text-[10px] uppercase font-bold tracking-widest bg-brand-500/20 text-brand-400 border border-brand-500/30 px-2 py-0.5 rounded-full">v2.0 Live</span>
                    </div>
                    <p class="text-xs text-slate-400 font-medium">rodrigoborin.com • <span class="text-emerald-400 font-semibold" id="totalHeaderCount">{len(tools)} Ferramentas</span></p>
                </div>
            </div>

            <!-- View Modes (Tabs) -->
            <div class="flex items-center bg-dark-900 border border-dark-750 p-1 rounded-xl text-xs font-semibold">
                <button onclick="switchTab('catalogo')" id="tabBtnCatalogo" class="tab-btn px-3 py-1.5 rounded-lg bg-brand-600 text-white shadow-sm transition">
                    🧭 Catálogo Curado
                </button>
                <button onclick="switchTab('github')" id="tabBtnGithub" class="tab-btn px-3 py-1.5 rounded-lg text-slate-400 hover:text-white transition">
                    🌐 GitHub Radar
                </button>
                <button onclick="switchTab('obsidian')" id="tabBtnObsidian" class="tab-btn px-3 py-1.5 rounded-lg text-slate-400 hover:text-white transition">
                    📓 Obsidian Vault
                </button>
            </div>
        </div>

        <!-- Search Bar (Aparece no Catálogo e GitHub) -->
        <div class="max-w-7xl mx-auto mt-3" id="searchBarContainer">
            <div class="relative flex items-center">
                <input type="text" id="mainSearchInput" placeholder="Buscar ferramenta, framework, LLM, MCP, caso de uso..." 
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

        <!-- Category Pills (Apenas no Catálogo Curado) -->
        <div class="max-w-7xl mx-auto mt-3 flex space-x-2 overflow-x-auto no-scrollbar pb-1 text-xs" id="categoryPillBar">
            <button onclick="filterCategory('TODAS')" class="cat-pill active px-3.5 py-2 rounded-xl bg-brand-600 text-white whitespace-nowrap font-semibold transition shadow-sm">
                Todas ({len(tools)})
            </button>
        </div>
    </header>

    <!-- Main Content Container -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 mt-6 flex-1 w-full">

        <!-- TAB 1: Catálogo Curado de 536 Ferramentas -->
        <section id="catalogoSection">
            <div class="flex items-center justify-between text-xs text-slate-400 mb-4 px-1">
                <span id="resultsInfo" class="font-medium">Mostrando {len(tools)} ferramentas filtradas</span>
                <div class="flex items-center space-x-2">
                    <span class="inline-block w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    <span class="text-slate-400">Sincronizado com Instagram & Google Drive</span>
                </div>
            </div>

            <div id="toolsGrid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                <!-- Injetado dinamicamente via JS -->
            </div>
        </section>

        <!-- TAB 2: GitHub Live Radar (Busca em Tempo Real na API do GitHub) -->
        <section id="githubSection" class="hidden">
            <div class="bg-dark-900 border border-dark-800 rounded-2xl p-6 mb-6">
                <h2 class="text-lg font-bold text-white mb-1 flex items-center gap-2">
                    <span>🌐</span> OpenSource Hunter Live Radar
                </h2>
                <p class="text-xs text-slate-400 mb-4">Pesquise diretamente em tempo real em mais de 100 milhões de repositórios do GitHub.</p>
                <div class="flex gap-2">
                    <input type="text" id="githubQueryInput" placeholder="Ex: AI agent, MCP server, web scraper, computer vision..."
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
                    Exporte todas as <strong>{len(tools)} notas estruturadas</strong> com arquitetura, tags e links bidirecionais direto para o seu Obsidian Vault no Desktop ou Celular.
                </p>
                <div class="flex flex-wrap gap-3">
                    <button onclick="downloadAllObsidianZip()" class="bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold py-2.5 px-4 rounded-xl transition flex items-center gap-2 shadow-lg shadow-emerald-600/20">
                        <span>📥</span> Baixar Pacote Completo do Vault (.MD)
                    </button>
                    <a href="/catalogo_mobile.csv" download class="bg-dark-800 hover:bg-dark-750 text-slate-200 border border-dark-700 text-xs font-semibold py-2.5 px-4 rounded-xl transition flex items-center gap-2">
                        <span>📊</span> Baixar Planilha CSV
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
        <p class="mt-1">Deploy automatizado via Vercel • Sincronizado com Google Drive & Obsidian</p>
    </footer>

    <!-- Scripts de Interatividade -->
    <script>
        const allTools = {tools_json_str};
        let currentTab = 'catalogo';
        let currentCategory = 'TODAS';
        let searchQuery = '';
        let currentSelectedTool = null;

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
            btn.innerHTML = `${{cat}} (${{categoryCounts[cat]}})`;
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

            const filtered = allTools.filter(t => {{
                const matchCat = currentCategory === 'TODAS' || t.categoria === currentCategory;
                const query = searchQuery.toLowerCase();
                const matchSearch = query === '' || 
                    t.nome.toLowerCase().includes(query) || 
                    t.caso_uso.toLowerCase().includes(query) ||
                    t.categoria.toLowerCase().includes(query);
                return matchCat && matchSearch;
            }});

            document.getElementById('resultsInfo').innerText = `Mostrando ${{filtered.length}} de ${{allTools.length}} ferramentas`;

            if (filtered.length === 0) {{
                grid.innerHTML = `
                    <div class="col-span-full py-16 text-center text-slate-400">
                        <div class="text-4xl mb-2">🔍</div>
                        <p class="font-bold text-base text-white">Nenhum projeto encontrado</p>
                        <p class="text-xs text-slate-400 mt-1">Tente outros termos ou limpe o filtro de categoria.</p>
                    </div>
                `;
                return;
            }}

            filtered.forEach(t => {{
                const card = document.createElement('div');
                card.className = "bg-dark-900 border border-dark-800 hover:border-brand-500/50 rounded-2xl p-5 flex flex-col justify-between transition-all duration-200 hover:-translate-y-1 hover:shadow-xl hover:shadow-indigo-500/5";

                const igBtn = t.link_ig ? `
                    <a href="${{t.link_ig}}" target="_blank" class="bg-pink-500/10 hover:bg-pink-500/20 text-pink-400 border border-pink-500/25 text-xs font-semibold py-2 px-3 rounded-xl transition flex items-center justify-center gap-1.5" title="Ver post original">
                        <span>📱</span>
                        <span>Post</span>
                    </a>
                ` : '';

                card.innerHTML = `
                    <div>
                        <div class="flex items-start justify-between gap-2 mb-2.5">
                            <div class="flex items-center space-x-2">
                                <span class="text-xl">${{t.emoji || '🤖'}}</span>
                                <h3 class="font-bold text-white text-base leading-snug">${{t.nome}}</h3>
                            </div>
                            <span class="text-[10px] px-2.5 py-1 rounded-full bg-dark-800 text-slate-400 border border-dark-700 shrink-0 font-semibold">${{t.categoria}}</span>
                        </div>
                        <p class="text-xs text-slate-300 leading-relaxed mb-4 line-clamp-3">${{t.caso_uso}}</p>
                    </div>

                    <div class="space-y-2 pt-3 border-t border-dark-800">
                        <div class="flex items-center gap-2">
                            <a href="${{t.github_search}}" target="_blank" class="flex-1 bg-brand-600 hover:bg-brand-500 text-white text-xs font-bold py-2 px-3 rounded-xl transition flex items-center justify-center gap-1.5 shadow-md shadow-indigo-600/20">
                                <span>🔍</span>
                                <span>Buscar Repo</span>
                            </a>
                            ${{igBtn}}
                        </div>
                        <button onclick='openObsidianModal(${{JSON.stringify(t)}})' class="w-full bg-dark-800 hover:bg-dark-750 text-slate-300 border border-dark-700/80 hover:text-white text-xs font-medium py-1.5 px-3 rounded-xl transition flex items-center justify-center gap-1.5">
                            <span>📓</span>
                            <span>Gerar Nota Obsidian</span>
                        </button>
                    </div>
                `;
                grid.appendChild(card);
            }});
        }}

        // Busca Live no GitHub
        async function searchLiveGithub(customQuery) {{
            const query = customQuery || document.getElementById('githubQueryInput').value.trim();
            if (!query) return;

            const grid = document.getElementById('githubResultsGrid');
            grid.innerHTML = `
                <div class="col-span-full py-12 text-center text-slate-400">
                    <div class="inline-block w-8 h-8 border-4 border-brand-500 border-t-transparent rounded-full animate-spin mb-3"></div>
                    <p class="text-sm font-medium">Buscando repositórios em tempo real no GitHub...</p>
                </div>
            `;

            try {{
                const res = await fetch(`https://api.github.com/search/repositories?q=${{encodeURIComponent(query)}}&sort=stars&order=desc&per_page=12`);
                const data = await res.json();

                grid.innerHTML = '';
                if (!data.items || data.items.length === 0) {{
                    grid.innerHTML = `<div class="col-span-full py-12 text-center text-slate-400"><p>Nenhum repositório encontrado para "${{query}}".</p></div>`;
                    return;
                }}

                data.items.forEach(repo => {{
                    const card = document.createElement('div');
                    card.className = "bg-dark-900 border border-dark-800 hover:border-brand-500/50 rounded-2xl p-5 flex flex-col justify-between transition-all duration-200 hover:-translate-y-1 hover:shadow-xl";
                    card.innerHTML = `
                        <div>
                            <div class="flex items-start justify-between gap-2 mb-2">
                                <h3 class="font-bold text-white text-base leading-snug break-all">${{repo.full_name}}</h3>
                                <span class="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 font-semibold shrink-0">★ ${{repo.stargazers_count.toLocaleString()}}</span>
                            </div>
                            <p class="text-xs text-slate-300 leading-relaxed mb-4 line-clamp-3">${{repo.description || 'Sem descrição fornecida.'}}</p>
                        </div>
                        <div class="pt-3 border-t border-dark-800 flex items-center justify-between text-xs">
                            <span class="text-slate-400 font-mono">${{repo.language || 'Code'}}</span>
                            <a href="${{repo.html_url}}" target="_blank" class="bg-brand-600 hover:bg-brand-500 text-white font-bold py-1.5 px-3 rounded-xl transition">
                                Abrir GitHub ↗
                            </a>
                        </div>
                    `;
                    grid.appendChild(card);
                }});
            }} catch (err) {{
                grid.innerHTML = `<div class="col-span-full py-12 text-center text-rose-400"><p>Erro ao conectar à API do GitHub: ${{err.message}}</p></div>`;
            }}
        }}

        function renderObsidianHub() {{
            const list = document.getElementById('obsidianCategoriesList');
            list.innerHTML = '';

            Object.keys(categoryCounts).sort().forEach(cat => {{
                const card = document.createElement('div');
                card.className = "bg-dark-900 border border-dark-800 rounded-2xl p-5 flex items-center justify-between";
                card.innerHTML = `
                    <div>
                        <h4 class="font-bold text-white text-sm">${{cat}}</h4>
                        <p class="text-xs text-slate-400 mt-0.5">${{categoryCounts[cat]}} notas estruturadas</p>
                    </div>
                    <button onclick="filterCategory('${{cat}}'); switchTab('catalogo');" class="text-xs bg-dark-800 hover:bg-dark-750 text-brand-400 border border-dark-700 px-3 py-1.5 rounded-xl font-semibold transition">
                        Ver Ferramentas →
                    </button>
                `;
                list.appendChild(card);
            }});
        }}

        // Modal Obsidian Logic
        function openObsidianModal(tool) {{
            currentSelectedTool = tool;
            document.getElementById('modalToolName').innerText = tool.nome;
            
            const noteMarkdown = `---
title: "${{tool.nome}}"
category: "${{tool.categoria}}"
source: "${{tool.origem}}"
instagram_url: "${{tool.link_ig || ''}}"
github_search: "${{tool.github_search}}"
date_added: "${{new Date().toISOString().split('T')[0]}}"
tags:
  - ai
  - opensource
  - ${{tool.categoria.toLowerCase().replace(/[^a-z0-9]/g, '_')}}
---

# 🚀 ${{tool.nome}}

> **Categoria:** \`${{tool.categoria}}\`  
> **Origem:** \`${{tool.origem}}\`

## 💡 Caso de Uso & Aplicação
${{tool.caso_uso}}

## 🔗 Links & Referências
- **Repositório GitHub:** [Buscar Repositório Oficial](${{tool.github_search}})
- **Post Original no Instagram:** [Abrir Post](${{tool.link_ig || '#'}})

---
*Gerado automaticamente pelo OpenSource Hunter (rodrigoborin.com)*
`;

            document.getElementById('modalNoteContent').innerText = noteMarkdown;
            document.getElementById('obsidianModal').classList.remove('hidden');
            document.getElementById('obsidianModal').classList.add('flex');
        }}

        function closeObsidianModal() {{
            document.getElementById('obsidianModal').classList.add('hidden');
            document.getElementById('obsidianModal').classList.remove('flex');
        }}

        function copyModalContent() {{
            const content = document.getElementById('modalNoteContent').innerText;
            navigator.clipboard.writeText(content);
            const btn = document.getElementById('copyBtn');
            btn.innerText = "✓ Copiado!";
            setTimeout(() => {{ btn.innerText = "📋 Copiar Markdown"; }}, 2000);
        }}

        function downloadModalNote() {{
            if (!currentSelectedTool) return;
            const content = document.getElementById('modalNoteContent').innerText;
            const blob = new Blob([content], {{ type: 'text/markdown' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${{currentSelectedTool.nome.replace(/[^a-zA-Z0-9]/g, '_')}}.md`;
            a.click();
        }}

        function clearSearch() {{
            document.getElementById('mainSearchInput').value = '';
            searchQuery = '';
            document.getElementById('clearSearchBtn').classList.add('hidden');
            renderCatalogo();
        }}

        document.getElementById('mainSearchInput').addEventListener('input', (e) => {{
            searchQuery = e.target.value.trim();
            if (searchQuery) {{
                document.getElementById('clearSearchBtn').classList.remove('hidden');
            }} else {{
                document.getElementById('clearSearchBtn').classList.add('hidden');
            }}
            renderCatalogo();
        }});

        // Inicializar
        renderCatalogo();
    </script>
</body>
</html>
"""

output_path = r"C:\temp\opensourcehunter-web\index.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_code)

print(f"index.html criado com sucesso em: {output_path}")
