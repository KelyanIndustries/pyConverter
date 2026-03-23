# PyConverter

**PyConverter** est un outil puissant et léger pour convertir vos images et vidéos rapidement. Conçu avec une interface moderne (**CustomTkinter**) et une intégration native à l'explorateur Windows, il permet de traiter des fichiers par lots en quelques clics.

## Fonctionnalités

- **Conversion d'Images** : Supporte JPG, PNG, WEBP, BMP, ICO, TIFF.
- **Conversion Vidéo** : Supporte MP4, AVI, MOV, MKV, WEBM.
- **Extraction Audio** : Extrayez le son de n'importe quelle vidéo en MP3.
- **GIF Maker** : Convertissez des vidéos en fichiers GIF animés.
- **Intégration Windows** : Convertissez directement depuis le clic-droit (Menu Contextuel).
- **Mode Batch** : Traitez des dizaines de fichiers simultanément.
- **Mode Ligne de Commande** : Utilisable sans interface pour l'automatisation.

## Installation

### Option 1 : Installeur Windows (Recommandé)

Téléchargez simplement la dernière version depuis l'onglet **[Releases](../../releases)** de ce dépôt.

1. Lancez `PyConverter_Installer_vX.X.exe`.
2. Suivez les instructions.
3. Une fois installé, faites un **clic-droit** sur un fichier image ou vidéo pour voir les options "PyConverter".

### Option 2 : Exécutable Portable

Si vous ne souhaitez pas installer le logiciel :

1. Téléchargez `pyconverter.exe` depuis les releases.
2. Utilisez le script `setup.bat` (fourni dans ce dépôt ou à côté de l'exe) si vous souhaitez ajouter manuellement les options au clic-droit.

## Installation depuis les sources (Développeurs)

Si vous souhaitez modifier le code ou compiler vous-même l'application.

### Prérequis

- Python 3.10+
- ffmpeg (généralement installé via imageio-ffmpeg)

### Étapes

1.  **Cloner le dépôt :**

    ```bash
    git clone https://github.com/votre-username/pyConverter.git
    cd pyConverter
    ```

2.  **Créer un environnement virtuel :**

    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Linux/Mac
    source .venv/bin/activate
    ```

3.  **Installer les dépendances :**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Lancer l'application :**
    ```bash
    python main.py
    ```

## Compiler l'exécutable (Build)

Pour recréer l'exécutable unique `.exe` :

1.  Assurez-vous d'être dans votre environnement virtuel.
2.  Lancez PyInstaller avec le fichier de spécification inclus :
    ```bash
    pyinstaller pyconverter.spec
    ```
3.  Le fichier généré se trouvera dans le dossier `dist/`.

### Créer l'installateur (Inno Setup)

Si vous avez **Inno Setup** installé, ouvrez le fichier `pyconverter_installer.iss` et compilez-le pour générer un installateur professionnel qui configure automatiquement le registre Windows.

## Note sur la compatibilité Linux / MacOS

Bien que ce projet soit **optimisé pour Windows** (notamment pour les fonctionnalités de menu contextuel via le Registre et les notifications système Windows), le cœur du code est écrit en Python pur.

- **GUI & Logique** : Fonctionnent parfaitement sur Linux et macOS (CustomTkinter et MoviePy sont cross-platform).
- **Limitations** : Le menu contextuel (clic-droit) et le script `setup.bat` sont spécifiques à Windows. Sur Linux, vous pouvez utiliser l'application via le terminal ou l'interface graphique classique.

## Utilisation en Ligne de Commande (CLI)

Vous pouvez utiliser PyConverter dans vos propres scripts :

```bash
# Convertir une vidéo en MP4 sans ouvrir l'interface
python main.py "C:\Chemin\Vers\Video.avi" --to .mp4 --direct

# Convertir une image en PNG
python main.py "image.jpg" --to .png --direct
```

## Licence

Distribué sous la licence **CC BY-NC 4.0** (Creative Commons Attribution - Pas d'Utilisation Commerciale).

Cela signifie que vous êtes libre de :

- **Partager** — copier, distribuer et communiquer le matériel par tous moyens et sous tous formats.
- **Adapter** — remixer, transformer et créer à partir du matériel.

Selon les conditions suivantes :

- **Attribution** — Vous devez créditer l'œuvre, intégrer un lien vers la licence et indiquer si des modifications ont été effectuées.
- **Pas d’Utilisation Commerciale** — Vous n'êtes pas autorisé à faire un usage commercial de cette œuvre, tout ou partie du matériel la composant.

Voir `LICENSE` pour plus d'informations.
