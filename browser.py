import sys
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QListWidget, QWidget, QToolBar, QMenu, QAction, QSplitter
from PyQt5.QtWebEngineWidgets import QWebEngineView

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Web Browser")
        
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.load_url)
        self.url_bar.textChanged.connect(self.update_url)
        
        self.go_button = QPushButton("Go")
        self.go_button.clicked.connect(self.load_url)
        
        self.browser = QWebEngineView()
        self.browser.urlChanged.connect(self.update_url_bar)
        
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.browser.back)
        
        self.forward_button = QPushButton("Forward")
        self.forward_button.clicked.connect(self.browser.forward)
        
        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.load_url_from_history)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.forward_button)
        button_layout.addWidget(self.url_bar)
        button_layout.addWidget(self.go_button)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.browser)
        
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.history_list)
        
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        right_widget = QWidget()
        right_widget.setLayout(right_layout)
        
        split_layout = QSplitter()
        split_layout.addWidget(main_widget)
        split_layout.addWidget(right_widget)
        
        self.setCentralWidget(split_layout)
        
        self.load_url()  # Load the default URL on startup
        
        self.create_toolbar()
        
    def create_toolbar(self):
        toolbar = QToolBar()
        
        history_action = QAction("History", self)
        history_action.triggered.connect(self.toggle_history_menu)
        toolbar.addAction(history_action)
        
        self.addToolBar(toolbar)
        
    def toggle_history_menu(self):
        if self.history_list.isHidden():
            self.history_list.show()
        else:
            self.history_list.hide()
        
    def load_url(self):
        input_text = self.url_bar.text()
        
        # If the input is a valid URL, load it directly
        if QUrl.fromUserInput(input_text).isValid():
            url = QUrl.fromUserInput(input_text)
        else:
            # Treat input as a search query
            search_engine_url = "https://www.google.com/search?q="
            query = input_text.replace(" ", "+")
            url = QUrl(search_engine_url + query)
        
        self.browser.load(url)
        
    def load_url_from_history(self, item):
        url = item.text()
        self.url_bar.setText(url)
        self.load_url()
        
    def update_url(self, text):
        # Add the URL to the history only if it is a valid URL and not empty
        if text and QUrl.fromUserInput(text).isValid():
            self.history_list.addItem(text)
        
    def update_url_bar(self, url):
        self.url_bar.setText(url.toString())
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec_())
