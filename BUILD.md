# Building Barbarian

## Requiremens for building Barbarian

Dependencies are defined in the conanfile.py:

### 7zip

Taken from [Conan-Center](https://conan.io/center/). No need to do anything.

### InnoSetup

Build instructions:
````shell
git clone https://github.com/kwallner/conan-InnoSetup.git
cd conan-InnoSetup
conan create . kwallner/testing
````

## Build your own Barbarian

Build instructions:
````shell
git clone https://github.com/kwallner/Barbarian.git
cd Barbarian
conan create . kwallner/testing 
````