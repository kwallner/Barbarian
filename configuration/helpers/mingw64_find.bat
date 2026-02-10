:: Copyright 2026 - Karl Wallner 

@echo OFF
set Mingw64Path=C:\mingw64
if not exist "%Mingw64Path%" goto :no-mingw64
set PATH=%Mingw64Path%\bin;%PATH%
exit /b 0
)
:no-mingw64
endlocal
exit /B 1
