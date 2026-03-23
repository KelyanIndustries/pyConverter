import sys
import os
import argparse
from plyer import notification
from src.config import FORMATS_IMAGE, FORMATS_VIDEO
from src.utils import is_image, is_video, MOVIEPY_AVAILABLE, MOVIEPY_ERROR
from src.server import start_server, send_file_to_server
from src.core_conversion import convert_file
from src.gui import App

def process_headless(input_file, target_ext):
    """Effectue une conversion directe sans interface graphique."""
    if not os.path.exists(input_file):
        print(f"Erreur: Fichier introuvable {input_file}")
        return
    if not target_ext.startswith('.'):
        target_ext = '.' + target_ext

    if is_image(input_file):
         if target_ext not in FORMATS_IMAGE:
             print(f"Erreur: Impossible de convertir image vers {target_ext}")
             return
    elif is_video(input_file):
         pass

    try:
        output_path = convert_file(input_file, target_ext)
        print(f"Succès: {output_path}")

        try:
            notification.notify(
                title="Conversion Terminée",
                message=f"{os.path.basename(output_path)} a été créé avec succès.",
                timeout=5
            )
        except Exception as e:
            print(f"Erreur notification: {e}")

    except Exception as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convertisseur Média Pro")
    parser.add_argument("files", nargs="*", help="Fichier(s) d'entrée")
    parser.add_argument("--to", help="Format de conversion cible (ex: .png, .mp4)", default=None)
    parser.add_argument("--direct", action="store_true", help="Conversion directe sans GUI")

    args = parser.parse_args()

    if args.direct and args.to and args.files:
        # Mode Direct
        for f in args.files:
            process_headless(f, args.to)
    else:
        # Mode GUI
        if args.files:
            is_server = start_server()
            if is_server:
                app = App(initial_files=args.files)
                app.mainloop()
            else:
                for f in args.files:
                    send_file_to_server(f)
                sys.exit(0)
        else:
            # Lancement sans fichier
            is_server = start_server()
            if is_server:
                app = App()
                app.mainloop()
            else:
                 sys.exit(0)
