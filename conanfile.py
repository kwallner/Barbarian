from conans import ConanFile, tools
from conans.errors import ConanException
from subprocess import call
import os
import shutil

class BarbarianConan(ConanFile):
    name = "Barbarian"
    version = "1.3.6"
    generators = "txt", "virtualenv"
    url = "http://github.com/kwallner/Barbarian"
    scm = { "type": "git", "url": "auto", "revision": "auto" }
    settings = {"os": ["Windows"], "arch": ["x86_64"]}
    exports_sources = [ "LICENSE.txt", "README.md" ]
    no_copy_source = True
    options = {"with_git": [True, False], "with_cmake": [True, False], "with_python": [True, False], "with_conanio": [True, False], "with_vscode": [True, False], "with_vim": [True, False]}
    default_options = "with_git=True", "with_cmake=True", "with_python=True", "with_conanio=True", "with_vscode=False", "with_vim=False"

    def configure(self):
        if self.options.with_conanio and not self.options.with_python:
            raise ConanException("Invalid configuration: Python is required when using Conan.io")

    def build_requirements(self):
        self.build_requires("7z_installer/1.0@conan/stable")

    def source(self):
        tools.download("https://github.com/cmderdev/cmder/releases/download/v1.3.6/cmder_mini.zip", "cmder_mini.zip")
        tools.download("https://github.com/git-for-windows/git/releases/download/v2.18.0.windows.1/PortableGit-2.18.0-64-bit.7z.exe", "git-for-windows.7z.exe")
        tools.download("https://cmake.org/files/v3.12/cmake-3.12.0-win64-x64.zip", "cmake-win64.zip")
        tools.download("https://github.com/winpython/winpython/releases/download/1.10.20180624/WinPython64-3.7.0.1.exe", "python-win64.exe")
        tools.download("https://go.microsoft.com/fwlink/?Linkid=850641", "vscode-win64.zip")
        tools.download("https://ftp.vim.org/pub/vim/pc/gvim81.zip", "vim-win64.zip", verify=False)

    def build(self):
        # 1. Cmder
        tools.unzip(os.path.join(self.source_folder, "cmder_mini.zip"))

        # 2. Git
        if self.options.with_git:
            call(["7z", "x", os.path.join(self.source_folder, "git-for-windows.7z.exe"), "-o%s" % "vendor/git-for-windows" ])

        # 3. CMake
        if self.options.with_cmake:
            tools.unzip(os.path.join(self.source_folder, "cmake-win64.zip"), destination = "vendor")
            os.rename(os.path.join("vendor", "cmake-3.12.0-win64-x64"), os.path.join("vendor", "cmake-for-windows"))

        # 4. Python
        if self.options.with_python:
            call(["7z", "x", os.path.join(self.source_folder, "python-win64.exe"), "-o.", "-ir!python-3.7.0.amd64" ])
            os.rename("python-3.7.0.amd64", os.path.join("vendor", "python-for-windows"))
            # Upgrade pip
            call(["vendor/python-for-windows/python.exe", "-m", "pip", "install", "--upgrade", "pip", "--no-warn-script-location"])

        # 5. Conan.io
        if self.options.with_conanio:
            # If a specific version of conan should be used change "conan" to e.g. "conan==1.4.4"
            call(["vendor/python-for-windows/python.exe", "-m", "pip", "install", "conan", "--no-warn-script-location"])

        # 5. VS Code + Extensions
        if self.options.with_vscode:
            tools.unzip(os.path.join(self.source_folder, "vscode-win64.zip"), destination = "vendor/vscode-for-windows")
            # Some useful extensions
            call(["vendor\\vscode-for-windows\\bin\\code.cmd", "--install-extension", "ms-vscode.cpptools"])
            call(["vendor\\vscode-for-windows\\bin\\code.cmd", "--install-extension", "ms-python.python"])
            call(["vendor\\vscode-for-windows\\bin\\code.cmd", "--install-extension", "MS-CEINTL.vscode-language-pack-de"])
            call(["vendor\\vscode-for-windows\\bin\\code.cmd", "--install-extension", "PeterJausovec.vscode-docker"])
            call(["vendor\\vscode-for-windows\\bin\\code.cmd", "--install-extension", "twxs.cmake"])

        # 6. Vim
        if self.options.with_vim:
            tools.unzip(os.path.join(self.source_folder, "vim-win64.zip"))
            os.rename(os.path.join("vim", "vim81"), os.path.join("vendor", "vim-for-windows"))
            os.rmdir("vim")

        # 7. Configure
        os.system("cmd /C vendor\\init.bat")
        with open(os.path.join("config", "user-profile.cmd"), 'a') as f:
            f.write('\n')
            f.write(':: Start: Customize Section ... automatically addded by Barbarian\n')
            if self.options.with_cmake:
                f.write(':: Vendor: cmake support\n')
                f.write('set "PATH=%CMDER_ROOT%\\vendor\\cmake-for-windows\\bin;%PATH%"\n')
                f.write('\n')
            if self.options.with_python:
                f.write(':: Vendor: python support\n')
                f.write('set "PATH=%CMDER_ROOT%\\vendor\\python-for-windows;%PATH%"\n')
                f.write('set "PATH=%CMDER_ROOT%\\vendor\\python-for-windows\\Scripts;%PATH%"\n')
                f.write('\n')
            if self.options.with_vscode:
                f.write(':: Vendor: vscode support\n')
                f.write('set "PATH=%CMDER_ROOT%\\vendor\\vscode-for-windows;%PATH%"\n')
                f.write('\n')
            if self.options.with_vim:
                f.write(':: Vendor: vim support\n')
                f.write('set "PATH=%CMDER_ROOT%\\vendor\\vim-for-windows;%PATH%"\n')
                f.write('\n')
            f.write(':: Done: Customize Section ... automatically addded by Barbarian\n')
            f.write('\n')

        # 8. Install
        shutil.copytree(os.path.join(self.build_folder, 'bin'), os.path.join(self.package_folder, 'bin'))
        shutil.copytree(os.path.join(self.build_folder, 'config'), os.path.join(self.package_folder, 'config'))
        shutil.copytree(os.path.join(self.build_folder, 'icons'), os.path.join(self.package_folder, 'icons'))
        shutil.copytree(os.path.join(self.build_folder, 'vendor'), os.path.join(self.package_folder, 'vendor'))
        shutil.copyfile(os.path.join(self.build_folder, 'Cmder.exe'), os.path.join(self.package_folder, 'Cmder.exe'))


    def package(self):
        #  Copy plain files
        self.copy("README.md")
        self.copy("LICENSE.txt")
        self.copy("activate.bat")
        self.copy("activate.ps1")
        self.copy("deactivate.bat")
        self.copy("deactivate.ps1")

    def package_info(self):
        if self.options.with_cmake:
            self.env_info.path.insert(0, os.path.join(self.package_folder, "cmake-for-windows", "bin"))
        if self.options.with_python:
            self.env_info.path.insert(0, os.path.join(self.package_folder, "python-for-windows"))
            self.env_info.path.insert(0, os.path.join(self.package_folder, "python-for-windows", "Scripts"))
        if self.options.with_vscode:
            self.env_info.path.insert(0, os.path.join(self.package_folder, "vscode-for-windows"))
        if self.options.with_vim:
            self.env_info.path.insert(0, os.path.join(self.package_folder, "vim-for-windows"))
        self.env_info.path.insert(0, os.path.join(self.package_folder, "bin"))
        self.env_info.path.insert(0, self.package_folder)
