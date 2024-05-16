# AlbertCode
### Documentation Complète pour le Projet Albert Code

#### Table des Matières

1. Introduction
2. Objectifs du Projet
3. Pré-requis
4. Configuration de l'Environnement de Développement
5. Développement de l'Interface Utilisateur
    - Structure de l'Application Electron
    - Création des Composants de l'Interface
    - Intégration de Monaco Editor
6. Intégration de Python
    - Écriture du Script Python
    - Conversion en Exécutable avec PyInstaller
7. Communication entre Electron et Python
    - Utilisation de `child_process` pour Exécuter le Script
    - Gestion des Entrées et Sorties
8. Fonctionnalités Avancées
    - Installation de Bibliothèques Python via pip
    - Gestion des Erreurs et des Logs
9. Développement Backend (Optionnel)
    - Création d'une API REST avec Flask
    - Communication via WebSockets
10. Emballage et Distribution
    - Création d'un Installateur avec Electron Builder
    - Tests et Déploiement
11. Ressources et Références

### 1. Introduction

Albert Code est un IDE (Environnement de Développement Intégré) conçu pour être simple à utiliser, ergonomique et éducatif. Il cible principalement les langages Python, JavaScript, HTML et CSS. Ce projet vise à fournir une plateforme conviviale pour les débutants en programmation tout en offrant des fonctionnalités puissantes pour les utilisateurs avancés.

### 2. Objectifs du Projet

- **Simplicité** : Une interface utilisateur intuitive et facile à utiliser.
- **Éducation** : Outils et ressources intégrés pour aider les débutants à apprendre à coder.
- **Multiplateforme** : Fonctionne sur Windows, macOS et Linux.
- **Autonome** : N'exige pas l'installation de Python sur la machine de l'utilisateur.

### 3. Pré-requis

- Node.js et npm (Node Package Manager) installés.
- Python installé pour le développement et les tests (bien que ce ne soit pas nécessaire pour les utilisateurs finaux).
- PyInstaller pour convertir les scripts Python en exécutables.

### 4. Configuration de l'Environnement de Développement

