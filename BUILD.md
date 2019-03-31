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
    * with_bazel (default False)
    * with_python (default True)
    * with_conanio (default True)
    * with_vscode (default False)
    * with_kdiff3 (default False)
    * with_gitext (default False)
    * with_graphviz (default False)
    * with_doxygen (default False)
    * with_miktex (default False)
    * with_ninja (default False)
    * with_npp (default False)
    * with_pandoc (default False)
    * with_ruby (default False)
    
To build with VSCode and KDiff3 and GitExtensions
```
# conan create . user/channel -o with_bazel=True -o with_vscode=True -o with_kdiff3=True -o with_winmerge=True -o with_gitext=True -o with_graphviz=True -o with_doxygen=True -o with_miktex=True -o with_ninja=True -o with_npp=True -o with_pandoc=True -o with_Ruby=True
```

To build a minimal version
```
conan create . user/channel -o with_cmake=False -o with_python=False -o with_conanio=False
```
