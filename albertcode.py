import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime
from PySide6.QtWidgets import (QApplication, QMainWindow, QTextEdit, QFileDialog, 
                               QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QTreeView, QMenu, QInputDialog, QMessageBox, QFileSystemModel, QHeaderView)
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor, QStandardItemModel, QStandardItem, QDesktopServices, QContextMenuEvent, QAction
from PySide6.QtCore import Qt, QDir, QRegularExpression, QUrl, QSize

class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super(SyntaxHighlighter, self).__init__(parent)
        self.highlighting_rules = []

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#569CD6"))
        keywords = ["def", "class", "if", "elif", "else", "while", "for", "try", "except", "import", "from", "as", "return"]
        for word in keywords:
            self.highlighting_rules.append((f"\\b{word}\\b", keyword_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            expression = QRegularExpression(pattern)
            index = expression.globalMatch(text)
            while index.hasNext():
                match = index.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)

class CodeEditor(QTextEdit):
    def __init__(self):
        super().__init__()
        self.highlighter = SyntaxHighlighter(self.document())

class FileTreeView(QTreeView):
    def __init__(self, parent=None):
        super(FileTreeView, self).__init__(parent)  # Appel correct de la méthode __init__ de la classe de base
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())  # Utilisez QDir.rootPath() pour définir le chemin racine
        self.setModel(self.model)

        # Rendre la largeur réglable
        self.header().setStretchLastSection(True)
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)

        # Augmenter la taille des éléments
        font = self.font()
        font.setPointSize(12)  # Ajustez la taille de la police selon vos besoins
        self.setFont(font)

        # Ajouter des icônes
        self.setIconSize(QSize(24, 24))  # Ajustez la taille des icônes selon vos besoins

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.open_context_menu)
        self.doubleClicked.connect(self.handle_double_click)

    def handle_double_click(self, index):
        file_path = self.model.filePath(index)
        if Path(file_path).is_file():
            self.parent().open_file(file_path)

    def open_context_menu(self, position):
        index = self.indexAt(position)
        if not index.isValid():
            return

        menu = QMenu()
        open_action = QAction("Ouvrir", self)
        open_action.triggered.connect(lambda: self.parent().open_file(self.model.filePath(index)))
        copy_action = QAction("Copier", self)
        copy_action.triggered.connect(lambda: self.copy_file(index))
        properties_action = QAction("Propriétés du fichier", self)
        properties_action.triggered.connect(lambda: self.file_properties(index))
        menu.addAction(open_action)
        menu.addAction(copy_action)
        menu.addAction(properties_action)
        menu.exec(self.viewport().mapToGlobal(position))

    def copy_file(self, index):
        file_path = self.model.filePath(index)
        QApplication.clipboard().setText(file_path)

    def file_properties(self, index):
        file_path = self.model.filePath(index)
        file_info = Path(file_path)
        properties = f"Path: {file_info}\nSize: {file_info.stat().st_size} bytes\nCreated: {datetime.fromtimestamp(file_info.stat().st_ctime)}\nModified: {datetime.fromtimestamp(file_info.stat().st_mtime)}"
        QMessageBox.information(self, "File Properties", properties)

    def open_file(self, file_path):
        # Logique pour ouvrir le fichier
        with open(file_path, 'r') as file:
            content = file.read()
            # Afficher le contenu du fichier dans l'éditeur de texte, par exemple
            self.editor.setText(content)