1. **Installer Node.js et npm** :
   Téléchargez et installez Node.js à partir de [nodejs.org](https://nodejs.org/).

2. **Créer un Nouveau Projet Electron** :
   ```bash
   mkdir albert-code
   cd albert-code
   npm init -y
   npm install electron --save-dev
   ```

3. **Configurer le Projet Electron** :
   Créez un fichier `main.js` à la racine de votre projet :
   ```javascript
   const { app, BrowserWindow } = require('electron');
   const path = require('path');

   function createWindow() {
       const win = new BrowserWindow({
           width: 800,
           height: 600,
           webPreferences: {
               preload: path.join(__dirname, 'preload.js')
           }
       });

       win.loadFile('index.html');
   }

   app.whenReady().then(createWindow);

   app.on('window-all-closed', () => {
       if (process.platform !== 'darwin') {
           app.quit();
       }
   });

   app.on('activate', () => {
       if (BrowserWindow.getAllWindows().length === 0) {
           createWindow();
       }
   });
   ```

   Créez un fichier `preload.js` pour le script de préchargement :
   ```javascript
   window.addEventListener('DOMContentLoaded', () => {
       const replaceText = (selector, text) => {
           const element = document.getElementById(selector);
           if (element) element.innerText = text;
       };

       for (const type of ['chrome', 'node', 'electron']) {
           replaceText(`${type}-version`, process.versions[type]);
       }
   });
   ```

4. **Créer les Fichiers HTML et CSS** :
   Créez un fichier `index.html` :
   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>Albert Code</title>
       <link rel="stylesheet" href="styles.css">
   </head>
   <body>
       <h1>Welcome to Albert Code</h1>
       <div id="editor"></div>
       <script src="renderer.js"></script>
   </body>
   </html>
   ```

   Créez un fichier `styles.css` pour les styles de base :
   ```css
   body {
       font-family: Arial, sans-serif;
       margin: 0;
       padding: 0;
       display: flex;
       flex-direction: column;
       height: 100vh;
   }

   #editor {
       flex-grow: 1;
       display: flex;
   }
   ```

5. **Configurer le Fichier package.json** :
   Modifiez `package.json` pour ajouter des scripts de démarrage :
   ```json
   {
       "name": "albert-code",
       "version": "1.0.0",
       "main": "main.js",
       "scripts": {
           "start": "electron ."
       },
       "devDependencies": {
           "electron": "^12.0.0"
       }
   }
   ```

### 5. Développement de l'Interface Utilisateur

#### Structure de l'Application Electron

1. **Installer Monaco Editor** :
   ```bash
   npm install monaco-editor
   ```

2. **Intégrer Monaco Editor dans renderer.js** :
   Créez un fichier `renderer.js` et ajoutez le code suivant pour initialiser l'éditeur :
   ```javascript
   const monaco = require('monaco-editor');

   window.addEventListener('DOMContentLoaded', () => {
       monaco.editor.create(document.getElementById('editor'), {
           value: '// Welcome to Albert Code\n',
           language: 'javascript',
           theme: 'vs-dark',
       });
   });
   ```

#### Création des Composants de l'Interface

1. **Améliorer l'Interface Utilisateur** :
   Modifiez `index.html` pour ajouter plus de structure :
   ```html
   <body>
       <header>
           <h1>Albert Code</h1>
       </header>
       <main>
           <div id="editor-container">
               <div id="editor"></div>
           </div>
           <div id="console"></div>
       </main>
       <footer>
           <button id="run-button">Run</button>
       </footer>
       <script src="renderer.js"></script>
   </body>
   ```

2. **Styling Avancé avec CSS** :
   Modifiez `styles.css` pour améliorer le design :
   ```css
   header, footer {
       background-color: #333;
       color: #fff;
       padding: 10px;
       text-align: center;
   }

   #editor-container {
       flex-grow: 1;
       display: flex;
       flex-direction: column;
   }

   #editor {
       flex-grow: 1;
   }

   #console {
       height: 150px;
       background-color: #1e1e1e;
       color: #fff;
       overflow-y: auto;
       padding: 10px;
   }

   button {
       background-color: #28a745;
       border: none;
       color: white;
       padding: 10px 20px;
       text-align: center;
       display: inline-block;
       font-size: 16px;
       cursor: pointer;
   }

   button:hover {
       background-color: #218838;
   }
   ```

### 6. Intégration de Python

#### Écriture du Script Python

1. **Créer le Script Python Principal** :
   Créez un fichier `script.py` avec le contenu suivant :
   ```python
   import sys
   import json

   def process_data(data):
       result = {
           "status": "success",
           "data": data
       }
       return result

   def main():
       try:
           input_data = sys.stdin.read()
           data = json.loads(input_data)
           result = process_data(data)
           print(json.dumps(result))
       except Exception as e:
           print(json.dumps({"error": str(e)}), file=sys.stderr)
           sys.exit(1)

   if __name__ == '__main__':
       main()
   ```

#### Conversion en Exécutable avec PyInstaller

1. **Installer PyInstaller** :
   ```bash
   pip install pyinstaller
   ```

2. **Créer l'Exécutable** :
   Utilisez PyInstaller pour convertir le script en un exécutable :
   ```bash
   pyinstaller --onefile script.py
   ```

   L'exécutable se trouvera dans le dossier `dist`.

### 7. Communication entre Electron et Python

#### Utilisation de `child_process` pour Exécuter le Script

1. **Modifier renderer.js pour Exécuter le Script** :
   ```javascript
   const { execFile } = require('child_process');
   const path = require('path');

   document.getElementById('run-button').addEventListener('click', () => {
       const editorContent = monaco.editor.getModels()[0].getValue();
       runPythonScript({ code: editorContent }, (error, result) => {
           if (error) {
               console.error('Failed to run script:', error);
               document.getElementById('console').innerText = `Error: ${error.message}`;
               return;
           }
           console.log('Script result:', result);
           document.getElementById('console').innerText = JSON.stringify(result, null, 2);
       });
   });

   function runPythonScript(inputData, callback) {
       const pythonExecutable = path.join(__dirname, 'dist', 'script'); // Adjust path if necessary
       const input = JSON.stringify(inputData);

       const process = execFile(pythonExecutable, (error, stdout, stderr) => {
           if (error) {
               console.error('Error:', error);
               callback(error, null);
               return;
           }
           if (stderr) {
               console.error('Stderr:', stderr);
               callback(new Error(stderr), null);
               return;
           }
           const result = JSON.parse(stdout);
           callback(null, result);
       });

       // Send input data to the executable via stdin
       process.stdin.write(input);
       process.stdin.end();
   }
   ```

### 8. Fonctionnalités Avancées

#### Installation de Bibliothèques Python via pip

1. **Configurer un Script d’Installation** :
   Vous pouvez écrire un script Python ou un script shell pour installer des bibliothèques supplémentaires dans l’environnement virtuel de l’application. Ce script peut être exécuté au premier lancement de l'application ou à la demande.

   Exemple de script Python pour installer une bibliothèque :
   ```python
   import subprocess
   import sys

   def install_package(package_name):
       subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

   if __name__ == '__main__':
       install_package("requests")  # Remplacez par le nom de la bibliothèque souhaitée
   ```

2. **Exécuter ce Script depuis Electron** :
   ```javascript
   const { execFile } = require('child_process');
   const path = require('path');

   function installPythonPackage(packageName, callback) {
       const installScript = path.join(__dirname, 'install_package.py');
       execFile('python', [installScript, packageName], (error, stdout, stderr) => {
           if (error) {
               console.error('Error:', error);
               callback(error);
               return;
           }
           if (stderr) {
               console.error('Stderr:', stderr);
               callback(new Error(stderr));
               return;
           }
           console.log('Package installed:', stdout);
           callback(null, stdout);
       });
   }

   // Exemple d'utilisation
   installPythonPackage('requests', (error, result) => {
       if (error) {
           console.error('Failed to install package:', error);
           return;
       }
       console.log('Package installation result:', result);
   });
   ```

#### Gestion des Erreurs et des Logs

1. **Ajouter un Système de Logs** :
   Implémentez un système de journalisation dans votre script Python pour capturer et enregistrer les erreurs et les événements importants.

   Exemple de script Python avec journalisation :
   ```python
   import sys
   import json
   import logging

   logging.basicConfig(filename='albert_code.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

   def process_data(data):
       logging.debug(f"Processing data: {data}")
       result = {
           "status": "success",
           "data": data
       }
       return result

   def main():
       try:
           input_data = sys.stdin.read()
           data = json.loads(input_data)
           result = process_data(data)
           logging.info("Processing completed successfully")
           print(json.dumps(result))
       except Exception as e:
           logging.error(f"An error occurred: {str(e)}")
           print(json.dumps({"error": str(e)}), file=sys.stderr)
           sys.exit(1)

   if __name__ == '__main__':
       main()
   ```

2. **Afficher les Logs dans l'Interface Electron** :
   Ajoutez une fonctionnalité dans l'interface Electron pour afficher les logs à partir du fichier de journalisation.

   Exemple de lecture et affichage des logs :
   ```javascript
   const fs = require('fs');
   const logFilePath = path.join(__dirname, 'albert_code.log');

   function displayLogs() {
       fs.readFile(logFilePath, 'utf8', (err, data) => {
           if (err) {
               console.error('Error reading log file:', err);
               return;
           }
           document.getElementById('console').innerText = data;
       });
   }

   // Exemple d'utilisation
   displayLogs();
   ```

### 9. Développement Backend (Optionnel)

#### Création d'une API REST avec Flask

1. **Installer Flask** :
   ```bash
   pip install flask
   ```

2. **Créer un Serveur Flask** :
   Créez un fichier `server.py` pour votre serveur Flask :
   ```python
   from flask import Flask, request, jsonify

   app = Flask(__name__)

   @app.route('/api/run', methods=['POST'])
   def run_code():
       data = request.json
       # Ajoutez votre logique de traitement ici
       result = {
           "status": "success",
           "data": data
       }
       return jsonify(result)

   if __name__ == '__main__':
       app.run(port=5000)
   ```

3. **Lancer le Serveur** :
   Exécutez le serveur Flask :
   ```bash
   python server.py
   ```

#### Communication via WebSockets

1. **Installer Flask-SocketIO** :
   ```bash
   pip install flask-socketio
   ```

2. **Configurer le Serveur Flask avec WebSockets** :
   Modifiez `server.py` pour utiliser Flask-SocketIO :
   ```python
   from flask import Flask, request, jsonify
   from flask_socketio import SocketIO, emit

   app = Flask(__name__)
   socketio = SocketIO(app)

   @app.route('/api/run', methods=['POST'])
   def run_code():
       data = request.json
       result = {
           "status": "success",
           "data": data
       }
       return jsonify(result)

   @socketio.on('message')
   def handle_message(message):
       print('received message: ' + message)
       emit('response', {'data': 'Message received!'})

   if __name__ == '__main__':
       socketio.run(app, port=5000)
   ```

3. **Client WebSocket dans Electron** :
   Utilisez `socket.io-client` pour établir une connexion WebSocket dans Electron :
   ```javascript
   const io = require('socket.io-client');
   const socket = io('http://localhost:5000');

   socket.on('connect', () => {
       console.log('Connected to server');
       socket.send('Hello from Electron');
   });

   socket.on('response', (data) => {
       console.log('Received response:', data);
       document.getElementById('console').innerText = JSON.stringify(data, null, 2);
   });
   ```

### 10. Emballage et Distribution

#### Création d'un Installateur avec Electron Builder

1. **Installer Electron Builder** :
   ```bash
   npm install --save-dev electron-builder
   ```

2. **Configurer `package.json` pour Electron Builder** :
   Ajoutez la configuration d’Electron Builder à votre `package.json` :
   ```json
   {
       "name": "albert-code",
       "version": "1.0.0",
       "main": "main.js",
       "scripts": {
           "start": "electron .",
           "pack": "electron-builder --dir",
           "dist": "electron-builder"
       },
       "build": {
           "appId": "com.albertcode.ide",
           "productName": "Albert Code",
           "files": [
               "dist/**/*",
               "main.js",
               "preload.js",
               "index.html",
               "renderer.js",
               "styles.css",
               "albert_code.log"
           ],
           "mac": {
               "target": "dmg"
           },
           "win": {
               "target": "nsis"
           },
           "linux": {
               "target": "AppImage"
           }
       },
       "devDependencies": {
           "electron": "^12.0.0",
           "electron-builder": "^22.9.1"
       },
       "dependencies": {
           "monaco-editor": "^0.22.3",
           "socket.io-client": "^4.0.0"
       }
   }
   ```

3. **Construire l'Application** :
   ```bash
   npm run dist
   ```

   Cela créera des fichiers d'installation pour macOS, Windows et Linux dans le dossier `dist`.

#### Tests et Déploiement

1. **Tester sur Différentes Plates-formes** :
   Assurez-vous de tester l'application sur Windows, macOS et Linux pour vérifier qu'elle fonctionne correctement sur toutes les plateformes.

2. **Déploiement** :
   Utilisez des services comme GitHub Releases, DigitalOcean, ou tout autre hébergeur de votre choix pour distribuer les fichiers d'installation.

### 11. Ressources et Références

- [Documentation Electron](https://www.electronjs.org/docs)
- [PyInstaller Documentation](https://pyinstaller.readthedocs.io/en/stable/)
- [Monaco Editor Documentation](https://microsoft.github.io/monaco-editor/)
- [Flask Documentation](https://flask.palletsprojects.com/en/latest/)
Socket.IO Documentation
