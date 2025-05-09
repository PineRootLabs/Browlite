[![Licença MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/PineRootLabs/Browlite/blob/main/LICENSE)
[![Versão Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![GitHub stars](https://img.shields.io/github/stars/PineRootLabs/Browlite.svg)](https://github.com/PineRootLabs/Browlite/stargazers)

# 🌐 Browlite - Navegador Minimalista de Alto Desempenho

**Browlite** é um navegador web minimalista desenvolvido em Python, focado em privacidade, desempenho e customização. Projetado para ser leve e rápido, consome menos recursos que navegadores tradicionais.

🔗 **Repositório Oficial**: [https://github.com/PineRootLabs/Browlite](https://github.com/PineRootLabs/Browlite)

📦 **Download Via pip (PyPI)**: [https://pypi.org/project/browlite/]

## ✨ Recursos Principais

- ✅ **Extremamente leve** (usa ~50% menos RAM que navegadores convencionais)
- ✅ **Bloqueio de anúncios e trackers** nativo
- ✅ **Multiplos mecanismos de busca** (Google, DuckDuckGo, Bing, etc.)
- ✅ **Modo escuro/light** configurável
- ✅ **Sistema de favoritos** com acesso via terminal
- ✅ **Interface minimalista** sem barras desnecessárias
- ✅ **Configuração flexível** via arquivos INI

## 🛠️ Instalação

### Pré-requisitos
- Python 3.7 ou superior
- Pip (gerenciador de pacotes Python)

### Passo a Passo
```bash
# Clone o repositório
git clone https://github.com/PineRootLabs/Browlite.git
cd Browlite

# Instale as dependências
pip install PyQt5 PyQtWebEngine

# Execute o navegador
browlite

🎛️ Configuração Inicial
Na primeira execução, o Browlite irá:

Perguntar qual modo de operação deseja usar:

🛡️ Minimalista Seguro (equilíbrio entre recursos e desempenho)

⚡ Extremamente Leve (máximo desempenho, menos recursos)

Solicitar a escolha do mecanismo de busca padrão

Os arquivos de configuração serão gerados automaticamente na pasta do projeto.

📂 Estrutura de Arquivos

Browlite/
├── main.py                 # Código principal
├── config.ini              # Configurações do usuário (gerado automaticamente)
├── config_minimal.ini      # Perfil Minimalista Seguro
├── config_light.ini        # Perfil Extremamente Leve
├── favs.txt                # Lista de favoritos (gerado automaticamente)
└── icons/                  # Ícones dos mecanismos de busca
    ├── google.png
    ├── duckduckgo.png
    ├── bing.png
    ├── yahoo.png
    ├── ecosia.png
    ├── back.png
    ├── forward.png
    ├── refresh.png
    └── home.png

# 🕹️ Como Usar

## 🚀 Comandos Básicos

| Comando                 | Descrição                          |
|-------------------------|------------------------------------|
| browlite                | Inicia o navegador normalmente     |
| browlite [URL]          | Abre uma URL específica            |
________________________________________________________________


⚙️ Personalização Avançada

Edite os arquivos .ini para ajustes personalizado:

Configurações Principais (config.ini)

[DEFAULT]
homepage = https://www.google.com ; Página inicial
dark_mode = true                  ; Tema escuro
block_ads = true                  ; Bloqueio de anúncios
default_search_engine = google    ; Mecanismo de busca padrão
Mecanismos de Busca Suportados
Google (google)

DuckDuckGo (duckduckgo)

Bing (bing)

Yahoo (yahoo)

Ecosia (ecosia)

Para adicionar novos buscadores, edite o dicionário SEARCH_ENGINES no código.

🤝 Agradecimentos Especiais
Este projeto contou com o suporte técnico e consultoria especializada do DeepSeek Chat durante o processo de desenvolvimento. Sua contribuição foi fundamental para:

Otimização de desempenho

Documentação técnica

"A inteligência artificial não substitui a criatividade humana, mas pode amplificá-la exponencialmente." - PineRootLabs

✉️ Contato
Desenvolvido por Caio R. - [Suporte+pinerootlabs@gmail.com]

🔗 Repositório: https://github.com/PineRootLabs/Browlite
