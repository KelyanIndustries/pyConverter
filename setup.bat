@echo off
setlocal


set "SCRIPT_DIR=%~dp0"

set "EXE_PATH=%SCRIPT_DIR%dist\pyconverter.exe"

echo Configuration de PyConverter avec le chemin : 
echo %EXE_PATH%
echo.


if not exist "%EXE_PATH%" (
    echo ERREUR : L'executable n'a pas ete trouve a l'emplacement prevu.
    echo %EXE_PATH%
    pause
    exit /b
)

echo Ajout des cles de registre...
echo.

:: 1. Main Menu Item
reg add "HKEY_CLASSES_ROOT\*\shell\PyConverter" /v "MUIVerb" /t REG_SZ /d "PyConverter" /f
reg add "HKEY_CLASSES_ROOT\*\shell\PyConverter" /v "Icon" /t REG_SZ /d "\"%EXE_PATH%\",0" /f
reg add "HKEY_CLASSES_ROOT\*\shell\PyConverter" /v "SubCommands" /t REG_SZ /d "" /f

:: 2. Option 01: GUI
reg add "HKEY_CLASSES_ROOT\*\shell\PyConverter\shell\01_GUI" /ve /t REG_SZ /d "Ouvrir l'interface..." /f
reg add "HKEY_CLASSES_ROOT\*\shell\PyConverter\shell\01_GUI" /v "Icon" /t REG_SZ /d "imageres.dll,-102" /f
reg add "HKEY_CLASSES_ROOT\*\shell\PyConverter\shell\01_GUI\command" /ve /t REG_SZ /d "\"%EXE_PATH%\" \"%%1\"" /f

:: 3. Option 02: PNG
reg add "HKEY_CLASSES_ROOT\*\shell\PyConverter\shell\02_PNG" /ve /t REG_SZ /d "Convertir en PNG (Image)" /f
reg add "HKEY_CLASSES_ROOT\*\shell\PyConverter\shell\02_PNG" /v "Icon" /t REG_SZ /d "imageres.dll,-72" /f
reg add "HKEY_CLASSES_ROOT\*\shell\PyConverter\shell\02_PNG\command" /ve /t REG_SZ /d "\"%EXE_PATH%\" \"%%1\" --to .png --direct" /f

:: 4. Option 03: JPG
reg add "HKEY_CLASSES_ROOT\*\shell\PyConverter\shell\03_JPG" /ve /t REG_SZ /d "Convertir en JPG (Image)" /f
reg add "HKEY_CLASSES_ROOT\*\shell\PyConverter\shell\03_JPG" /v "Icon" /t REG_SZ /d "imageres.dll,-72" /f
reg add "HKEY_CLASSES_ROOT\*\shell\PyConverter\shell\03_JPG\command" /ve /t REG_SZ /d "\"%EXE_PATH%\" \"%%1\" --to .jpg --direct" /f

:: 5. Option 04: MP4
reg add "HKEY_CLASSES_ROOT\*\shell\PyConverter\shell\04_MP4" /ve /t REG_SZ /d "Convertir en MP4 (Video)" /f
reg add "HKEY_CLASSES_ROOT\*\shell\PyConverter\shell\04_MP4" /v "Icon" /t REG_SZ /d "imageres.dll,-18" /f
reg add "HKEY_CLASSES_ROOT\*\shell\PyConverter\shell\04_MP4\command" /ve /t REG_SZ /d "\"%EXE_PATH%\" \"%%1\" --to .mp4 --direct" /f

:: 6. Option 05: MP3
reg add "HKEY_CLASSES_ROOT\*\shell\PyConverter\shell\05_MP3" /ve /t REG_SZ /d "Extraire Audio (MP3)" /f
reg add "HKEY_CLASSES_ROOT\*\shell\PyConverter\shell\05_MP3" /v "Icon" /t REG_SZ /d "imageres.dll,-1008" /f
reg add "HKEY_CLASSES_ROOT\*\shell\PyConverter\shell\05_MP3\command" /ve /t REG_SZ /d "\"%EXE_PATH%\" \"%%1\" --to .mp3 --direct" /f

echo.
echo Termine ! Le menu contextuel a ete mis a jour.
pause
