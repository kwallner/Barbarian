[Setup]
AppName=Barbarian
AppVerName=Barbarian 1.3.6
AppPublisher=Karl Wallner <kwallner@mail.de>
AppPublisherURL=http://github.com/kwallner/Barbarian
AppSupportURL=http://github.com/kwallner/Barbarian
AppUpdatesURL=http://github.com/kwallner/Barbarian
ArchitecturesInstallIn64BitMode=x64
ArchitecturesAllowed=x64
DefaultDirName={pf}\Barbarian
DefaultGroupName=Barbarian
Compression=lzma
SolidCompression=yes
OutputDir=..            
OutputBaseFilename=Barbarian-1.3.6

[Files]
Source: "Barbarian\Cmder.exe";          DestDir: "{app}"
Source: "Barbarian\LICENSE.txt";        DestDir: "{app}"
Source: "Barbarian\README.md";          DestDir: "{app}"
Source: "Barbarian\bin\*";              DestDir: "{app}\bin";       Flags: recursesubdirs
Source: "Barbarian\config\*";           DestDir: "{app}\config";    Flags: recursesubdirs
Source: "Barbarian\icons\*";            DestDir: "{app}\icons";     Flags: recursesubdirs
Source: "Barbarian\vendor\*";           DestDir: "{app}\vendor";    Flags: recursesubdirs

[Icons]
Name: "{group}\Cmder"; Filename: "{app}\Cmder.exe"; Parameters: ""; WorkingDir: "{app}"
Name: "{group}\Visual Studio Code"; Filename: "{app}\vendor\vscode-for-windows\Code.exe"; Parameters: ""; WorkingDir: "{app}"
Name: "{group}\KDiff3"; Filename: "{app}\vendor\kdiff3-for-windows\kdiff3.exe"; Parameters: ""; WorkingDir: "{app}"
Name: "{group}\GitExtensions"; Filename: "{app}\vendor\gitext-for-windows\GitExtensions.exe"; Parameters: ""; WorkingDir: "{app}"
