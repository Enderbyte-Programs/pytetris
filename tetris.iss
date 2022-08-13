#define MyAppName "Tetris 22"
#define MyAppVersion "0.6"
#define MyAppPublisher "Enderbyte Programs LLC"
#define MyAppURL "https://sites.google.com/view/enderbyteprograms"
#define MyAppExeName "tetris.exe"

[Setup]
AppId={{1ABD5B1C-9E27-4F58-8004-ABCC29245086}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=C:\Python310\Scripts\tetris-22\license.txt
; Remove the following line to run in administrative install mode (install for all users.)
PrivilegesRequired=lowest
OutputDir=C:\Python310\Scripts\tetris-22
OutputBaseFilename=Tetris22-v0.6-installer
SetupIconFile=C:\Python310\Scripts\tetris-22\logo.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "C:\Python310\Scripts\tetris-22\dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Python310\Scripts\tetris-22\t22assets\logo.png"; DestDir: "{app}\t22assets"; Flags: ignoreversion
Source: "C:\Python310\Scripts\tetris-22\t22assets\tetris.mp3"; DestDir: "{app}\t22assets"; Flags: ignoreversion
Source: "C:\Python310\Scripts\tetris-22\t22assets\laser.wav"; DestDir: "{app}\t22assets"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:ProgramOnTheWeb,{#MyAppName}}"; Filename: "{#MyAppURL}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

