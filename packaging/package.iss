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
Name: cmder;                                    Description: "Cmder (http://cmder.net/): Console emulator for Windows";                             Types: full compact custom;           Flags: fixed
#ifdef with_git
Name: git;                                      Description: "Git (https://git-scm.com): Distributed version control system";                       Types: full compact custom
#endif
#ifdef with_cmake
Name: cmake;                                    Description: "CMake (https:://cmake.org): Cross-Plattform Build System";                            Types: full custom
#endif
#ifdef with_python
Name: python;                                   Description: "Python (https:://python.org): Python Programming Language";                           Types: full custom
#ifdef with_conanio
Name: python/conanio;                           Description: "Conan.io (https:://conan.io): C/C++ Package Manager";                                 Types: full custom
#endif
#endif
#ifdef with_vscode
Name: vscode;                                   Description: "Visual Studio Code (https://code.visualstudio.com): IDE and Code Editor";             Types: full
#endif
#ifdef with_kdiff3
Name: kdiff3;                                   Description: "KDiff3 (http://kdiff3.sourceforge.net): Diff and Merge Tool";                         Types: full
#endif
#ifdef with_winmerge
Name: winmerge;                                 Description: "WinMerge (http://winmerge.org): Another Diff and Merge Tool";                         Types: full
#endif
#ifdef with_gitext
Name: gitext;                                   Description: "GitExtensions (http://gitextensions.github.io): Graphical User Interface for Git";    Types: full
#endif

[Files]
Source: "@name@\Cmder.exe";                                DestDir: "{app}";                                           Flags: ignoreversion
Source: "@name@\LICENSE.txt";                              DestDir: "{app}";                                           Flags: ignoreversion
Source: "@name@\README.txt";                               DestDir: "{app}";                                           Flags: ignoreversion isreadme
Source: "@name@\README.md";                                DestDir: "{app}";                                           Flags: ignoreversion
Source: "@name@\Version*";                                 DestDir: "{app}";                                           Flags: ignoreversion
Source: "@name@\bin\*";                                    DestDir: "{app}\bin";                                       Flags: recursesubdirs ignoreversion
Source: "@name@\config\*.*";                               DestDir: "{app}\config";                                    Flags: ignoreversion;    Permissions: users-modify
#ifdef with_cmake
Source: "@name@\config\profile.d\cmake-for-windows.cmd";   DestDir: "{app}\config\profile.d";                          Flags: ignoreversion;    Components: cmake
#endif
#ifdef with_gitext
Source: "@name@\config\profile.d\gitext-for-windows.cmd";  DestDir: "{app}\config\profile.d";                          Flags: ignoreversion;    Components: gitext
#endif
#ifdef with_kdiff3
Source: "@name@\config\profile.d\kdiff3-for-windows.cmd";  DestDir: "{app}\config\profile.d";                          Flags: ignoreversion;    Components: kdiff3
#endif
#ifdef with_winmerge
Source: "@name@\config\profile.d\winmerge-for-windows.cmd"; DestDir: "{app}\config\profile.d";                          Flags: ignoreversion;    Components: winmerge
#endif
#ifdef with_python
Source: "@name@\config\profile.d\python-for-windows.cmd";  DestDir: "{app}\config\profile.d";                          Flags: ignoreversion;    Components: python
#endif
#ifdef with_vscode
Source: "@name@\config\profile.d\vscode-for-windows.cmd";  DestDir: "{app}\config\profile.d";                          Flags: ignoreversion;    Components: vscode
#endif
Source: "@name@\icons\*";                                  DestDir: "{app}\icons";                                     Flags: recursesubdirs ignoreversion
Source: "@name@\vendor\*.*";                               DestDir: "{app}\vendor";                                    Flags: ignoreversion
Source: "@name@\vendor\clink\*";                           DestDir: "{app}\vendor\clink";                              Flags: recursesubdirs ignoreversion;
Source: "@name@\vendor\conemu-maximus5\*";                 DestDir: "{app}\vendor\conemu-maximus5";                    Flags: recursesubdirs ignoreversion;
Source: "@name@\vendor\lib\*";                             DestDir: "{app}\vendor\lib";                                Flags: recursesubdirs ignoreversion;
Source: "@name@\vendor\psmodules\*";                       DestDir: "{app}\vendor\psmodules";                          Flags: recursesubdirs ignoreversion;
Source: "@name@\vendor\clink-completions\*";               DestDir: "{app}\vendor\clink-completions";                  Flags: recursesubdirs ignoreversion;
#ifdef with_cmake
Source: "@name@\vendor\cmake-for-windows\*";               DestDir: "{app}\vendor\cmake-for-windows";                  Flags: recursesubdirs ignoreversion;    Components: cmake
#endif
#ifdef with_git
Source: "@name@\vendor\git-for-windows\*";                 DestDir: "{app}\vendor\git-for-windows";                    Flags: recursesubdirs ignoreversion;    Components: git
#endif
#ifdef with_gitext
Source: "@name@\vendor\gitext-for-windows\*";              DestDir: "{app}\vendor\gitext-for-windows";                 Flags: recursesubdirs ignoreversion;    Components: gitext
#endif
#ifdef with_kdiff3
Source: "@name@\vendor\kdiff3-for-windows\*";              DestDir: "{app}\vendor\kdiff3-for-windows";                 Flags: recursesubdirs ignoreversion;    Components: kdiff3
#endif
#ifdef with_winmerge
Source: "@name@\vendor\winmerge-for-windows\*";            DestDir: "{app}\vendor\winmerge-for-windows";                 Flags: recursesubdirs ignoreversion;    Components: kdiff3
#endif
#ifdef with_python
#ifdef with_conanio
Source: "@name@\vendor\python-for-windows\*";              DestDir: "{app}\vendor\python-for-windows";                 Flags: recursesubdirs ignoreversion;    Components: python and python/conanio;        Permissions: users-modify;    Excludes: "__pycache__,conans,conan*"
Source: "@name@\vendor\python-for-windows\*";              DestDir: "{app}\vendor\python-for-windows";                 Flags: recursesubdirs ignoreversion;    Components: python and not python/conanio;    Permissions: users-modify;    Excludes: "__pycache__"
#else
Source: "@name@\vendor\python-for-windows\*";              DestDir: "{app}\vendor\python-for-windows";                 Flags: recursesubdirs ignoreversion;    Components: python;                           Permissions: users-modify;    Excludes: "__pycache__"
#endif
#endif
#ifdef with_vscode
Source: "@name@\vendor\vscode-for-windows\*";              DestDir: "{app}\vendor\vscode-for-windows";                 Flags: recursesubdirs ignoreversion;    Components: vscode;    Permissions: users-modify
#endif

