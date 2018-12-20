# Building Barbarian

## Requiremens for building Barbarian

Dependencies are defined in the conanfile.py.

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

## Build Variants

### Default, Full, Minimal Builds

You can include and exclude packages. Default is a full build containing all packages except VSCode available.
The options used are:
    * with_git (default True)
    * with_cmake (default True)
    * with_bazel (default True)
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
conan create . user/channel -o with_cmake=False -o with_bazel=False -o with_python=False -o with_conanio=False
```

### Python Flavour

Barbarian can be configured to use [Miniconda3](https://winpython.github.io) instead of [WinPython3](https://conda.io/miniconda.html)

To build with MiniConda3 instead of WinPython3
```
# conan create . user/channel -o python_flavor=MiniConda3
```