class AlbertCode(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Albert Code")
        self.setGeometry(100, 100, 800, 600)

        self.current_file_path = None

        self.editor = CodeEditor()
        
        self.file_tree_view = FileTreeView(self)
        self.file_tree_model = QStandardItemModel()
        self.file_tree_view.setModel(self.file_tree_model)
        self.file_tree_view.hide()

        self.info_bar = QLabel("Language: None")
        self.info_bar.setStyleSheet("color: green")

        self.create_actions()
        self.create_menu_bar()
        button_style = ("""
            QPushButton {
                background-color: #5271ff;
                color: white;
                padding: 10px;
                font-size: 20px;
                border: 2px solid #5271ff;
                border-radius: 8px;
                border-style: inset;
            }

            QPushButton:hover {
                background-color: #3e5eb9;
            }

            QPushButton:pressed {
                background-color: #3e5eb9;
            }
        """)
        self.open_folder_button = QPushButton("Open Folder")
        self.open_folder_button.setStyleSheet(button_style)
        self.open_folder_button.clicked.connect(self.open_folder)

        self.new_file_button = QPushButton("New File")
        self.new_file_button.setStyleSheet(button_style)
        self.new_file_button.clicked.connect(self.new_file)

        self.new_folder_button = QPushButton("New Folder")
        self.new_folder_button.setStyleSheet(button_style)
        self.new_folder_button.clicked.connect(self.new_folder)

        self.run_code_button = QPushButton("Run Code")
        self.run_code_button.setStyleSheet(button_style)
        self.run_code_button.clicked.connect(self.run_code)

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.open_folder_button)
        left_layout.addWidget(self.new_file_button)
        left_layout.addWidget(self.new_folder_button)
        left_layout.addWidget(self.run_code_button)
        left_layout.addWidget(self.file_tree_view)

        left_widget = QWidget()
        left_widget.setLayout(left_layout)

        main_layout = QHBoxLayout()
        main_layout.addWidget(left_widget)
        main_layout.addWidget(self.editor)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)

        container = QVBoxLayout()
        container.addWidget(main_widget)
        container.addWidget(self.info_bar)

        container_widget = QWidget()
        container_widget.setLayout(container)

        self.setCentralWidget(container_widget)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: #dcdcdc;
                font-family: Arial, Helvetica, sans-serif;
                font-size: 14px;
            }
            QTreeView {
                background-color: #1e1e1e;
                color: #dcdcdc;
            }
            QLabel {
                color: #dcdcdc;
            }
            Qbutton
        """)

    def create_actions(self):
        self.save_action = QAction("&Save", self)
        self.save_action.triggered.connect(self.save_file)

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(self.save_action)

        extension_menu = menu_bar.addMenu("&Extensions")
        
        documentation_menu = menu_bar.addMenu("&Documentation")
        python_docs = QAction("Python Docs", self)
        python_docs.triggered.connect(lambda: self.open_web_url("https://docs.python.org/3/"))
        documentation_menu.addAction(python_docs)

        install_menu = menu_bar.addMenu("&Install Modules")
        install_package = QAction("Install Python Package", self)
        install_package.triggered.connect(self.install_package)
        install_menu.addAction(install_package)

    def open_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.file_tree_model.clear()
            self.load_folder(folder_path)
            self.file_tree_view.show()

    def load_folder(self, folder_path):
        root_item = self.file_tree_model.invisibleRootItem()
        self.add_items(root_item, Path(folder_path))

    def add_items(self, parent_item, path):
        for child in path.iterdir():
            item = QStandardItem(child.name)
            parent_item.appendRow(item)
            if child.is_dir():
                self.add_items(item, child)


    def new_file(self):
        text, ok = QInputDialog.getText(self, "Create a file", "Enter a file name:")
        if ok:
            extension, ok_ext = QInputDialog.getText(self, "Create a file", "Extension of the file :")
            if ok_ext:
                # Ouvrir l'explorateur de fichiers pour sélectionner le chemin
                path = QFileDialog.getExistingDirectory(self, "Select Directory")
                if path:  # Vérifier si un chemin a été sélectionné
                    full_path = f"{path}/{text}.{extension}"
                    with open(full_path, "w+") as file:
                        if extension == "py":
                            file.write(f"# Starting development with {text}.py")
                        else:
                            pass
        AlbertCode.load_folder("./")
        

        

    def new_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            new_folder_name, ok = QInputDialog.getText(self, "New Folder", "Enter folder name:")
            if ok:
                Path(folder_path, new_folder_name).mkdir()
                self.open_folder()

    def save_file(self):
        if self.current_file_path:
            with open(self.current_file_path, 'w') as file:
                file.write(self.editor.toPlainText())
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File As")
        if file_path:
            self.current_file_path = file_path
            self.save_file()

    def open_file(self, file_path):
        with open(file_path, 'r') as file:
            self.editor.setPlainText(file.read())
        self.current_file_path = file_path
        self.update_info_bar(file_path)

    def update_file_list():
        pass

    def update_info_bar(self, file_path):
        _, extension = os.path.splitext(file_path)
        language = "None"
        if extension == ".py":
            language = "Python"
        self.info_bar.setText(f"Language: {language}")

    def run_code(self):
        if self.current_file_path:
            command = f'python "{self.current_file_path}"'
            try:
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
                QMessageBox.information(self, "Run Output", output)
            except subprocess.CalledProcessError as e:
                QMessageBox.critical(self, "Run Error", e.output)

    def install_package(self):
        package, ok = QInputDialog.getText(self, "Install Package", "Enter package name:")
        if ok and package:
            command = f'pip install {package}'
            try:
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
                QMessageBox.information(self, "Install Output", output)
            except subprocess.CalledProcessError as e:
                QMessageBox.critical(self, "Install Error", e.output)

    def open_web_url(self, url):
        QDesktopServices.openUrl(QUrl(url))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AlbertCode()
    window.show()
    sys.exit(app.exec())
