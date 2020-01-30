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
AllowNetworkDrive=no
CloseApplications=yes
OutputDir=.
OutputBaseFilename=@output_base_name@
UninstallDisplayIcon={app}\Barbarian.ico
SetupIconFile=@name@\Barbarian.ico

[Messages]
WelcomeLabel1=Barbarian - A Software Development Environment for Conan.io

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
#ifdef with_conanio_pip
Name: python/conanio;                           Description: "Conan.io (https:://conan.io): C/C++ Package Manager";                                 Types: full custom
#endif
#endif
#ifdef with_conanio_standalone
Name: conanio;                                  Description: "Conan.io (https:://conan.io): C/C++ Package Manager (Standalone)";                                 Types: full custom
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
#ifdef with_graphviz
Name: graphviz;                                 Description: "Graphviz (https://www.graphviz.org): Graph Visualization Software";                    Types: full
#endif
#ifdef with_doxygen
Name: doxygen;                                  Description: "Doxygen (http://www.doxygen.nl): Generate documentation from source code";           Types: full
#endif
#ifdef with_ninja
Name: ninja;                                   Description: "Ninja (https://ninja-build.org): Ninja is a small build system with a focus on speed";           Types: full
#endif
#ifdef with_npp
Name: npp;                                   Description: "Notepad++ (https://notepad-plus-plus.org): Source code editor and Notepad replacement";           Types: full
#endif

