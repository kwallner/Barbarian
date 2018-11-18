:: Copyright 2017 - Refael Ackermann (Original Author)
:: Copyright 2018 - Karl Wallner (Changed)
:: Distributed under MIT style license
:: See accompanying file LICENSE at https://github.com/node4good/windows-autoconf
:: version: 2.0.0

@echo OFF
set InstallerPath=%ProgramFiles(x86)%\Microsoft Visual Studio\Installer
if not exist "%InstallerPath%" set InstallerPath=%ProgramFiles%\Microsoft Visual Studio\Installer
if not exist "%InstallerPath%" goto :no-vswhere
set PATH=%InstallerPath%;%PATH%
for /F "tokens=* USEBACKQ" %%i in (`vswhere.exe -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath -version "[15.0, 16.0)"`) do (
set VS150COMNTOOLS=%%i\Common7\Tools\
exit /b 0
)
:no-vswhere
endlocal
exit /B 1
