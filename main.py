import sys
import os
import shutil
import configparser
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QVBoxLayout, QWidget,
    QToolBar, QAction, QMenuBar, QInputDialog, QMessageBox
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtCore import QUrl, QSize
from PyQt5.QtGui import QIcon

# Dicionário de buscadores
SEARCH_ENGINES = {
    'google': {
        'name': 'Google',
        'url': 'https://www.google.com/search?q={}',
        'icon': 'icons/google.png'
    },
    'duckduckgo': {
        'name': 'DuckDuckGo',
        'url': 'https://duckduckgo.com/?q={}',
        'icon': 'icons/duckduckgo.png'
    },
    'bing': {
        'name': 'Bing',
        'url': 'https://www.bing.com/search?q={}',
        'icon': 'icons/bing.png'
    },
    'yahoo': {
        'name': 'Yahoo',
        'url': 'https://search.yahoo.com/search?p={}',
        'icon': 'icons/yahoo.png'
    },
    'ecosia': {
        'name': 'Ecosia',
        'url': 'https://www.ecosia.org/search?q={}',
        'icon': 'icons/ecosia.png'
    }
}

class Browlite(QMainWindow):
    def __init__(self, start_url=None):
        super().__init__()
        self.setWindowTitle("Browlite")
        self.setMinimumSize(800, 600)

        # Configurações
        self.config_file = "config.ini"
        self.favs_file = "favs.txt"
        self.load_config()
        self.load_favorites()
        self.load_search_engine()

        # Widgets
        self.browser = QWebEngineView()
        self.urlbar = QLineEdit()
        self.setup_browser_settings()

        # Interface
        self.setup_toolbar()
        self.setup_menu()

        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Eventos
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        self.browser.urlChanged.connect(self.update_urlbar)

        # Navegação inicial
        initial_url = QUrl(start_url) if start_url else QUrl(self.homepage)
        self.browser.setUrl(initial_url)

        # Aplica configurações de tema
        if self.dark_mode:
            self.apply_dark_mode()

    def load_config(self):
        """Carrega as configurações do arquivo .ini"""
        self.config = configparser.ConfigParser()
        
        if not os.path.exists(self.config_file):
            self.setup_config_choice()

        self.config.read(self.config_file)
        self.homepage = self.config['DEFAULT'].get('homepage', 'https://www.google.com')
        self.dark_mode = self.config['DEFAULT'].getboolean('dark_mode', True)
        self.block_ads = self.config['DEFAULT'].getboolean('block_ads', True)
        self.disable_images = self.config['DEFAULT'].getboolean('disable_images', False)

    def load_search_engine(self):
        """Carrega o buscador padrão"""
        self.default_search = self.config['DEFAULT'].get('default_search_engine', 'google')
        self.available_engines = [
            e.strip() for e in 
            self.config['DEFAULT'].get('available_search_engines', 'google,duckduckgo').split(',')
        ]

    def setup_config_choice(self):
        """Pergunta ao usuário qual configuração usar"""
        print("\n🔧 Selecione o modo de operação:")
        print("1. Minimalista Seguro (Recomendado)")
        print("2. Extremamente Leve (Máximo desempenho)")
        
        choice = input("Escolha (1/2): ").strip()
        
        if choice == "2":
            shutil.copyfile('config_light.ini', 'config.ini')
            print("✅ Modo Extremamente Leve ativado!")
        else:
            shutil.copyfile('config_minimal.ini', 'config.ini')
            print("✅ Modo Minimalista Seguro ativado!")

        # Pergunta sobre o buscador
        self.ask_search_engine()

    def ask_search_engine(self):
        """Pergunta ao usuário qual buscador usar"""
        print("\n🔍 Escolha seu buscador padrão:")
        engines = list(SEARCH_ENGINES.keys())
        for i, engine in enumerate(engines, 1):
            print(f"{i}. {SEARCH_ENGINES[engine]['name']}")
        
        choice = input("Digite o número do buscador: ").strip()
        if choice.isdigit() and 0 < int(choice) <= len(engines):
            self.config = configparser.ConfigParser()
            self.config.read('config.ini')
            self.config['DEFAULT']['default_search_engine'] = engines[int(choice)-1]
            with open('config.ini', 'w') as f:
                self.config.write(f)

    def setup_browser_settings(self):
        """Configurações de privacidade e desempenho"""
        settings = self.browser.settings()
        
        if self.block_ads:
            # Configurações para bloquear anúncios
            settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        
        if self.disable_images:
            settings.setAttribute(QWebEngineSettings.AutoLoadImages, False)

    def setup_toolbar(self):
        """Barra de ferramentas minimalista"""
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(toolbar)

        # Botões de navegação
        back_btn = QAction(QIcon.fromTheme("go-previous"), "Voltar", self)
        back_btn.triggered.connect(self.browser.back)
        
        forward_btn = QAction(QIcon.fromTheme("go-next"), "Avançar", self)
        forward_btn.triggered.connect(self.browser.forward)
        
        # Botão de busca
        search_btn = QAction(QIcon(SEARCH_ENGINES[self.default_search]['icon']), "Buscar", self)
        search_btn.triggered.connect(self.perform_search)
        
        # Barra de URL
        self.urlbar.setPlaceholderText("Digite uma URL ou termo de busca...")
        
        # Botão de fechar
        close_btn = QAction(QIcon.fromTheme("window-close"), "Fechar", self)
        close_btn.triggered.connect(self.close)

        # Adiciona à toolbar
        toolbar.addAction(back_btn)
        toolbar.addAction(forward_btn)
        toolbar.addAction(search_btn)
        toolbar.addWidget(self.urlbar)
        toolbar.addAction(close_btn)

    def setup_menu(self):
        """Configura a barra de menus"""
        menubar = self.menuBar()
        
        # Menu Navegação
        nav_menu = menubar.addMenu("Navegação")
        nav_menu.addAction("Voltar", self.browser.back, "Alt+Left")
        nav_menu.addAction("Avançar", self.browser.forward, "Alt+Right")
        nav_menu.addAction("Recarregar", self.browser.reload, "F5")
        nav_menu.addAction("Home", self.navigate_home, "Alt+Home")
        nav_menu.addSeparator()
        nav_menu.addAction("Adicionar aos Favoritos", self.add_to_favorites, "Ctrl+D")
        
        # Menu Configuração
        config_menu = menubar.addMenu("Configuração")
        config_menu.addAction("Alterar Buscador", self.change_search_engine)
        config_menu.addAction("Modo Escuro", self.toggle_dark_mode, checkable=True).setChecked(self.dark_mode)
        config_menu.addAction("Alterar Homepage", self.change_homepage)

    def navigate_to_url(self):
        """Navega para URL ou faz busca"""
        url = self.urlbar.text().strip()
        
        if url == "-favs":
            self.show_favorites()
        elif url.startswith(('http://', 'https://')):
            self.browser.setUrl(QUrl(url))
        else:
            self.perform_search()

    def perform_search(self):
        """Executa busca usando o mecanismo padrão"""
        query = self.urlbar.text()
        if query:
            search_url = SEARCH_ENGINES[self.default_search]['url'].format(query)
            self.browser.setUrl(QUrl(search_url))

    def change_search_engine(self):
        """Altera o buscador padrão"""
        engines = [
            (e, SEARCH_ENGINES[e]['name']) 
            for e in self.available_engines
            if e in SEARCH_ENGINES
        ]
        
        engine, ok = QInputDialog.getItem(
            self, "Escolha seu buscador",
            "Selecione o buscador padrão:",
            [e[1] for e in engines],
            0, False
        )
        
        if ok and engine:
            for key, name in engines:
                if name == engine:
                    self.default_search = key
                    self.config['DEFAULT']['default_search_engine'] = key
                    self.save_config()
                    # Atualiza a interface
                    self.setup_toolbar()
                    break

    def update_urlbar(self, q):
        """Atualiza a barra de URL"""
        self.urlbar.setText(q.toString())

    def add_to_favorites(self):
        """Adiciona URL atual aos favoritos"""
        current_url = self.browser.url().toString()
        
        if current_url in self.favorites:
            QMessageBox.information(self, "Favorito", "⭐ URL já está nos favoritos!")
            return
        
        self.favorites.append(current_url)
        self.save_favorites()
        QMessageBox.information(self, "Favorito", "✅ URL adicionada aos favoritos!")

    def show_favorites(self):
        """Mostra favoritos no terminal"""
        if not self.favorites:
            print("🌟 Nenhum favorito salvo.")
            return
        
        print("\n⭐ Favoritos:")
        for i, fav in enumerate(self.favorites, 1):
            print(f"{i}. {fav}")
        
        choice = input("\n🔢 Escolha um número (ou Enter para cancelar): ")
        if choice.isdigit() and 0 < int(choice) <= len(self.favorites):
            self.browser.setUrl(QUrl(self.favorites[int(choice)-1]))

    def load_favorites(self):
        """Carrega favoritos do arquivo"""
        if not os.path.exists(self.favs_file):
            return []
        
        with open(self.favs_file, "r") as f:
            return [line.strip() for line in f if line.strip()]

    def save_favorites(self):
        """Salva favoritos no arquivo"""
        with open(self.favs_file, "w") as f:
            f.write("\n".join(self.favorites))

    def toggle_dark_mode(self, state):
        """Ativa/desativa o modo escuro"""
        self.dark_mode = state
        self.config['DEFAULT']['dark_mode'] = 'true' if state else 'false'
        self.save_config()
        
        if state:
            self.apply_dark_mode()
        else:
            self.setStyleSheet("")

    def apply_dark_mode(self):
        """Aplica o tema escuro"""
        self.setStyleSheet("""
            QMainWindow, QToolBar, QMenuBar {
                background-color: #222;
                color: #eee;
            }
            QLineEdit {
                background-color: #333;
                color: #fff;
                border: 1px solid #555;
                padding: 5px;
            }
            QMenu {
                background-color: #333;
                color: #fff;
            }
            QMenu::item:selected {
                background-color: #555;
            }
        """)

    def change_homepage(self):
        """Altera a homepage padrão"""
        new_homepage, ok = QInputDialog.getText(
            self, "Alterar Homepage",
            "Digite a nova URL para homepage:",
            QLineEdit.Normal, self.homepage
        )
        
        if ok and new_homepage:
            if not new_homepage.startswith(("http://", "https://")):
                new_homepage = "https://" + new_homepage
            
            self.homepage = new_homepage
            self.config['DEFAULT']['homepage'] = new_homepage
            self.save_config()
            QMessageBox.information(self, "Sucesso", "✅ Homepage atualizada!")

    def save_config(self):
        """Salva as configurações no arquivo"""
        with open(self.config_file, 'w') as f:
            self.config.write(f)

    def closeEvent(self, event):
        """Salva tudo ao fechar"""
        self.save_config()
        self.save_favorites()
        event.accept()

