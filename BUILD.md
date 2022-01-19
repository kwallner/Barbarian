# Building Barbarian

## Requiremens for building Barbarian

Dependencies are defined in the conanfile.py:

### 7zip

````
self.build_requires("7zip/19.0")
````

Taken from [Conan-Center](https://conan.io/center/).

### InnoSetup

````
self.build_requires("InnoSetup/6.0.5@%s/%s" % (self.user, self.channel))
````

Build instructions:
````shell
git clone https://github.com/kwallner/conan-InnoSetup.git
cd conan-InnoSetup
conan create . kwallner/testing
````

### cpython

````
self.build_requires("cpython/%s@%s/%s" % (self._python_version, self.user, self.channel))
````

Build instructions:
Visual Studio 2017 is required to build python.

Profile:
````
[settings]
arch=x86_64
arch_build=x86_64
build_type=Release
compiler=Visual Studio
compiler.runtime=MD
compiler.version=15
os=Windows
````

````shell
git clone https://github.com/kwallner/conan-cpython.git
conan create . kwallner/testing
````


## Build your own Barbarian

Build instructions:
```shell
git clone https://github.com/kwallner/Barbarian.git
cd Barbarian
conan create . kwallner/testing 
```