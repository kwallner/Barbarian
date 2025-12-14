# Building Barbarian

## Requiremens for building Barbarian

Dependencies are defined in the conanfile.py:

### 7zip

Build instructions:
````shell
git clone https://github.com/kwallner/conan-7zip.git
cd conan-7zip
conan create --user kwallner --channel testing .
````


### InnoSetup

Build instructions:
````shell
git clone https://github.com/kwallner/conan-InnoSetup.git
cd conan-InnoSetup
conan create --user kwallner --channel testing .
````

## Build your own Barbarian

Build instructions:
````shell
git clone https://github.com/kwallner/Barbarian.git
cd Barbarian
conan create --user kwallner --channel testing .
````