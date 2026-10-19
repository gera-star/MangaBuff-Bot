; 2R2R installer (Inno Setup 6).
; Build: ISCC /DAppVersion=11.0.0 /DDistDir=<folder with 2R2R.exe> installer\buffy.iss

#ifndef AppVersion
  #define AppVersion "11.0.10"
#endif
#ifndef DistDir
  #define DistDir "..\dist\2R2R"
#endif

[Setup]
AppId={{6F4B7C2E-9D1A-4E7B-A3C5-B0FF1E5A9D21}
AppName=2R2R
AppVersion={#AppVersion}
AppVerName=2R2R {#AppVersion}
AppPublisher=Qu4dyz
AppPublisherURL=https://github.com/gera-star/MangaBuff-Bot
AppSupportURL=https://github.com/gera-star/MangaBuff-Bot/issues
; Per-user install: no admin prompt, updates in place
PrivilegesRequired=lowest
DefaultDirName={localappdata}\Programs\2R2R
DisableProgramGroupPage=yes
DisableDirPage=auto
UninstallDisplayIcon={app}\2R2R.exe
UninstallDisplayName=2R2R
SetupIconFile=..\buffy\assets\buffy.ico
WizardStyle=modern
Compression=lzma2/normal
SolidCompression=no
OutputDir=..\dist
OutputBaseFilename=2R2R-Setup-{#AppVersion}
CloseApplications=yes
CloseApplicationsFilter=Buffy.exe,2R2R.exe
RestartApplications=no
VersionInfoVersion={#AppVersion}
VersionInfoProductName=2R2R
VersionInfoDescription=2R2R - MangaBuff autopilot installer

[Languages]
Name: "ru"; MessagesFile: "compiler:Languages\Russian.isl"
Name: "en"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "{#DistDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\2R2R"; Filename: "{app}\2R2R.exe"
Name: "{autodesktop}\2R2R"; Filename: "{app}\2R2R.exe"; Tasks: desktopicon

[Registry]
; Remove the "start with Windows" entry the app may have added
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: none; ValueName: "Buffy"; Flags: uninsdeletevalue dontcreatekey

[Run]
Filename: "{app}\2R2R.exe"; Description: "{cm:LaunchProgram,2R2R}"; Flags: nowait postinstall skipifsilent
; Silent install = self-update from inside 2R2R: start the new version right away
Filename: "{app}\2R2R.exe"; Flags: nowait; Check: WizardSilent

[UninstallRun]
Filename: "{sys}\taskkill.exe"; Parameters: "/F /IM 2R2R.exe"; Flags: runhidden; RunOnceId: "StopBuffy"
