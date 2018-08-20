from conans import ConanFile, tools
from conans.errors import ConanException
from subprocess import call
import os
import shutil
import pathlib

class BarbarianConan(ConanFile):
    name = "Barbarian"
    version = "1.3.6"
    cmder_version = "1.3.6"
    git_version = "2.18.0"
    cmake_version = "3.12.1"
    winpython3_version = "3.7.0.1"
    miniconda3_version = "4.5.4"
    conan_version = "1.6.1"
    vscode_version = "1.26.0"
    kdiff_version = "0.9.98"
    winmerge_version = "2.14.0"
    gitext_version = "2.51.04"
    generators = "txt"
    url = "http://github.com/kwallner/Barbarian"
    author = "Karl Wallner <kwallner@mail.de>"
    license = "https://raw.githubusercontent.com/kwallner/Barbarian/develop/LICENSE.txt"
    description = "Software Development Environment for Conan.io"
    settings = {"os": ["Windows"], "arch": ["x86_64"]}
    exports_sources = [ "LICENSE.txt", "README.txt",  "README.md", "packaging/package.iss" ]
    no_copy_source = True
    short_paths = True
    options = {"with_git": [True, False], "with_cmake": [True, False], "with_python": [True, False], "with_conanio": [True, False], "with_vscode": [True, False], "with_kdiff3": [True, False], "with_winmerge": [True, False], "with_gitext": [True, False], "python_flavor": [ "WinPython3", "MiniConda3" ]}
    default_options = "with_git=True", "with_cmake=True", "with_python=True", "with_conanio=True", "with_vscode=False", "with_kdiff3=False", "with_winmerge=False", "with_gitext=False", "python_flavor=MiniConda3"

    @property
    def installertype_set(self):
        if self.options.with_git and self.options.with_cmake and self.options.with_python and self.options.with_conanio and self.options.with_vscode and self.options.with_kdiff3 and self.options.with_winmerge and self.options.with_gitext:
            return "full"
        if not self.options.with_git and not self.options.with_cmake and not self.options.with_python and not self.options.with_conanio and not self.options.with_vscode and not self.options.with_kdiff3 and not self.options.with_winmerge and not self.options.with_gitext:
            return "minimal"
        if self.options.with_git and self.options.with_cmake and self.options.with_python and self.options.with_conanio and not self.options.with_vscode and not self.options.with_kdiff3 and not self.options.with_winmerge and not self.options.with_gitext:
            return "default"
        return "custom"

    @property
    def installertype(self):
        if self.options.python_flavor == "MiniConda3":
            return self.installertype_set
        else:
            return "%s+%s" % (self.installertype_set, self.options.python_flavor)

    def configure(self):
        if self.options.with_conanio and not self.options.with_python:
            raise ConanException("Invalid configuration: Python is required when using Conan.io")

    def build_requirements(self):
        self.build_requires("7z_installer/1.0@conan/stable")
        self.build_requires("InnoSetup/5.6.1@kwallner/testing")

    def source(self):
        tools.download("https://github.com/cmderdev/cmder/releases/download/v%s/cmder_mini.zip" % (self.cmder_version), "cmder_mini.zip")
        tools.download("https://github.com/git-for-windows/git/releases/download/v%s.windows.1/PortableGit-%s-64-bit.7z.exe" % (self.git_version, self.git_version), "git-for-windows.7z.exe")
        tools.download("https://cmake.org/files/v%s.%s/cmake-%s-win64-x64.zip" % (self.cmake_version.split(".")[0], self.cmake_version.split(".")[1], self.cmake_version), "cmake-win64.zip")
        tools.download("https://github.com/winpython/winpython/releases/download/1.10.20180624/WinPython64-%s.exe" % (self.winpython3_version), "winpython3-win64.exe")
        tools.download("https://repo.continuum.io/miniconda/Miniconda3-%s-Windows-x86_64.exe" % (self.miniconda3_version), "miniconda3-win64.exe")
        tools.download("https://go.microsoft.com/fwlink/?Linkid=850641", "vscode-win64.zip")
        tools.download("https://datapacket.dl.sourceforge.net/project/kdiff3/kdiff3/%s/KDiff3-64bit-Setup_%s-2.exe" % (self.kdiff_version, self.kdiff_version), "kdiff3-win64.exe")
        tools.download("https://datapacket.dl.sourceforge.net/project/winmerge/stable/%s/WinMerge-%s-exe.zip" % (self.winmerge_version, self.winmerge_version), "winmerge.exe.zip")
        tools.download("https://github.com/gitextensions/gitextensions/releases/download/v%s/GitExtensions-%s.msi" % (self.gitext_version, self.gitext_version), "gitext.exe")

    def build(self):
        # 0. Cmder
        tools.unzip(os.path.join(self.source_folder, "cmder_mini.zip"), destination = self.name)
        os.remove(os.path.join(self.build_folder, self.name, "LICENSE"))

        # 1. Create profile directory
        tools.mkdir(os.path.join(self.build_folder, self.name, "config", "profile.d"))
        shutil.copyfile(os.path.join(self.source_folder, "LICENSE.txt"), os.path.join(self.build_folder, self.name,"LICENSE.txt"))
        shutil.copyfile(os.path.join(self.source_folder, "README.txt"), os.path.join(self.build_folder, self.name,"README.txt"))
        shutil.copyfile(os.path.join(self.source_folder, "README.md"), os.path.join(self.build_folder, self.name,"README.md"))

        # 2. Git
        if self.options.with_git:
            call(["7z", "x", os.path.join(self.source_folder, "git-for-windows.7z.exe"), "-o%s/%s" % (self.name, "vendor/git-for-windows") ])
            # No need for install script. Git is already included (so do not change name)

        # 3. CMake
        if self.options.with_cmake:
            tools.unzip(os.path.join(self.source_folder, "cmake-win64.zip"), destination = os.path.join(self.name, "vendor"))
            os.rename(os.path.join(self.name, "vendor", "cmake-%s-win64-x64" % (self.cmake_version)), os.path.join(self.name, "vendor", "cmake-for-windows"))
            # Create install script
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "cmake-for-windows.cmd"), 'w') as f:
                f.write(':: Vendor: cmake support\n')
                path = os.path.join("%CMDER_ROOT%", "vendor", "cmake-for-windows", "bin")
                f.write('set "PATH={0};%PATH%"\n'.format(path))

        # 4. Python
        if self.options.with_python:
            if self.options.python_flavor == "MiniConda3":
                #call([os.path.join(self.source_folder, "miniconda3-win64.exe"), "/InstallationType=JustMe", "/RegisterPython=0", "/S", "/AddToPath=0", "/D=%s" % (os.path.join(self.build_folder, self.name, "vendor", "python-for-windows")) ])
                call([os.path.join(self.source_folder, "miniconda3-win64.exe"), "/InstallationType=JustMe", "/RegisterPython=0", "/S", "/AddToPath=0", "/D=%s" % (pathlib.PureWindowsPath(self.build_folder, self.name, "vendor", "python-for-windows")) ])
            elif self.options.python_flavor == "WinPython3":
                call(["7z", "x", os.path.join(self.source_folder, "winpython3-win64.exe"), "-o.", "-ir!python-3.7.0.amd64" ])
                os.rename("python-3.7.0.amd64", os.path.join(self.name, "vendor", "python-for-windows"))
            else:
                raise ConanException("Invalid python flavor \"%s\"" % self.options.python_flavor)
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "python-for-windows.cmd"), 'w') as f:
                f.write(':: Vendor: python support\n')
                path = os.path.join("%CMDER_ROOT%", "vendor", "python-for-windows")
                f.write('set "PATH={0};%PATH%"\n'.format(path))
                path = os.path.join("%CMDER_ROOT%", "vendor", "python-for-windows", "Scripts")
                f.write('set "PATH={0};%PATH%"\n'.format(path))

        # 5. Conan.io
        if self.options.with_conanio:
            call(["%s/vendor/python-for-windows/python.exe" % self.name, "-m", "pip", "install", "conan==%s" % self.conan_version, "--no-warn-script-location"])
            # No install script needed ... installed with python

        # 6. VS Code + Extensions
        if self.options.with_vscode:
            tools.unzip(os.path.join(self.source_folder, "vscode-win64.zip"), destination = os.path.join(self.name, "vendor", "vscode-for-windows"))
            # Some useful extensions
            old = os.getcwd()
            os.chdir(os.path.join(self.name, "vendor", "vscode-for-windows", "bin"))
            call(["code.cmd", "--install-extension", "ms-vscode.cpptools"])
            call(["code.cmd", "--install-extension", "ms-python.python"])
            call(["code.cmd", "--install-extension", "MS-CEINTL.vscode-language-pack-de"])
            call(["code.cmd", "--install-extension", "PeterJausovec.vscode-docker"])
            call(["code.cmd", "--install-extension", "twxs.cmake"])
            call(["code.cmd", "--install-extension", "vector-of-bool.cmake-tools"])
            os.chdir(old)
            # Create install script
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "vscode-for-windows.cmd"), 'w') as f:
                f.write(':: Vendor: vscode support\n')
                path = os.path.join("%CMDER_ROOT%", "vendor", "vscode-for-windows", "bin")
                f.write('set "PATH={0};%PATH%"\n'.format(path))

        # 7. KDiff
        if self.options.with_kdiff3:
            call(["7z", "x", os.path.join(self.source_folder, "kdiff3-win64.exe"), "-o%s/%s" % (self.name, "vendor/kdiff3-for-windows"), '-x!$PLUGINSDIR', '-x!Uninstall.exe' ])
            # Create install script
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "kdiff3-for-windows.cmd"), 'w') as f:
                f.write(':: Vendor: kdiff3 support\n')
                path = os.path.join("%CMDER_ROOT%", "vendor", "kdiff3-for-windows")
                f.write('set "PATH={0};%PATH%"\n'.format(path))

        # 8. WinMerge
        if self.options.with_winmerge:
            tools.unzip(os.path.join(self.source_folder, "winmerge.exe.zip"))
            os.rename("WinMerge-%s-exe" % self.winmerge_version, os.path.join(self.name, "vendor", "winmerge-for-windows"))
            tools.mkdir(os.path.join(self.build_folder, self.name, "vendor", "winmerge-for-windows", "bin"))
            # Create run script
            with open(os.path.join(self.build_folder, self.name, "vendor", "winmerge-for-windows", "bin", "winmerge.cmd"), 'w') as f:
                f.write('@echo off\n')
                f.write('call "%~dp0..\\WinMergeU.exe" %*\n')
            # Create install script
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "winmerge-for-windows.cmd"), 'w') as f:
                f.write(':: Vendor: winmerge support\n')
                path = os.path.join("%CMDER_ROOT%", "vendor", "winmerge-for-windows", "bin")
                f.write('set "PATH={0};%PATH%"\n'.format(path))

        # 9. GitExt
        if self.options.with_gitext:
            call(["7z", "x", os.path.join(self.source_folder, "gitext.exe"), "-o%s/%s" % (self.name, "vendor/gitext-for-windows") ])
            tools.mkdir(os.path.join(self.build_folder, self.name, "vendor", "gitext-for-windows", "bin"))
            # Create run script
            with open(os.path.join(self.build_folder, self.name, "vendor", "gitext-for-windows", "bin", "gitext.cmd"), 'w') as f:
                f.write('@echo off\n')
                f.write('call "%~dp0..\\GitExtensions.exe" %*\n')
            # Create install script
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "gitext-for-windows.cmd"), 'w') as f:
                f.write(':: Vendor: gitext support\n')
                path = os.path.join("%CMDER_ROOT%", "vendor", "gitext-for-windows", "bin")
                f.write('set "PATH={0};%PATH%"\n'.format(path))

        # 10. Pack it: ZIP-File
        call(["7z", "a", os.path.join(self.package_folder, "%s-%s-%s-%s.zip" % (self.name, self.version, self.settings.arch, self.installertype)), self.name])

        # 11. Installer file: EXE-File
        shutil.copyfile(os.path.join(self.source_folder, "packaging", "package.iss"), "package.iss")
        tools.replace_in_file("package.iss", '@name@', self.name)
        tools.replace_in_file("package.iss", '@version@', self.version)
        tools.replace_in_file("package.iss", '@author@', self.author)
        tools.replace_in_file("package.iss", '@url@', self.url)
        tools.replace_in_file("package.iss", '@conan_version@', self.conan_version)
        iscc_command= ["iscc", "/Q"]
        if self.options.with_git:
            iscc_command.append("/Dwith_git")
        if self.options.with_cmake:
            iscc_command.append("/Dwith_cmake")
        if self.options.with_python:
            iscc_command.append("/Dwith_python")
        if self.options.with_conanio:
            iscc_command.append("/Dwith_conanio")
        if self.options.with_vscode:
            iscc_command.append("/Dwith_vscode")
        if self.options.with_kdiff3:
            iscc_command.append("/Dwith_kdiff3")
        if self.options.with_winmerge:
            iscc_command.append("/Dwith_winmerge")
        if self.options.with_gitext:
            iscc_command.append("/Dwith_gitext")
        iscc_command.append("package.iss")
        call(iscc_command)
        shutil.move("%s-%s.exe" % (self.name, self.version), os.path.join(self.package_folder, "%s-%s-%s-%s.exe" % (self.name, self.version, self.settings.arch, self.installertype)) )
