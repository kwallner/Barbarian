# <font color="red">Work in Progress</font>

# Barbarian - A Software Development Environment for Conan.io

Barbarian is an all in one package for everybody developing software with:
* [Conan.io](https:://conan.io):  C/C++ Package Manager
* [CMake](https:://cmake.org): Cross-Plattform Build System
* [Git](https://git-scm.com): Distributed version control system

Barbarian is based on:
* [Cmder](http://cmder.net/): Console emulator for Windows

Barbarian also contains:
* [WinPython](https://winpython.github.io): Python-distribution for Windows platform
* [Visual Studio Code](https://code.visualstudio.com): IDE and Code Editor
* [Vim](https://www.vim.org): vi Text Editor

*Barbarian brings all you need to start with conan.io, cmake and git contained in a single installation package.*

## Naming of Barbarian

[Conan](https:://conan.io) is also the principal character in [Conan the Barbarian](https://www.imdb.com/title/tt0082198/).

## Install Barbarian

Not yet done.

TODO: Should provide zip-files.

Unzip the Bavarian installation zip-file.

## Using Barbarian

Start the program (executable) ```Cmder.exe``` located in the root directory of the zip file.

## Build your own Barbarian

Barbarian provides a flexible basis to create a customized development environment.

To build barbarian you already need a build environment like barbarian, at least conan.io and git installed.

First clone the repository
```
# git clone https://github.com/kwallner/Barbarian.git
```

Change directory
```
# cd Barbarian
```

And build it
```
# conan create . user/channel
```

You can include and exclude packages. Default is a full build containing all packages except VSCode available.
The options used are:
    * with_git (default True)
    * with_cmake (default True)
    * with_python (default True)
    * with_conanio (default True)
    * with_vscode (default False)
    * with_vim (default False)

To build with VSCode and VI included use
```
# conan create . user/channel -o with_vscode=True -o with_vim=True
```
