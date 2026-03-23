; Script généré grâce à Gemini pour Inno Setup

#define MyAppName "PyConverter"
#define MyAppVersion "1.0"
#define MyAppPublisher "Mon Projet Perso"
#define MyAppExeName "pyconverter.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{A1B2C3D4-E5F6-7890-1234-56789ABCDEF0}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
; Remove the following line to run in administrative install mode (install for all users.)
PrivilegesRequired=admin
OutputDir=Output
OutputBaseFilename=PyConverter_Installer_v1.0
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "french"; MessagesFile: "compiler:Languages\French.isl"

[Files]
; Le fichier exécutable généré par PyInstaller
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"

[Registry]
; --- Menu Contextuel Principal ---
Root: HKCR; Subkey: "*\shell\PyConverter"; ValueType: string; ValueName: "MUIVerb"; ValueData: "PyConverter"; Flags: uninsdeletekey
Root: HKCR; Subkey: "*\shell\PyConverter"; ValueType: string; ValueName: "Icon"; ValueData: """{app}\{#MyAppExeName}"",0"
Root: HKCR; Subkey: "*\shell\PyConverter"; ValueType: string; ValueName: "SubCommands"; ValueData: ""

; --- Option 1: Ouvrir l'interface ---
Root: HKCR; Subkey: "*\shell\PyConverter\shell\01_GUI"; ValueType: string; ValueData: "Ouvrir l'interface..."; Flags: uninsdeletekey
Root: HKCR; Subkey: "*\shell\PyConverter\shell\01_GUI"; ValueType: string; ValueName: "Icon"; ValueData: "imageres.dll,-102"
Root: HKCR; Subkey: "*\shell\PyConverter\shell\01_GUI\command"; ValueType: string; ValueData: """{app}\{#MyAppExeName}"" ""%1"""

; --- Option 2: PNG ---
Root: HKCR; Subkey: "*\shell\PyConverter\shell\02_PNG"; ValueType: string; ValueData: "Convertir en PNG (Image)"; Flags: uninsdeletekey
Root: HKCR; Subkey: "*\shell\PyConverter\shell\02_PNG"; ValueType: string; ValueName: "Icon"; ValueData: "imageres.dll,-72"
Root: HKCR; Subkey: "*\shell\PyConverter\shell\02_PNG\command"; ValueType: string; ValueData: """{app}\{#MyAppExeName}"" ""%1"" --to .png --direct"

; --- Option 3: JPG ---
Root: HKCR; Subkey: "*\shell\PyConverter\shell\03_JPG"; ValueType: string; ValueData: "Convertir en JPG (Image)"; Flags: uninsdeletekey
Root: HKCR; Subkey: "*\shell\PyConverter\shell\03_JPG"; ValueType: string; ValueName: "Icon"; ValueData: "imageres.dll,-72"
Root: HKCR; Subkey: "*\shell\PyConverter\shell\03_JPG\command"; ValueType: string; ValueData: """{app}\{#MyAppExeName}"" ""%1"" --to .jpg --direct"

; --- Option 4: MP4 ---
Root: HKCR; Subkey: "*\shell\PyConverter\shell\04_MP4"; ValueType: string; ValueData: "Convertir en MP4 (Video)"; Flags: uninsdeletekey
Root: HKCR; Subkey: "*\shell\PyConverter\shell\04_MP4"; ValueType: string; ValueName: "Icon"; ValueData: "imageres.dll,-18"
Root: HKCR; Subkey: "*\shell\PyConverter\shell\04_MP4\command"; ValueType: string; ValueData: """{app}\{#MyAppExeName}"" ""%1"" --to .mp4 --direct"

; --- Option 5: MP3 ---
Root: HKCR; Subkey: "*\shell\PyConverter\shell\05_MP3"; ValueType: string; ValueData: "Extraire Audio (MP3)"; Flags: uninsdeletekey
Root: HKCR; Subkey: "*\shell\PyConverter\shell\05_MP3"; ValueType: string; ValueName: "Icon"; ValueData: "imageres.dll,-1008"
Root: HKCR; Subkey: "*\shell\PyConverter\shell\05_MP3\command"; ValueType: string; ValueData: """{app}\{#MyAppExeName}"" ""%1"" --to .mp3 --direct"