def main():
    # Verifica e cria arquivos padrão se não existirem
    if not os.path.exists("config_minimal.ini"):
        with open("config_minimal.ini", "w") as f:
            f.write("""[DEFAULT]
homepage = https://www.google.com
dark_mode = true
block_ads = true
disable_images = false
default_search_engine = google
available_search_engines = google,duckduckgo,bing,yahoo,ecosia""")

    if not os.path.exists("config_light.ini"):
        with open("config_light.ini", "w") as f:
            f.write("""[DEFAULT]
homepage = about:blank
dark_mode = true
block_ads = true
disable_images = true
default_search_engine = duckduckgo
available_search_engines = google,duckduckgo,bing""")

    # Verifica argumentos
    app = QApplication(sys.argv)
    start_url = None
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "-favs":
            if os.path.exists("favs.txt"):
                with open("favs.txt", "r") as f:
                    favorites = [line.strip() for line in f if line.strip()]
                
                if favorites:
                    print("\n⭐ Favoritos:")
                    for i, fav in enumerate(favorites, 1):
                        print(f"{i}. {fav}")
                    
                    choice = input("\n🔢 Escolha um número (ou Enter para sair): ")
                    if choice.isdigit() and 0 < int(choice) <= len(favorites):
                        start_url = favorites[int(choice)-1]
            else:
                print("🌟 Nenhum favorito salvo.")
                return
        else:
            start_url = sys.argv[1]

    # Inicia a aplicação
    window = Browlite(start_url)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()