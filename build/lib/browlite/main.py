#!/usr/bin/env python3
import sys
import os
import configparser
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QVBoxLayout, QWidget,
    QToolBar, QAction, QStatusBar, QProgressBar, QMenuBar,
    QInputDialog, QMessageBox, QMenu
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QSize
from PyQt5.QtGui import QIcon

class Browlite(QMainWindow):
    def __init__(self, start_url=None):
        super().__init__()
        
        # Initialize paths
        self.app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_file = os.path.join(self.app_dir, 'config.ini')
        self.favs_file = os.path.join(self.app_dir, 'favs.txt')
        
        # Search engine configuration
        self.search_engines = {
            'google': {
                'name': 'Google',
                'url': 'https://www.google.com/search?q={}',
                'icon': self.resource_path('icons/google.png')
            },
            'duckduckgo': {
                'name': 'DuckDuckGo',
                'url': 'https://duckduckgo.com/?q={}',
                'icon': self.resource_path('icons/duckduckgo.png')
            },
            'bing': {
                'name': 'Bing',
                'url': 'https://www.bing.com/search?q={}',
                'icon': self.resource_path('icons/bing.png')
            },
            'yahoo': {
                'name': 'Yahoo',
                'url': 'https://search.yahoo.com/search?p={}',
                'icon': self.resource_path('icons/yahoo.png')
            },
            'ecosia': {
                'name': 'Ecosia',
                'url': 'https://www.ecosia.org/search?q={}',
                'icon': self.resource_path('icons/ecosia.png')
            }
        }
        
        # Load configuration
        self.load_config()
        self.load_favorites()
        
        # Setup UI
        self.init_ui()
        self.apply_theme()
        
        # Navigate to initial URL
        initial_url = QUrl(start_url) if start_url else QUrl(self.homepage)
        self.browser.setUrl(initial_url)

    def resource_path(self, relative_path):
        return os.path.join(self.app_dir, 'browlite', 'resources', relative_path)

    def load_config(self):
        self.config = configparser.ConfigParser()
        if not os.path.exists(self.config_file):
            self.create_default_config()
        self.config.read(self.config_file)
        
        self.homepage = self.config['DEFAULT'].get('homepage', 'https://www.google.com')
        self.dark_mode = self.config['DEFAULT'].getboolean('dark_mode', True)
        self.default_search = self.config['DEFAULT'].get('default_search_engine', 'google')

    def create_default_config(self):
        self.config['DEFAULT'] = {
            'homepage': 'https://www.google.com',
            'dark_mode': 'true',
            'default_search_engine': 'google'
        }
        with open(self.config_file, 'w') as f:
            self.config.write(f)

    def init_ui(self):
        self.setWindowTitle("Browlite")
        self.resize(1024, 768)
        self.setMinimumSize(800, 600)
        self.setSizePolicy(QWidget().sizePolicy())

        self.browser = QWebEngineView()
        self.urlbar = QLineEdit()
        
        self.setup_toolbar()
        self.setup_menu()
        self.setup_statusbar()
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.browser)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        self.browser.urlChanged.connect(self.update_urlbar)
        self.browser.loadProgress.connect(self.update_progress)

    def setup_toolbar(self):
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(toolbar)
        
        nav_actions = [
            ('back.png', "Back", self.browser.back),
            ('forward.png', "Forward", self.browser.forward),
            ('refresh.png', "Refresh", self.browser.reload),
            ('home.png', "Home", self.go_home)
        ]
        
        for icon, text, callback in nav_actions:
            action = QAction(QIcon(self.resource_path(f'icons/{icon}')), text, self)
            action.triggered.connect(callback)
            toolbar.addAction(action)
        
        self.urlbar.setPlaceholderText("Enter URL or search term...")
        toolbar.addWidget(self.urlbar)
        
        self.search_menu = QMenu("Search Engine")
        for engine_id, engine_data in self.search_engines.items():
            action = QAction(QIcon(engine_data['icon']), engine_data['name'], self)
            action.triggered.connect(lambda _, e=engine_id: self.set_search_engine(e))
            self.search_menu.addAction(action)
        
        toolbar.addAction(self.search_menu.menuAction())

    def setup_menu(self):
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        view_menu = menubar.addMenu("View")
        self.dark_mode_action = QAction("Dark Mode", self, checkable=True)
        self.dark_mode_action.setChecked(self.dark_mode)
        self.dark_mode_action.toggled.connect(self.toggle_dark_mode)
        view_menu.addAction(self.dark_mode_action)

    def setup_statusbar(self):
        self.statusbar = self.statusBar()
        self.progress_bar = QProgressBar()
        self.statusbar.addPermanentWidget(self.progress_bar)
        self.progress_bar.hide()

    def apply_theme(self):
        if self.dark_mode:
            self.setStyleSheet("""
                QMainWindow { background-color: #2d2d2d; }
                QToolBar { background-color: #34403d; border: none; }
                QLineEdit { 
                    background-color: #3b4f4b; 
                    color: #e0fff7; 
                    border: 1px solid #5fc3ad; 
                    padding: 5px; 
                    selection-background-color: #5fc3ad;
                }
                QStatusBar { background-color: #34403d; color: #aaffee; }
                QProgressBar { 
                    border: 1px solid #5fc3ad; 
                    border-radius: 3px; 
                    background-color: #2f3b38; 
                    text-align: center; 
                }
                QProgressBar::chunk { background-color: #5fc3ad; width: 10px; }
            """)
        else:
            self.setStyleSheet("""
                QMainWindow { background-color: #f8fefc; }
                QToolBar { background-color: #e6f7f3; border: none; }
                QLineEdit { 
                    background-color: #ffffff; 
                    color: #000000; 
                    border: 1px solid #80d9c4; 
                    padding: 5px; 
                    selection-background-color: #5fc3ad;
                }
                QStatusBar { background-color: #e6f7f3; color: #337d6b; }
                QProgressBar { 
                    border: 1px solid #80d9c4; 
                    border-radius: 3px; 
                    background-color: #f0fefb; 
                    text-align: center; 
                }
                QProgressBar::chunk { background-color: #5fc3ad; width: 10px; }
            """)

    def toggle_dark_mode(self, checked):
        self.dark_mode = checked
        self.config['DEFAULT']['dark_mode'] = str(checked).lower()
        with open(self.config_file, 'w') as f:
            self.config.write(f)
        self.apply_theme()

    def set_search_engine(self, engine_id):
        if engine_id in self.search_engines:
            self.default_search = engine_id
            self.config['DEFAULT']['default_search_engine'] = engine_id
            with open(self.config_file, 'w') as f:
                self.config.write(f)
            QMessageBox.information(
                self, 
                "Search Engine Changed", 
                f"Default search engine set to {self.search_engines[engine_id]['name']}"
            )

    def navigate_to_url(self):
        url = self.urlbar.text().strip()
        if not url:
            return
            
        if url == "-favs":
            self.show_favorites()
        elif url.startswith(('http://', 'https://')):
            self.browser.setUrl(QUrl(url))
        else:
            search_url = self.search_engines[self.default_search]['url'].format(url)
            self.browser.setUrl(QUrl(search_url))

    def update_urlbar(self, q):
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)
        self.progress_bar.setVisible(progress < 100)

    def go_home(self):
        self.browser.setUrl(QUrl(self.homepage))

    def load_favorites(self):
        if not os.path.exists(self.favs_file):
            self.favorites = []
            return
        with open(self.favs_file, 'r') as f:
            self.favorites = [line.strip() for line in f if line.strip()]

    def save_favorites(self):
        with open(self.favs_file, 'w') as f:
            f.write('\n'.join(self.favorites))

    def show_favorites(self):
        if not self.favorites:
            QMessageBox.information(self, "Favorites", "No favorites saved yet.")
            return
            
        items = [f"{i+1}. {url}" for i, url in enumerate(self.favorites)]
        item, ok = QInputDialog.getItem(
            self, "Favorites", "Select a favorite:", items, 0, False)
            
        if ok and item:
            url = item.split(". ", 1)[1]
            self.browser.setUrl(QUrl(url))

    def closeEvent(self, event):
        self.save_favorites()
        event.accept()

def main():
    os.environ['QT_QPA_PLATFORM'] = 'xcb'
    app = QApplication(sys.argv)
    app.setApplicationName("Browlite")
    app.setApplicationVersion("1.0.0")
    
    start_url = sys.argv[1] if len(sys.argv) > 1 else None
    
    window = Browlite(start_url)
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
