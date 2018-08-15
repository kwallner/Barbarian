[Setup]
AppName=@name@
AppVerName=@name@ @version@
AppPublisher=@author@
AppPublisherURL=@url@
AppSupportURL=@url@
AppUpdatesURL=@url@
ArchitecturesInstallIn64BitMode=x64
ArchitecturesAllowed=x64
DefaultDirName={pf}\@name@
DefaultGroupName=@name@
Compression=lzma2
OutputDir=.
OutputBaseFilename=@name@-@version@

[Components]
Name: with_git;                                             Description: "Install Git (https://git-scm.com)";                             Types: full compact custom
Name: with_cmake;                                           Description: "Install CMake (https:://cmake.org)";                            Types: full custom
Name: with_python;                                          Description: "Install Python and Conan.io (https:://conan.io)";               Types: full custom
//Name: with_vscode;                                          Description: "Install Visual Studio Code (https://code.visualstudio.com)";    Types: full 
Name: with_kdiff3;                                          Description: "Install KDiff3 (http://kdiff3.sourceforge.net)";                Types: full 
Name: with_gitext;                                          Description: "Install GitExtensions (http://gitextensions.github.io)";        Types: full 

[Files]
Source: "@name@\Cmder.exe";                                DestDir: "{app}";                                           Flags: ignoreversion 
Source: "@name@\LICENSE.txt";                              DestDir: "{app}";                                           Flags: ignoreversion 
Source: "@name@\README.md";                                DestDir: "{app}";                                           Flags: ignoreversion isreadme
Source: "@name@\bin\*";                                    DestDir: "{app}\bin";                                       Flags: recursesubdirs ignoreversion
Source: "@name@\config\ConEmu.xml";                        DestDir: "{app}\config\ConEmu.xml";                         Flags: ignoreversion
Source: "@name@\config\Readme.md";                         DestDir: "{app}\config\Readme.md";                          Flags: ignoreversion
Source: "@name@\config\profile.d\cmake-for-windows.cmd";   DestDir: "{app}\config\profile.d\cmake-for-windows.cmd";    Flags: ignoreversion;    Components: with_cmake 
Source: "@name@\config\profile.d\gitext-for-windows.cmd";  DestDir: "{app}\config\profile.d\gitext-for-windows.cmd";   Flags: ignoreversion;    Components: with_gitext 
Source: "@name@\config\profile.d\kdiff3-for-windows.cmd";  DestDir: "{app}\config\profile.d\kdiff3-for-windows.cmd";   Flags: ignoreversion;    Components: with_kdiff3 
Source: "@name@\config\profile.d\python-for-windows.cmd";  DestDir: "{app}\config\profile.d\python-for-windows.cmd";   Flags: ignoreversion;    Components: with_python 
//Source: "@name@\config\profile.d\vscode-for-windows.cmd";  DestDir: "{app}\config\profile.d\vscode-for-windows.cmd";   Flags: ignoreversion;    Components: with_vscode 
Source: "@name@\icons\*";                                  DestDir: "{app}\icons";                                     Flags: recursesubdirs ignoreversion
Source: "@name@\vendor\Readme.md";                         DestDir: "{app}\vendor\Readme.md";                          Flags: ignoreversion 
Source: "@name@\vendor\clink.lua";                         DestDir: "{app}\vendor\clink.lua";                          Flags: ignoreversion 
Source: "@name@\vendor\init.bat";                          DestDir: "{app}\vendor\init.bat";                           Flags: ignoreversion 
Source: "@name@\vendor\profile.ps1";                       DestDir: "{app}\vendor\profile.ps1";                        Flags: ignoreversion 
Source: "@name@\vendor\sources.json";                      DestDir: "{app}\vendor\sources.json";                       Flags: ignoreversion 
Source: "@name@\vendor\user-aliases.cmd.example";          DestDir: "{app}\vendor\user-aliases.cmd.example";           Flags: ignoreversion 
Source: "@name@\vendor\clink\*";                           DestDir: "{app}\vendor\clink";                              Flags: recursesubdirs ignoreversion;  
Source: "@name@\vendor\clink-completions\*";               DestDir: "{app}\vendor\clink-completions";                  Flags: recursesubdirs ignoreversion;  
Source: "@name@\vendor\cmake-for-windows\*";               DestDir: "{app}\vendor\cmake-for-windows";                  Flags: recursesubdirs ignoreversion;    Components: with_cmake  
Source: "@name@\vendor\conemu-maximus5\*";                 DestDir: "{app}\vendor\conemu-maximus5";                    Flags: recursesubdirs ignoreversion;  
Source: "@name@\vendor\git-for-windows\*";                 DestDir: "{app}\vendor\git-for-windows";                    Flags: recursesubdirs ignoreversion;    Components: with_git  
Source: "@name@\vendor\gitext-for-windows\*";              DestDir: "{app}\vendor\gitext-for-windows";                 Flags: recursesubdirs ignoreversion;    Components: with_gitext   
Source: "@name@\vendor\kdiff3-for-windows\*";              DestDir: "{app}\vendor\kdiff3-for-windows";                 Flags: recursesubdirs ignoreversion;    Components: with_kdiff3 
Source: "@name@\vendor\lib\*";                             DestDir: "{app}\vendor\lib";                                Flags: recursesubdirs ignoreversion;  
Source: "@name@\vendor\psmodules\*";                       DestDir: "{app}\vendor\psmodules";                          Flags: recursesubdirs ignoreversion;     
Source: "@name@\vendor\python-for-windows\*";              DestDir: "{app}\vendor\python-for-windows";                 Flags: recursesubdirs ignoreversion;    Components: with_python;    Excludes: "__pycache__"
// FIXME: Can not pack VSCode ... does not work !!!
//Source: "@name@\vendor\vscode-for-windows\*";            DestDir: "{app}\vendor\vscode-for-windows";                 Flags: recursesubdirs ignoreversion;    Components: with_vscode  

[Icons]
Name: "{group}\Cmder";                Filename: "{app}\Cmder.exe";                                    Parameters: ""; WorkingDir: "{app}"
//Name: "{group}\Visual Studio Code";   Filename: "{app}\vendor\vscode-for-windows\Code.exe";           Parameters: ""; WorkingDir: "{app}";    Components: with_vscode
Name: "{group}\KDiff3";               Filename: "{app}\vendor\kdiff3-for-windows\kdiff3.exe";         Parameters: ""; WorkingDir: "{app}";    Components: with_kdiff3
Name: "{group}\GitExtensions";        Filename: "{app}\vendor\gitext-for-windows\GitExtensions.exe";  Parameters: ""; WorkingDir: "{app}";    Components: with_gitext