[Files]
Source: "@name@\Cmder.exe";                                DestDir: "{app}";                                           Flags: ignoreversion
Source: "@name@\LICENSE.txt";                              DestDir: "{app}";                                           Flags: ignoreversion
Source: "@name@\README.txt";                               DestDir: "{app}";                                           Flags: ignoreversion
Source: "@name@\README.md";                                DestDir: "{app}";                                           Flags: ignoreversion
Source: "@name@\Barbarian.ico";                            DestDir: "{app}";                                           Flags: ignoreversion
Source: "@name@\Barbarian.png";                            DestDir: "{app}";                                           Flags: ignoreversion
Source: "@name@\bin\*";                                    DestDir: "{app}\bin";                                       Flags: recursesubdirs createallsubdirs ignoreversion
Source: "@name@\config\*.*";                               DestDir: "{app}\config";                                    Flags: ignoreversion;    Permissions: users-modify
#ifdef with_git
Source: "@name@\config\profile.d\git-for-windows.*";       DestDir: "{app}\config\profile.d";                          Flags: ignoreversion;    Components: git
#endif
#ifdef with_cmake
Source: "@name@\config\profile.d\cmake-for-windows.*";     DestDir: "{app}\config\profile.d";                          Flags: ignoreversion;    Components: cmake
#endif
#ifdef with_gitext
Source: "@name@\config\profile.d\gitext-for-windows.*";    DestDir: "{app}\config\profile.d";                          Flags: ignoreversion;    Components: gitext
#endif
#ifdef with_kdiff3
Source: "@name@\config\profile.d\kdiff3-for-windows.*";    DestDir: "{app}\config\profile.d";                          Flags: ignoreversion;    Components: kdiff3
#endif
#ifdef with_winmerge
Source: "@name@\config\profile.d\winmerge-for-windows.*";  DestDir: "{app}\config\profile.d";                          Flags: ignoreversion;    Components: winmerge
#endif
#ifdef with_python
Source: "@name@\config\profile.d\python-for-windows.*";    DestDir: "{app}\config\profile.d";                          Flags: ignoreversion;    Components: python
#endif
#ifdef with_conanio_standalone
Source: "@name@\config\profile.d\conan-for-windows.*";    DestDir: "{app}\config\profile.d";                          Flags: ignoreversion;    Components: conanio
#endif
#ifdef with_vscode
Source: "@name@\config\profile.d\vscode-for-windows.*";    DestDir: "{app}\config\profile.d";                          Flags: ignoreversion;    Components: vscode
#endif
#ifdef with_graphviz
Source: "@name@\config\profile.d\graphviz-for-windows.*";    DestDir: "{app}\config\profile.d";                          Flags: ignoreversion;    Components: graphviz
#endif
#ifdef with_doxygen
Source: "@name@\config\profile.d\doxygen-for-windows.*";    DestDir: "{app}\config\profile.d";                          Flags: ignoreversion;    Components: doxygen
#endif
#ifdef with_ninja
Source: "@name@\config\profile.d\ninja-for-windows.*";    DestDir: "{app}\config\profile.d";                          Flags: ignoreversion;    Components: ninja
#endif
#ifdef with_npp
Source: "@name@\config\profile.d\npp-for-windows.*";    DestDir: "{app}\config\profile.d";                          Flags: ignoreversion;    Components: npp
#endif
Source: "@name@\icons\*";                                  DestDir: "{app}\icons";                                     Flags: recursesubdirs createallsubdirs ignoreversion
Source: "@name@\vendor\*.*";                               DestDir: "{app}\vendor";                                    Flags: ignoreversion
Source: "@name@\vendor\bin\*";                             DestDir: "{app}\vendor\bin";                                Flags: recursesubdirs createallsubdirs ignoreversion;
Source: "@name@\vendor\clink\*";                           DestDir: "{app}\vendor\clink";                              Flags: recursesubdirs createallsubdirs ignoreversion;
Source: "@name@\vendor\conemu-maximus5\*";                 DestDir: "{app}\vendor\conemu-maximus5";                    Flags: recursesubdirs createallsubdirs ignoreversion;
Source: "@name@\vendor\lib\*";                             DestDir: "{app}\vendor\lib";                                Flags: recursesubdirs createallsubdirs ignoreversion;
Source: "@name@\vendor\psmodules\*";                       DestDir: "{app}\vendor\psmodules";                          Flags: recursesubdirs createallsubdirs ignoreversion;
Source: "@name@\vendor\clink-completions\*";               DestDir: "{app}\vendor\clink-completions";                  Flags: recursesubdirs createallsubdirs ignoreversion;
Source: "@name@\vendor\barbarian-extra\*";                 DestDir: "{app}\vendor\barbarian-extra";                  Flags: recursesubdirs createallsubdirs ignoreversion;
#ifdef with_cmake
Source: "@name@\vendor\cmake-for-windows\*";               DestDir: "{app}\vendor\cmake-for-windows";                  Flags: recursesubdirs createallsubdirs ignoreversion;    Components: cmake
#endif
#ifdef with_git
Source: "@name@\vendor\git-for-windows\*";                 DestDir: "{app}\vendor\git-for-windows";                    Flags: recursesubdirs createallsubdirs  ignoreversion;    Components: git
#endif
#ifdef with_gitext
Source: "@name@\vendor\gitext-for-windows\*";              DestDir: "{app}\vendor\gitext-for-windows";                 Flags: recursesubdirs createallsubdirs  ignoreversion;    Components: gitext
#endif
#ifdef with_kdiff3
Source: "@name@\vendor\kdiff3-for-windows\*";              DestDir: "{app}\vendor\kdiff3-for-windows";                 Flags: recursesubdirs createallsubdirs ignoreversion;    Components: kdiff3
#endif
#ifdef with_winmerge
Source: "@name@\vendor\winmerge-for-windows\*";            DestDir: "{app}\vendor\winmerge-for-windows";               Flags: recursesubdirs createallsubdirs ignoreversion;    Components: winmerge
#endif
#ifdef with_python
#ifdef with_conanio_pip
Source: "@name@\vendor\python-for-windows\*";              DestDir: "{app}\vendor\python-for-windows";                 Flags: recursesubdirs createallsubdirs ignoreversion;    Components: python;        Permissions: users-modify;    Excludes: "__pycache__,conans,conan*"
Source: "@name@\vendor\python-for-windows\@winpython3_subdirectory@\Scripts\conan*"; DestDir: "{app}\vendor\python-for-windows\@winpython3_subdirectory@\Scripts";         Flags: recursesubdirs createallsubdirs ignoreversion;    Components: python/conanio;Permissions: users-modify;    Excludes: "__pycache__"
Source: "@name@\vendor\python-for-windows\@winpython3_subdirectory@\Lib\site-packages\conan-@conan_version@.dist-info\*"; DestDir: "{app}\vendor\python-for-windows\@winpython3_subdirectory@\Lib\site-packages\conan-@conan_version@.dist-info";         Flags: recursesubdirs createallsubdirs ignoreversion;    Components: python/conanio;Permissions: users-modify;
Source: "@name@\vendor\python-for-windows\@winpython3_subdirectory@\Lib\site-packages\conans\*"; DestDir: "{app}\vendor\python-for-windows\@winpython3_subdirectory@\Lib\site-packages\conans";         Flags: recursesubdirs createallsubdirs ignoreversion;    Components: python/conanio;Permissions: users-modify;    Excludes: "__pycache__"
#else
Source: "@name@\vendor\python-for-windows\*";              DestDir: "{app}\vendor\python-for-windows";                 Flags: recursesubdirs createallsubdirs ignoreversion;    Components: python;    Permissions: users-modify;    Excludes: "__pycache__"
#endif
#endif
#ifdef with_conanio_standalone
Source: "@name@\vendor\conan-for-windows\*";              DestDir: "{app}\vendor\conan-for-windows";                 Flags: recursesubdirs createallsubdirs ignoreversion;    Components: conanio;    Permissions: users-modify
#endif
#ifdef with_vscode
Source: "@name@\vendor\vscode-for-windows\*";              DestDir: "{app}\vendor\vscode-for-windows";                 Flags: recursesubdirs createallsubdirs ignoreversion;    Components: vscode;    Permissions: users-modify
#endif
#ifdef with_graphviz
Source: "@name@\vendor\graphviz-for-windows\*";            DestDir: "{app}\vendor\graphviz-for-windows";               Flags: recursesubdirs createallsubdirs ignoreversion;    Components: graphviz;
#endif
#ifdef with_doxygen
Source: "@name@\vendor\doxygen-for-windows\*";             DestDir: "{app}\vendor\doxygen-for-windows";               Flags: recursesubdirs createallsubdirs ignoreversion;    Components: doxygen;
#endif
#ifdef with_ninja
Source: "@name@\vendor\ninja-for-windows\*";             DestDir: "{app}\vendor\ninja-for-windows";                Flags: recursesubdirs createallsubdirs ignoreversion;    Components: ninja; Permissions: users-modify
#endif
#ifdef with_npp
Source: "@name@\vendor\npp-for-windows\*";             DestDir: "{app}\vendor\npp-for-windows";                Flags: recursesubdirs createallsubdirs ignoreversion;    Components: npp; Permissions: users-modify
#endif

