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
    * with_cmake (default True)
    * with_kdiff3 (default False)
    * with_gitext (default False)
    * with_npp (default False)
Additional variant options:
    * conanio_variant (default "pip")
      "pip": Use python integrated conan, installed with pip
      "standalone": Use standalone conan, installed using installer
    
To build full version:
```
conan create . user/channel -o with_kdiff3=True -o with_winmerge=True -o with_gitext=True -o with_npp=True
```

To build a minimal version
```
conan create . user/channel -o with_cmake=False
```


## Current Build commands

```
conan create . kwallner/testing -o with_kdiff3=True -o with_winmerge=True -o with_gitext=True -o with_npp=True
conan create . kwallner/testing -o with_cmake=False
conan create . kwallner/testing 
```