[Dirs]
Name: "{app}\config";                          Permissions: users-modify
Name: "{app}\config\profile.d";                Permissions: users-modify
#ifdef with_python
Name: "{app}\vendor\python-for-windows";       Permissions: users-modify
#endif
#ifdef with_vscode
Name: "{app}\vendor\vscode-for-windows";       Permissions: users-modify
#endif

[UninstallDelete]
Type: files;            Name: "{app}\config\.history"
Type: files;            Name: "{app}\config\settings"
Type: files;            Name: "{app}\config\user-aliases.cmd"
Type: files;            Name: "{app}\config\user-ConEmu.xml"
Type: files;            Name: "{app}\config\user-profile.cmd"
Type: filesandordirs;   Name: "{app}\vendor"
Type: dirifempty;       Name: "{app}\config\profile.d"

[Icons]
Name: "{group}\Cmder";                Filename: "{app}\Cmder.exe";                                    Parameters: ""; WorkingDir: "{userdocs}"
#ifdef with_vscode
Name: "{group}\Visual Studio Code";   Filename: "{app}\vendor\vscode-for-windows\Code.exe";           Parameters: ""; WorkingDir: "{userdocs}";    Components: vscode
#endif
#ifdef with_kdiff3
Name: "{group}\KDiff3";               Filename: "{app}\vendor\kdiff3-for-windows\kdiff3.exe";         Parameters: ""; WorkingDir: "{userdocs}";    Components: kdiff3
#endif
#ifdef with_winmerge
Name: "{group}\WinMerge";             Filename: "{app}\vendor\winmerge-for-windows\WinMergeU.exe";    Parameters: ""; WorkingDir: "{userdocs}";    Components: kdiff3
#endif
#ifdef with_gitext
Name: "{group}\GitExtensions";        Filename: "{app}\vendor\gitext-for-windows\GitExtensions.exe";  Parameters: ""; WorkingDir: "{userdocs}";    Components: gitext
#endif
Name: "{group}\Uninstall @name@";     Filename: "{uninstallexe}"