[Run]
Filename: "{app}\README.txt"; Description: "View the README file"; Flags: postinstall shellexec skipifsilent unchecked
Filename: "{app}\LICENSE.txt"; Description: "View the LICENSE file"; Flags: postinstall shellexec skipifsilent unchecked
#ifdef with_python
Filename: "{app}\vendor\python-for-windows\WinPython Control Panel.exe"; WorkingDir: "{app}\vendor\python-for-windows";  Description: "Start WinPython Control Panel"; Flags: postinstall skipifsilent unchecked;  Components: python
#endif
#ifdef with_gitext
Filename: "{sys}\regsvr32.exe"; Parameters: "/s /u GitExtensionsShellEx64.dll"; WorkingDir: "{app}\vendor\gitext-for-windows"; Flags: runhidden;  Components: gitext
Filename: "{app}\vendor\gitext-for-windows\GitExtensions.exe";  Description: "Start GitExtensions"; Flags: postinstall skipifsilent unchecked;  Components: gitext
#endif

[Dirs]
Name: "{app}\config";                          Permissions: users-modify
Name: "{app}\config\profile.d";                Permissions: users-modify
#ifdef with_python
Name: "{app}\vendor\python-for-windows";       Permissions: users-modify;    Components: python
#endif
#ifdef with_vscode
Name: "{app}\vendor\vscode-for-windows";       Permissions: users-modify;    Components: vscode
#endif

