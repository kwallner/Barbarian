# <font color="red">Work in Progress</font>

# Barbarian - A Software Development Environment for Conan.io

Barbarian is an all in one package for everybody developing software with:
* [Conan.io](https:://conan.io):  C/C++ Package Manager
* [CMake](https:://cmake.org): Cross-Plattform Build System
* [Git](https://git-scm.com): Distributed version control system

Barbarian is based on:
* [Cmder](http://cmder.net/): Console emulator for Windows

Barbarian also contains:
* [Miniconda3](https://conda.io/miniconda.html): Python-distribution for Windows platform
* [WinPython3](https://winpython.github.io): Python-distribution for Windows platform
* [Visual Studio Code](https://code.visualstudio.com): IDE and Code Editor
* [KDiff3](http://kdiff3.sourceforge.net): Diff and Merge Tool
* [WinMerge](http://winmerge.org): Diff and Merge Tool
* [GitExtension](http://gitextensions.github.io): Graphical User Interface for Git

Barbarian can be configured to
* Use [Miniconda3](https://conda.io/miniconda.html) instead of [WinPython3](https://winpython.github.io)

*Barbarian brings all you need to start with conan.io, cmake and git contained in a single installation package.*

## Naming of Barbarian

[Conan](https:://conan.io) is also the principal character in [Conan the Barbarian](https://www.imdb.com/title/tt0082198/).

## Install Barbarian

Barbarian is delivered as installer. This installer does not require admin priviledges and is installable as user.

Building the installer required [InnoSetup](http://www.jrsoftware.org/isinfo.php).

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
    * with_kdiff3 (default False)
    * with_gitext (default False)

To build with VSCode and KDiff3 and GitExtensions
```
# conan create . user/channel -o with_vscode=True -o with_kdiff3=True -o with_winmerge=True -o with_gitext=True
```

To build a minimal version
```
conan create . user/channel -o with_git=False -o with_cmake=False -o with_python=False -o with_conanio=False
```

To build with WinPython3 instead of Miniconda3
```
# conan create . user/channel -o python_flavor=WinPython3
```
