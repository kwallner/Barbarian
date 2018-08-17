[Setup]
AppName=@name@
AppVerName=@name@ @version@
AppPublisher=@author@
AppPublisherURL=@url@
AppSupportURL=@url@
AppUpdatesURL=@url@
ArchitecturesInstallIn64BitMode=x64
ArchitecturesAllowed=x64
DefaultDirName={userpf}\@name@
DefaultGroupName=@name@
Compression=lzma2
PrivilegesRequired=lowest
AlwaysUsePersonalGroup=yes
OutputDir=.
OutputBaseFilename=@name@-@version@

[Components]
#ifdef with_git
Name: component_git;                                      Description: "Install Git (https://git-scm.com)";                             Types: full compact custom
#endif
#ifdef with_cmake
Name: component_cmake;                                    Description: "Install CMake (https:://cmake.org)";                            Types: full custom
#endif
#ifdef with_python
Name: component_python;                                   Description: "Install Python and Conan.io (https:://conan.io)";               Types: full custom
#endif
#ifdef with_vscode
Name: component_vscode;                                   Description: "Install Visual Studio Code (https://code.visualstudio.com)";    Types: full
#endif
#ifdef with_kdiff3
Name: component_kdiff3;                                   Description: "Install KDiff3 (http://kdiff3.sourceforge.net)";                Types: full
#endif
#ifdef with_gitext
Name: component_gitext;                                   Description: "Install GitExtensions (http://gitextensions.github.io)";        Types: full
#endif

[Files]
Source: "@name@\Cmder.exe";                                DestDir: "{app}";                                           Flags: ignoreversion
Source: "@name@\LICENSE.txt";                              DestDir: "{app}";                                           Flags: ignoreversion
Source: "@name@\LICENSE";                                  DestDir: "{app}";                                           Flags: ignoreversion
Source: "@name@\README.txt";                               DestDir: "{app}";                                           Flags: ignoreversion isreadme
Source: "@name@\README.md";                                DestDir: "{app}";                                           Flags: ignoreversion
Source: "@name@\Version*";                                 DestDir: "{app}";                                           Flags: ignoreversion
Source: "@name@\bin\*";                                    DestDir: "{app}\bin";                                       Flags: recursesubdirs ignoreversion
Source: "@name@\config\*.*";                               DestDir: "{app}\config";                                    Flags: ignoreversion
#ifdef with_cmake
Source: "@name@\config\profile.d\cmake-for-windows.cmd";   DestDir: "{app}\config\profile.d";                          Flags: ignoreversion;    Components: component_cmake
#endif
#ifdef with_gitext
Source: "@name@\config\profile.d\gitext-for-windows.cmd";  DestDir: "{app}\config\profile.d";                          Flags: ignoreversion;    Components: component_gitext
#endif
#ifdef with_kdiff3
Source: "@name@\config\profile.d\kdiff3-for-windows.cmd";  DestDir: "{app}\config\profile.d";                          Flags: ignoreversion;    Components: component_kdiff3
#endif
#ifdef with_python
Source: "@name@\config\profile.d\python-for-windows.cmd";  DestDir: "{app}\config\profile.d";                          Flags: ignoreversion;    Components: component_python
#endif
#ifdef with_vscode
Source: "@name@\config\profile.d\vscode-for-windows.cmd";  DestDir: "{app}\config\profile.d";                          Flags: ignoreversion;    Components: component_vscode
#endif
Source: "@name@\icons\*";                                  DestDir: "{app}\icons";                                     Flags: recursesubdirs ignoreversion
Source: "@name@\vendor\*.*";                               DestDir: "{app}\vendor";                                    Flags: ignoreversion
Source: "@name@\vendor\clink\*";                           DestDir: "{app}\vendor\clink";                              Flags: recursesubdirs ignoreversion;
Source: "@name@\vendor\conemu-maximus5\*";                 DestDir: "{app}\vendor\conemu-maximus5";                    Flags: recursesubdirs ignoreversion;
Source: "@name@\vendor\lib\*";                             DestDir: "{app}\vendor\lib";                                Flags: recursesubdirs ignoreversion;
Source: "@name@\vendor\psmodules\*";                       DestDir: "{app}\vendor\psmodules";                          Flags: recursesubdirs ignoreversion;
Source: "@name@\vendor\clink-completions\*";               DestDir: "{app}\vendor\clink-completions";                  Flags: recursesubdirs ignoreversion;
#ifdef with_cmake
Source: "@name@\vendor\cmake-for-windows\*";               DestDir: "{app}\vendor\cmake-for-windows";                  Flags: recursesubdirs ignoreversion;    Components: component_cmake
#endif
#ifdef with_git
Source: "@name@\vendor\git-for-windows\*";                 DestDir: "{app}\vendor\git-for-windows";                    Flags: recursesubdirs ignoreversion;    Components: component_git
#endif
#ifdef with_gitext
Source: "@name@\vendor\gitext-for-windows\*";              DestDir: "{app}\vendor\gitext-for-windows";                 Flags: recursesubdirs ignoreversion;    Components: component_gitext
#endif
#ifdef with_kdiff3
Source: "@name@\vendor\kdiff3-for-windows\*";              DestDir: "{app}\vendor\kdiff3-for-windows";                 Flags: recursesubdirs ignoreversion;    Components: component_kdiff3
#endif
#ifdef with_python
Source: "@name@\vendor\python-for-windows\*";              DestDir: "{app}\vendor\python-for-windows";                 Flags: recursesubdirs ignoreversion;    Components: component_python;    Excludes: "__pycache__"
#endif
#ifdef with_vscode
Source: "@name@\vendor\vscode-for-windows\*";              DestDir: "{app}\vendor\vscode-for-windows";                 Flags: recursesubdirs ignoreversion;    Components: component_vscode
#endif

[UninstallDelete]
Type: files;            Name: "{app}\config\.history"
Type: files;            Name: "{app}\config\settings"
Type: files;            Name: "{app}\config\user-aliases.cmd"
Type: files;            Name: "{app}\config\user-ConEmu.xml"
Type: files;            Name: "{app}\config\user-profile.cmd"
Type: files;            Name: "{app}\vendor\conemu-maximus5\ConEmu.xml"
Type: dirifempty;       Name: "{app}\config\profile.d"

[Icons]
Name: "{group}\Cmder";                Filename: "{app}\Cmder.exe";                                    Parameters: ""; WorkingDir: "{app}"
#ifdef with_vscode
Name: "{group}\Visual Studio Code";   Filename: "{app}\vendor\vscode-for-windows\Code.exe";           Parameters: ""; WorkingDir: "{app}";    Components: component_vscode
#endif
#ifdef with_kdiff3
Name: "{group}\KDiff3";               Filename: "{app}\vendor\kdiff3-for-windows\kdiff3.exe";         Parameters: ""; WorkingDir: "{app}";    Components: component_kdiff3
#endif
#ifdef with_gitext
Name: "{group}\GitExtensions";        Filename: "{app}\vendor\gitext-for-windows\GitExtensions.exe";  Parameters: ""; WorkingDir: "{app}";    Components: component_gitext
#endif
Name: "{group}\Uninstall @name@";     Filename: "{uninstallexe}"