[UninstallRun]
#ifdef with_gitext
Filename: "{sys}\regsvr32.exe"; Parameters: "/s /u GitExtensionsShellEx64.dll"; WorkingDir: "{app}\vendor\gitext-for-windows"; Flags: runhidden;  Components: gitext
#endif

[UninstallDelete]
Type: files;            Name: "{app}\config\.history"
Type: files;            Name: "{app}\config\settings"
Type: files;            Name: "{app}\config\user_aliases.*"
Type: files;            Name: "{app}\config\user-ConEmu.xml"
Type: files;            Name: "{app}\config\user_profile.*"
Type: filesandordirs;   Name: "{app}\vendor"
Type: dirifempty;       Name: "{app}\config\profile.d"
Type: dirifempty;       Name: "{app}"

[Icons]
Name: "{group}\Cmder";                Filename: "{app}\Cmder.exe";                                    Parameters: ""; WorkingDir: "{userdocs}"
#ifdef with_python
Name: "{group}\WinPython\IDLE (Python IDE)";   Filename: "{app}\vendor\python-for-windows\IDLE (Python GUI).exe";                       Parameters: ""; WorkingDir: "{userdocs}";    Components: python
Name: "{group}\WinPython\IPython Qt Console";   Filename: "{app}\vendor\python-for-windows\IPython Qt Console.exe";                     Parameters: ""; WorkingDir: "{userdocs}";    Components: python
//Name: "{group}\WinPython\Jupyter Lab";   Filename: "{app}\vendor\python-for-windows\Jupyter Lab.exe";                                   Parameters: ""; WorkingDir: "{userdocs}";    Components: python
//Name: "{group}\WinPython\Jupyter Notebook";   Filename: "{app}\vendor\python-for-windows\Jupyter Notebook.exe";                         Parameters: ""; WorkingDir: "{userdocs}";    Components: python
Name: "{group}\WinPython\Pyzo (Python IDE)";   Filename: "{app}\vendor\python-for-windows\Pyzo.exe";                       Parameters: ""; WorkingDir: "{userdocs}";    Components: python
//Name: "{group}\WinPython\Spyder (Python IDE)";   Filename: "{app}\vendor\python-for-windows\Spyder.exe";                                  Parameters: ""; WorkingDir: "{userdocs}";    Components: python
Name: "{group}\WinPython\WinPython Command Prompt";   Filename: "{app}\vendor\python-for-windows\WinPython Command Prompt.exe";         Parameters: ""; WorkingDir: "{userdocs}";    Components: python
Name: "{group}\WinPython\WinPython Control Panel";   Filename: "{app}\vendor\python-for-windows\WinPython Control Panel.exe";           Parameters: ""; WorkingDir: "{userdocs}";    Components: python
Name: "{group}\WinPython\WinPython Command Prompt";   Filename: "{app}\vendor\python-for-windows\WinPython Command Prompt.exe";         Parameters: ""; WorkingDir: "{userdocs}";    Components: python
Name: "{group}\WinPython\Qt Designer";   Filename: "{app}\vendor\python-for-windows\Qt Designer.exe";           Parameters: ""; WorkingDir: "{userdocs}";    Components: python
Name: "{group}\WinPython\Qt Linguist";   Filename: "{app}\vendor\python-for-windows\Qt Linguist.exe";           Parameters: ""; WorkingDir: "{userdocs}";    Components: python
#endif
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
#ifdef with_doxygen
Name: "{group}\DoxygenWizard";        Filename: "{app}\vendor\doxygen-for-windows\bin\doxywizard.exe";  Parameters: ""; WorkingDir: "{userdocs}";    Components: doxygen
#endif
#ifdef with_npp
Name: "{group}\Notepad++";        Filename: "{app}\vendor\npp-for-windows\notepad++.exe";  Parameters: ""; WorkingDir: "{userdocs}";    Components: npp
#endif
Name: "{group}\Uninstall @name@";     Filename: "{uninstallexe}"; IconFilename: "{app}\Barbarian.ico"
