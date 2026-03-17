[Setup]
AppName=Monitor de Sistema Avanzado
AppVersion=2.0
; Publisher
AppPublisher=Desarrollador Profesional
AppSupportURL=https://github.com/monitor-sistema
AppUpdatesURL=https://github.com/monitor-sistema

DefaultDirName={autopf}\MonitorSistema
DefaultGroupName=Monitor Sistema
OutputDir=Output
OutputBaseFilename=MonitorSistema-Setup-v2
; Icono nativo Inno Setup
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\MonitorSistema.exe

Compression=lzma2/ultra64
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "startupicon"; Description: "Ejecutar al iniciar Windows"; GroupDescription: "Arranque:"; Flags: unchecked

[Files]
; IMPORTANT: Asume que build.py generó dist/MonitorSistema/ usando --onedir
Source: "..\dist\MonitorSistema\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; Source: "license.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Monitor Sistema"; Filename: "{app}\MonitorSistema.exe"
Name: "{group}\Desinstalar Monitor"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Monitor Sistema"; Filename: "{app}\MonitorSistema.exe"; Tasks: desktopicon
Name: "{userstartup}\Monitor Sistema"; Filename: "{app}\MonitorSistema.exe"; Tasks: startupicon

[Registry]
; Asociar extensión custom .msreport
Root: HKCR; Subkey: ".msreport"; ValueType: string; ValueName: ""; ValueData: "MonitorSistemaReport"; Flags: uninsdeletevalue
Root: HKCR; Subkey: "MonitorSistemaReport"; ValueType: string; ValueName: ""; ValueData: "Reporte de Monitor Sistema"; Flags: uninsdeletekey
Root: HKCR; Subkey: "MonitorSistemaReport\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\MonitorSistema.exe,0"
Root: HKCR; Subkey: "MonitorSistemaReport\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\MonitorSistema.exe"" ""%1"""

[Run]
Filename: "{app}\MonitorSistema.exe"; Description: "{cm:LaunchProgram,Monitor Sistema}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
