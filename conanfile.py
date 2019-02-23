from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration
from subprocess import call
import os
import shutil
import jinja2
from datetime import datetime

class VsToolVersion:
    def __init__(self, name, modified, build, Name, CommonToolsEnv, Architecture):
        self.name = name
        self.modified = modified
        self.build = build
        self.Name = Name
        self.GuiArgs = " /icon \"%" + CommonToolsEnv + "%\\..\\IDE\\devenv.exe\""
        extra_call = ""
        extra_path= ""
        if CommonToolsEnv == "VS150COMNTOOLS":
            extra_call = "call \"%ConEmuDir%\\..\\barbarian-extra\\vswhere_find_vs2017.bat\" &amp; "
            extra_path = "Auxiliary\\Build\\"
        self.Cmd1 = extra_call + "call \"%" + CommonToolsEnv + "%..\\..\\VC\\" + extra_path + "vcvarsall.bat\" " + Architecture + " &amp; cmd /k \"\"%ConEmuDir%\\..\\init.bat\"\"" 
        self.Count = "1"
        self.Hotkey = "0"
        self.Flags = "0"
        self.Active = "1"
        
class BarbarianConan(ConanFile):
    name = "Barbarian"
    version = "1.7.0"
    _cmder_version = "1.3.11"
    _cmder_version_build = "%s.843" % _cmder_version
    _git_version = "2.20.1"
    _cmake_version = "3.13.4"
    _bazel_version = "0.22.0"
    _winpython3_version = "3.7.2.0"
    _conan_version = "1.12.3"
    _openpyxl_version = "2.6.0"
    _vscode_version = "1.31.1"
    _kdiff_version = "0.9.98"
    _winmerge_version = "2.16.0"
    _gitext_version = "3.0.2"
    _gitext_version_build = "%s.5232" % _gitext_version
    _graphviz_version = "2.38"
    _doxygen_version = "1.8.15"
    _miktex_version = "2.9.6942"
    _ninja_version = "1.9.0"
    _conemu_xml_creation_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _conemu_xml_buildnummer = "180318"
    generators = "txt"
    url = "http://github.com/kwallner/Barbarian"
    author = "Karl Wallner <kwallner@mail.de>"
    license = "https://raw.githubusercontent.com/kwallner/Barbarian/develop/LICENSE.txt"
    description = "Software Development Environment for Conan.io"
    settings = {"os": ["Windows"], "arch": ["x86_64"]}
    scm = { "type": "git", "url": "auto", "revision": "auto" }
    no_copy_source = True
    short_paths = True
    options = {"with_git": [True, False], "with_cmake": [True, False], "with_bazel": [True, False], "with_python": [True, False], "with_conanio" : [True, False], "with_vscode" : [True, False], "with_kdiff3" : [True, False], "with_winmerge" : [True, False], "with_gitext" : [True, False], "with_graphviz" : [True, False], "with_doxygen" : [True, False], "with_miktex" : [True, False], "with_ninja" : [True, False]}
    default_options = {"with_git": True, "with_cmake" : True, "with_bazel" : False, "with_python" : True, "with_conanio" : True, "with_vscode" : False, "with_kdiff3" : False, "with_winmerge" : False, "with_gitext" : False, "with_graphviz" : False, "with_doxygen" : False, "with_miktex" : False, "with_ninja" : False}

    @property
    def _installertype_set(self):
        if self.options.with_git and self.options.with_cmake and self.options.with_bazel and self.options.with_python and self.options.with_conanio and self.options.with_vscode and self.options.with_kdiff3 and self.options.with_winmerge and self.options.with_gitext and self.options.with_graphviz and self.options.with_doxygen and self.options.with_miktex and self.options.with_ninja:
            return "full"
        if self.options.with_git and not self.options.with_cmake and not self.options.with_bazel and not self.options.with_python and not self.options.with_conanio and not self.options.with_vscode and not self.options.with_kdiff3 and not self.options.with_winmerge and not self.options.with_gitext and not self.options.with_graphviz and not self.options.with_doxygen and not self.options.with_miktex and not self.options.with_ninja:
            return "minimal"
        if self.options.with_git and self.options.with_cmake and self.options.with_bazel and self.options.with_python and self.options.with_conanio and not self.options.with_vscode and not self.options.with_kdiff3 and not self.options.with_winmerge and not self.options.with_gitext and not self.options.with_graphviz and not self.options.with_doxygen and not self.options.with_miktex and not self.options.with_ninja:
            return "default"
        return "custom"

    @property
    def _installertype(self):
        return self._installertype_set
            
    def configure(self):
        if self.options.with_conanio and not self.options.with_python:
            raise ConanInvalidConfiguration("Invalid configuration: Python is required when using Conan.io")

    def build_requirements(self):
        self.build_requires("7z_installer/1.0@conan/stable")
        self.build_requires("InnoSetup/5.6.1@kwallner/testing")
        if self.options.with_python:
            self.build_requires("InnoSetupUnpacker/0.47@kwallner/testing")
                
    def source(self):
        tools.download("https://github.com/cmderdev/cmder/releases/download/v%s/cmder_mini.zip" % (self._cmder_version), "cmder_mini.zip")
        if self.options.with_git:
            tools.download("https://github.com/git-for-windows/git/releases/download/v%s.windows.1/PortableGit-%s-64-bit.7z.exe" % (self._git_version, self._git_version), "git-for-windows.7z.exe")
        if self.options.with_cmake:
            tools.download("https://cmake.org/files/v%s.%s/cmake-%s-win64-x64.zip" % (self._cmake_version.split(".")[0], self._cmake_version.split(".")[1], self._cmake_version), "cmake-win64.zip")
        if self.options.with_bazel:
            tools.download("https://github.com/bazelbuild/bazel/releases/download/%s/bazel-%s-windows-x86_64.zip" % (self._bazel_version, self._bazel_version), "bazel-win64.zip")
            tools.download("https://raw.githubusercontent.com/bazelbuild/bazel/master/LICENSE", "bazel-LICENSE.txt")
        if self.options.with_python:
            tools.download("https://github.com/winpython/winpython/releases/download/1.11.20181031/WinPython64-%s.exe" % (self._winpython3_version), "winpython3-win64.exe")
            tools.download("https://raw.githubusercontent.com/winpython/winpython/master/LICENSE", "winpython3-LICENSE.txt")
            tools.download("https://raw.githubusercontent.com/python/cpython/master/LICENSE", "cpython-LICENSE.txt")
            tools.download("https://bitbucket.org/openpyxl/openpyxl/raw/1234131eb33fc7191a554afdd092ee368f7b1fc9/LICENCE.rst", "openpyxl-LICENSE.txt")
        if self.options.with_conanio:
            tools.download("https://raw.githubusercontent.com/conan-io/conan/develop/LICENSE.md", "conanio-LICENSE.txt")
        if self.options.with_vscode:
            tools.download("https://go.microsoft.com/fwlink/?Linkid=850641", "vscode-win64.zip")
        if self.options.with_kdiff3:
            tools.download("https://datapacket.dl.sourceforge.net/project/kdiff3/kdiff3/%s/KDiff3-64bit-Setup_%s-2.exe" % (self._kdiff_version, self._kdiff_version), "kdiff3-win64.exe")
        if self.options.with_winmerge:
            tools.download("https://datapacket.dl.sourceforge.net/project/winmerge/stable/%s/winmerge-%s-x64-exe.zip" % (self._winmerge_version, self._winmerge_version), "winmerge-win64.exe.zip")
            tools.download("https://bitbucket.org/winmerge/winmerge/raw/c1164661fef83403f91e93e4919801b3e7804df3/Docs/Users/GPL.rtf.txt", "winmerge-LICENSE.txt")
        if self.options.with_gitext:
            tools.download("https://github.com/gitextensions/gitextensions/releases/download/v%s/GitExtensions-%s.msi" % (self._gitext_version, self._gitext_version_build), "gitext.exe")
            tools.download("https://raw.githubusercontent.com/gitextensions/gitextensions/master/LICENSE.md", "gitext-LICENSE.txt")
        if self.options.with_graphviz:
            tools.download("https://graphviz.gitlab.io/_pages/Download/windows/graphviz-%s.zip" % (self._graphviz_version), "graphviz.zip")
            tools.download("https://gitlab.com/graphviz/graphviz/raw/master/COPYING", "graphviz-LICENSE.txt")
        if self.options.with_doxygen:
            tools.download("http://doxygen.nl/files/doxygen-%s-setup.exe" % (self._doxygen_version), "doxygen-win64.exe")
            tools.download("https://raw.githubusercontent.com/doxygen/doxygen/master/LICENSE", "doxygen-LICENSE.txt")
        if self.options.with_miktex:
            tools.download("http://ftp.fau.de/ctan/systems/win32/miktex/setup/windows-x86/miktex-portable-%s.exe" % (self._miktex_version), "miktex-win64.exe")
            tools.download("https://raw.githubusercontent.com/MiKTeX/miktex/master/COPYING.md", "miktex-LICENSE.txt")
        if self.options.with_ninja:
            tools.download("https://github.com/ninja-build/ninja/releases/download/v%s/ninja-win.zip" % (self._ninja_version), "ninja-win.zip")
            tools.download("https://raw.githubusercontent.com/ninja-build/ninja/master/COPYING", "ninja-LICENSE.txt")
    
    def _append_to_license_txt(self, name, url, description, license_file):
        os.linesep= '\r\n'
        with open(os.path.join(self.build_folder, self.name, "LICENSE.txt"), "a", encoding="utf8") as f:
            f.write("\n")
            f.write("=" * 80 + "\n")
            f.write("=" * 2  + "\n")
            f.write("=" * 2 + " %s: %s" % (name, description)  + "\n")
            f.write("=" * 2 + " %s" % (url)  + "\n")
            f.write("=" * 2  + "\n")
            f.write("=" * 2 + " %s is covered by the following licensed terms (LICENSE.txt):" % (name)  + "\n")
            f.write("=" * 2  + "\n")
            f.write("\n")
            with open(license_file, 'r', encoding="utf8") as f2:
                for line in f2:
                    f.write(line)
            f.write("\n")
                
    def _update_conemu_xml_config(self):
        output_dir = output = os.path.join(self.build_folder, self.name, "vendor", "barbarian-extra")
        os.mkdir(output_dir)
        shutil.copyfile(os.path.join(self.source_folder, "configuration", "helpers", "vswhere_find_vs2017.bat"), os.path.join(output_dir, "vswhere_find_vs2017.bat"))
        vs_versions = { 
            "VS 2010" : "VS100COMNTOOLS", 
            "VS 2012" : "VS110COMNTOOLS", 
            "VS 2013" : "VS120COMNTOOLS", 
            "VS 2015" : "VS140COMNTOOLS", 
            "VS 2017" : "VS150COMNTOOLS" 
            }
        template_dir = os.path.join(self.source_folder, "configuration")
        env = jinja2.Environment(loader= jinja2.FileSystemLoader(template_dir), trim_blocks=True, lstrip_blocks=True, undefined=jinja2.StrictUndefined)
        conemu_xml_template = env.get_template("ConEmu.xml.default.j2") 
        output_dir = os.path.join(self.build_folder, self.name, "vendor")
        output = os.path.join(output_dir, "ConEmu.xml.default")
        os.rename(output, os.path.join(output_dir, "ConEmu.xml.original"))
        f = open(output, "w")
        vs_tool_prompts = [ ]
        Count = 9
        for vs_version,vs_common_tools in vs_versions.items():
            Count = Count + 1
            vs_tool_prompts.append(VsToolVersion("Task%d" % Count, self._conemu_xml_creation_datetime, self._conemu_xml_buildnummer, "%s-32Bit" % vs_version, vs_common_tools, "x86"))
            Count = Count + 1
            vs_tool_prompts.append(VsToolVersion("Task%d" % Count, self._conemu_xml_creation_datetime, self._conemu_xml_buildnummer, "%s-64Bit" % vs_version, vs_common_tools, "x86_amd64"))
        f.write(conemu_xml_template.render(vs_tool_prompts = vs_tool_prompts, Count = Count))
        f.close()

    def build(self):
        # 0. Cmder
        tools.unzip(os.path.join(self.source_folder, "cmder_mini.zip"), destination = self.name)

        # 0b. Setup docs
        os.remove(os.path.join(self.build_folder, self.name, "Version %s" % self._cmder_version_build))
        os.rename(os.path.join(self.build_folder, self.name, "LICENSE"), os.path.join(self.build_folder, self.name, "LICENSE-cmder.txt"))

        # 1. Create profile directory
        tools.mkdir(os.path.join(self.build_folder, self.name, "config", "profile.d"))

        # 1b. Copy LICENSE and README files, and icons
        shutil.copyfile(os.path.join(self.source_folder, "LICENSE.txt"), os.path.join(self.build_folder, self.name, "LICENSE-barbarian.txt"))
        shutil.copyfile(os.path.join(self.source_folder, "README.txt"), os.path.join(self.build_folder, self.name, "README.txt"))
        shutil.copyfile(os.path.join(self.source_folder, "README.md"), os.path.join(self.build_folder, self.name, "README.md"))
        shutil.copyfile(os.path.join(self.source_folder, "documentation", "logo", "Barbarian.ico"), os.path.join(self.build_folder, self.name, "Barbarian.ico"))
        shutil.copyfile(os.path.join(self.source_folder, "documentation", "logo", "Barbarian128.png"), os.path.join(self.build_folder, self.name, "Barbarian.png"))

        # 1c. Append to license
        self._append_to_license_txt("Barbarian", "https://github.com/kwallner/Barbarian", "A Software Development Environment for Conan.io", os.path.join(self.build_folder, self.name, "LICENSE-barbarian.txt"))
        os.remove(os.path.join(self.build_folder, self.name, "LICENSE-barbarian.txt"))

        # 1c. Append License of cmder
        self._append_to_license_txt("Cmder", "http://cmder.net/", "Console emulator for Windows", os.path.join(self.build_folder, self.name, "LICENSE-cmder.txt"))
        os.remove(os.path.join(self.build_folder, self.name, "LICENSE-cmder.txt"))
        self._append_to_license_txt("Clink", "http://mridgers.github.io/clink/", "Powerful Bash-style command line editing for cmd.exe", os.path.join(self.build_folder, self.name, "vendor", "clink", "LICENSE"))
        self._append_to_license_txt("clink-completions", "https://github.com/vladimir-kotikov/clink-completions", "Completion files to clink util", os.path.join(self.build_folder, self.name, "vendor", "clink-completions", "LICENSE"))
        self._append_to_license_txt("ConEmu", "https://conemu.github.io/", "Handy Windows Terminal", os.path.join(self.build_folder, self.name, "vendor", "conemu-maximus5", "ConEmu", "License.txt"))

        # 1d. Update/Replace ConEmu.xml
        self._update_conemu_xml_config()

        # 2. Git
        if self.options.with_git:
            call(["7z", "x", os.path.join(self.source_folder, "git-for-windows.7z.exe"), "-o%s/%s" % (self.name, "vendor/git-for-windows") ])
            # No need for install script. Git is already included (so do not change name)
            os.linesep= '\r\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "git-for-windows.cmd"), 'w') as f:
                f.write(':: Vendor: git support\n')
                path = os.path.join("%CMDER_ROOT%", "vendor", "git-for-windows", "cmd")
                f.write('set "PATH={0};%PATH%"\n'.format(path))
                path = os.path.join("%CMDER_ROOT%", "vendor", "git-for-windows", "mingw64", "bin")
                f.write('set "PATH={0};%PATH%"\n'.format(path))
                path = os.path.join("%CMDER_ROOT%", "vendor", "git-for-windows", "usr", "bin")
                f.write('set "PATH={0};%PATH%"\n'.format(path))
            os.linesep= '\r\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "git-for-windows.ps1"), 'w') as f:
                f.write('# Vendor: git support\n')
                path = os.path.join("$env:CMDER_ROOT", "vendor", "git-for-windows", "cmd")
                f.write('$env:PATH="PATH={0};" + $env:PATH\n'.format(path))
                path = os.path.join("$env:CMDER_ROOT", "vendor", "git-for-windows", "mingw64", "bin")
                f.write('$env:PATH="PATH={0};" + $env:PATH\n'.format(path))
                path = os.path.join("$env:CMDER_ROOT", "vendor", "git-for-windows", "usr", "bin")
                f.write('$env:PATH="PATH={0};" + $env:PATH\n'.format(path))
            os.linesep= '\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "git-for-windows.sh"), 'w') as f:
                f.write('# Vendor: git support\n')
                # Pathes are already correct
            self._append_to_license_txt("Git", "https://git-scm.com", "Distributed version control system", os.path.join(self.build_folder, self.name, "vendor", "git-for-windows", "LICENSE.txt"))

        # 3a. CMake
        if self.options.with_cmake:
            tools.unzip(os.path.join(self.source_folder, "cmake-win64.zip"), destination = os.path.join(self.name, "vendor"))
            os.rename(os.path.join(self.name, "vendor", "cmake-%s-win64-x64" % (self._cmake_version)), os.path.join(self.name, "vendor", "cmake-for-windows"))
            # Create install script
            os.linesep= '\r\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "cmake-for-windows.cmd"), 'w') as f:
                f.write(':: Vendor: cmake support\n')
                path = os.path.join("%CMDER_ROOT%", "vendor", "cmake-for-windows", "bin")
                f.write('set "PATH={0};%PATH%"\n'.format(path))
            os.linesep= '\r\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "cmake-for-windows.ps1"), 'w') as f:
                f.write('# Vendor: cmake support\n')
                path = os.path.join("$env:CMDER_ROOT", "vendor", "cmake-for-windows", "bin")
                f.write('$env:PATH="PATH={0};" + $env:PATH\n'.format(path))
            os.linesep= '\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "cmake-for-windows.sh"), 'w') as f:
                f.write('# Vendor: cmake support\n')
                path = os.path.join("$CMDER_ROOT", "vendor", "cmake-for-windows", "bin")
                f.write('export "PATH={0}:$PATH"\n'.format(path))
            self._append_to_license_txt("CMake", "https://cmake.org/", "Cross-Plattform Build System", os.path.join(self.build_folder, self.name, "vendor", "cmake-for-windows", "doc", "cmake", "Copyright.txt"))

        # 3b. Bazel
        if self.options.with_bazel:
            tools.unzip(os.path.join(self.source_folder, "bazel-win64.zip"), destination = os.path.join(self.name, "vendor", "bazel-for-windows"))
            shutil.copyfile(os.path.join(self.source_folder, "bazel-LICENSE.txt"), os.path.join(self.name, "vendor", "bazel-for-windows", "LICENSE.txt"))
            # Create install script
            os.linesep= '\r\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "bazel-for-windows.cmd"), 'w') as f:
                f.write(':: Vendor: bazel support\n')
                path = os.path.join("%CMDER_ROOT%", "vendor", "bazel-for-windows")
                f.write('set "PATH={0};%PATH%"\n'.format(path))
            os.linesep= '\r\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "bazel-for-windows.ps1"), 'w') as f:
                f.write('# Vendor: bazel support\n')
                path = os.path.join("$env:CMDER_ROOT", "vendor", "bazel-for-windows")
                f.write('$env:PATH="PATH={0};" + $env:PATH\n'.format(path))
            os.linesep= '\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "bazel-for-windows.sh"), 'w') as f:
                f.write('# Vendor: bazel support\n')
                path = os.path.join("$CMDER_ROOT", "vendor", "bazel-for-windows")
                f.write('export "PATH={0}:$PATH"\n'.format(path))
            self._append_to_license_txt("Bazel", "https://bazel.build/", "Build and test software of any size, quickly and reliably", os.path.join(self.name, "vendor", "bazel-for-windows", "LICENSE.txt"))

        # 4. Python
        if self.options.with_python:
            call(["innounp", "-q", "-x", os.path.join(self.source_folder, "winpython3-win64.exe")])
            os.rename("{app}/python-3.7.1.amd64", os.path.join(self.name, "vendor", "python-for-windows"))
            shutil.rmtree("{app}")
            os.remove("install_script.iss")
            shutil.copyfile(os.path.join(self.source_folder, "winpython3-LICENSE.txt"), os.path.join(self.name, "vendor", "python-for-windows", "LICENSE.txt"))
            os.linesep= '\r\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "python-for-windows.cmd"), 'w') as f:
                f.write(':: Vendor: python support\n')
                path = os.path.join("%CMDER_ROOT%", "vendor", "python-for-windows")
                f.write('set "PATH={0};%PATH%"\n'.format(path))
                path = os.path.join("%CMDER_ROOT%", "vendor", "python-for-windows", "Scripts")
                f.write('set "PATH={0};%PATH%"\n'.format(path))
            os.linesep= '\r\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "python-for-windows.ps1"), 'w') as f:
                f.write('# Vendor: python support\n')
                path = os.path.join("$env:CMDER_ROOT", "vendor", "python-for-windows")
                f.write('$env:PATH="PATH={0};" + $env:PATH\n'.format(path))
                path = os.path.join("$env:CMDER_ROOT", "vendor", "python-for-windows", "Scripts")
                f.write('$env:PATH="PATH={0};" + $env:PATH\n'.format(path))
            os.linesep= '\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "python-for-windows.sh"), 'w') as f:
                f.write('# Vendor: python support\n')
                path = os.path.join("$CMDER_ROOT", "vendor", "python-for-windows")
                f.write('export "PATH={0}:$PATH"\n'.format(path))
                path = os.path.join("$CMDER_ROOT", "vendor", "python-for-windows", "Scripts")
                f.write('export "PATH={0}:$PATH"\n'.format(path))
            self._append_to_license_txt("WinPython", "http://winpython.github.io/", "Portable distribution of the Python programming language for Windows", os.path.join(self.name, "vendor", "python-for-windows", "LICENSE.txt"))
            self._append_to_license_txt("Python", "https://www.python.org/", "Python programming language", os.path.join(self.source_folder, "cpython-LICENSE.txt"))
            # Additional python packages
            call(["%s/vendor/python-for-windows/python.exe" % self.name, "-m", "pip", "install", "openpyxl==%s" % self._openpyxl_version, "--no-warn-script-location"])
            self._append_to_license_txt("openpyxl", "https://openpyxl.readthedocs.io/", "Python programming language", os.path.join(self.source_folder, "openpyxl-LICENSE.txt"))

        # 5. Conan.io
        if self.options.with_conanio:
            call(["%s/vendor/python-for-windows/python.exe" % self.name, "-m", "pip", "install", "conan==%s" % self._conan_version, "--no-warn-script-location"])
            # No install script needed ... installed with python
            self._append_to_license_txt("Conan.io", "https://conan.io/", "A Python library to read/write Excel 2010 xlsx/xlsm files", os.path.join(self.source_folder, "conanio-LICENSE.txt"))

        # 6. VS Code + Extensions
        if self.options.with_vscode:
            tools.unzip(os.path.join(self.source_folder, "vscode-win64.zip"), destination = os.path.join(self.name, "vendor", "vscode-for-windows"))
            # Some useful extensions
            old = os.getcwd()
            os.chdir(os.path.join(self.name, "vendor", "vscode-for-windows", "bin"))
            call(["code.cmd", "--install-extension", "ms-vscode.cpptools", "--force", "--extensions-dir", "resources/app/extensions"])
            call(["code.cmd", "--install-extension", "ms-python.python", "--force", "--extensions-dir", "resources/app/extensions"])
            call(["code.cmd", "--install-extension", "MS-CEINTL.vscode-language-pack-de", "--force", "--extensions-dir", "resources/app/extensions"])
            call(["code.cmd", "--install-extension", "twxs.cmake", "--force", "--extensions-dir", "resources/app/extensions"])
            call(["code.cmd", "--install-extension", "vector-of-bool.cmake-tools", "--force", "--extensions-dir", "resources/app/extensions"])
            call(["code.cmd", "--install-extension", "DevonDCarew.bazel-code", "--force", "--extensions-dir", "resources/app/extensions"])
            os.chdir(old)
            # Create install script
            os.linesep= '\r\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "vscode-for-windows.cmd"), 'w') as f:
                f.write(':: Vendor: vscode support\n')
                path = os.path.join("%CMDER_ROOT%", "vendor", "vscode-for-windows", "bin")
                f.write('set "PATH={0};%PATH%"\n'.format(path))
            os.linesep= '\r\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "vscode-for-windows.ps1"), 'w') as f:
                f.write('# Vendor: vscode support\n')
                path = os.path.join("$env:CMDER_ROOT", "vendor", "vscode-for-windows", "bin")
                f.write('$env:PATH="PATH={0};" + $env:PATH\n'.format(path))
            os.linesep= '\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "vscode-for-windows.sh"), 'w') as f:
                f.write('# Vendor: vscode support\n')
                path = os.path.join("$CMDER_ROOT", "vendor", "vscode-for-windows", "bin")
                f.write('export "PATH={0}:$PATH"\n'.format(path))
            self._append_to_license_txt("Visual Studio Code", "https://code.visualstudio.com/", "Code editing Redefined", os.path.join(self.name, "vendor", "vscode-for-windows", "resources", "app", "LICENSE.txt"))

        # 7. KDiff3
        if self.options.with_kdiff3:
            call(["7z", "x", os.path.join(self.source_folder, "kdiff3-win64.exe"), "-o%s/%s" % (self.name, "vendor/kdiff3-for-windows"), '-x!$PLUGINSDIR', '-x!Uninstall.exe' ])
            # Create install script
            os.linesep= '\r\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "kdiff3-for-windows.cmd"), 'w') as f:
                f.write(':: Vendor: kdiff3 support\n')
                path = os.path.join("%CMDER_ROOT%", "vendor", "kdiff3-for-windows")
                f.write('set "PATH={0};%PATH%"\n'.format(path))
            os.linesep= '\r\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "kdiff3-for-windows.ps1"), 'w') as f:
                f.write('# Vendor: kdiff3 support\n')
                path = os.path.join("$env:CMDER_ROOT", "vendor", "kdiff3-for-windows")
                f.write('$env:PATH="PATH={0};" + $env:PATH\n'.format(path))
            os.linesep= '\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "kdiff3-for-windows.sh"), 'w') as f:
                f.write('# Vendor: kdiff3 support\n')
                path = os.path.join("$CMDER_ROOT", "vendor", "kdiff3-for-windows")
                f.write('export "PATH={0}:$PATH"\n'.format(path))
            self._append_to_license_txt("KDiff3", "http://kdiff3.sourceforge.net/", "Diff and Merge Program", os.path.join(self.name, "vendor", "kdiff3-for-windows", "COPYING.txt"))

        # 8. WinMerge
        if self.options.with_winmerge:
            tools.unzip(os.path.join(self.source_folder, "winmerge-win64.exe.zip"))
            os.rename("WinMerge", os.path.join(self.name, "vendor", "winmerge-for-windows"))
            tools.mkdir(os.path.join(self.build_folder, self.name, "vendor", "winmerge-for-windows", "bin"))
            # Create run script
            with open(os.path.join(self.build_folder, self.name, "vendor", "winmerge-for-windows", "bin", "winmerge.cmd"), 'w') as f:
                f.write('@echo off\n')
                f.write('call "%~dp0..\\WinMergeU.exe" %*\n')
            # Create install script
            os.linesep= '\r\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "winmerge-for-windows.cmd"), 'w') as f:
                f.write(':: Vendor: winmerge support\n')
                path = os.path.join("%CMDER_ROOT%", "vendor", "winmerge-for-windows", "bin")
                f.write('set "PATH={0};%PATH%"\n'.format(path))
            os.linesep= '\r\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "winmerge-for-windows.ps1"), 'w') as f:
                f.write('# Vendor: winmerge support\n')
                path = os.path.join("$env:CMDER_ROOT", "vendor", "winmerge-for-windows", "bin")
                f.write('$env:PATH="PATH={0};" + $env:PATH\n'.format(path))
            os.linesep= '\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "winmerge-for-windows.sh"), 'w') as f:
                f.write('# Vendor: winmerge support\n')
                path = os.path.join("$CMDER_ROOT", "vendor", "winmerge-for-windows", "bin")
                f.write('export "PATH={0}:$PATH"\n'.format(path))
                f.write('alias winmerge=WinMergeU.exe\n')
            self._append_to_license_txt("WinMerge", "http://winmerge.org/", "Open Source differencing and merging tool for Windows", os.path.join(self.source_folder, "winmerge-LICENSE.txt"))

        # 9. GitExt
        if self.options.with_gitext:
            call(["7z", "x", os.path.join(self.source_folder, "gitext.exe"), "-o%s/%s" % (self.name, "vendor/gitext-for-windows") ])
            tools.mkdir(os.path.join(self.build_folder, self.name, "vendor", "gitext-for-windows", "bin"))
            # Create run script
            with open(os.path.join(self.build_folder, self.name, "vendor", "gitext-for-windows", "bin", "gitext.cmd"), 'w') as f:
                f.write('@echo off\n')
                f.write('call "%~dp0..\\GitExtensions.exe" %*\n')
            # Create install script
            os.linesep= '\r\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "gitext-for-windows.cmd"), 'w') as f:
                f.write(':: Vendor: gitext support\n')
                path = os.path.join("%CMDER_ROOT%", "vendor", "gitext-for-windows", "bin")
                f.write('set "PATH={0};%PATH%"\n'.format(path))
            os.linesep= '\r\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "gitext-for-windows.ps1"), 'w') as f:
                f.write('# Vendor: gitext support\n')
                path = os.path.join("$env:CMDER_ROOT", "vendor", "gitext-for-windows", "bin")
                f.write('$env:PATH="PATH={0};" + $env:PATH\n'.format(path))
            os.linesep= '\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "gitext-for-windows.sh"), 'w') as f:
                f.write('# Vendor: gitext support\n')
                path = os.path.join("$CMDER_ROOT", "vendor", "gitext-for-windows", "bin")
                f.write('export "PATH={0}:$PATH"\n'.format(path))
            self._append_to_license_txt("Git Extensions", "http://gitextensions.github.io/", "Graphical user interface for Git", os.path.join(self.source_folder, "gitext-LICENSE.txt"))

        # 10. Graphviz
        if self.options.with_graphviz:
            tools.unzip(os.path.join(self.source_folder, "graphviz.zip"), destination = os.path.join(self.name, "vendor"))
            os.rename(os.path.join(self.name, "vendor", "release"), os.path.join(self.name, "vendor", "graphviz-for-windows"))
            # Create install script
            os.linesep= '\r\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "graphviz-for-windows.cmd"), 'w') as f:
                f.write(':: Vendor: graphviz support\n')
                path = os.path.join("%CMDER_ROOT%", "vendor", "graphviz-for-windows", "bin")
                f.write('set "PATH={0};%PATH%"\n'.format(path))
            os.linesep= '\r\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "graphviz-for-windows.ps1"), 'w') as f:
                f.write('# Vendor: graphviz support\n')
                path = os.path.join("$env:CMDER_ROOT", "vendor", "graphviz-for-windows", "bin")
                f.write('$env:PATH="PATH={0};" + $env:PATH\n'.format(path))
            os.linesep= '\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "graphviz-for-windows.sh"), 'w') as f:
                f.write('# Vendor: graphviz support\n')
                path = os.path.join("$CMDER_ROOT", "vendor", "graphviz-for-windows", "bin")
                f.write('export "PATH={0}:$PATH"\n'.format(path))
            self._append_to_license_txt("Graphviz", "https://www.graphviz.org/", "Graph Visualization Software", os.path.join(self.source_folder, "graphviz-LICENSE.txt"))
            
        # 11. Doxygen
        if self.options.with_doxygen:
            call(["innounp", "-q", "-x", os.path.join(self.source_folder, "doxygen-win64.exe")])
            os.rename("{app}", os.path.join(self.name, "vendor", "doxygen-for-windows"))
            shutil.rmtree("{tmp}")
            os.remove("install_script.iss")
            shutil.copyfile(os.path.join(self.source_folder, "doxygen-LICENSE.txt"), os.path.join(self.name, "vendor", "doxygen-for-windows", "LICENSE.txt"))
            # Fix Doxygen
            os.remove(os.path.join(self.name, "vendor", "doxygen-for-windows", "bin", "doxygen,2.exe"))
            os.remove(os.path.join(self.name, "vendor", "doxygen-for-windows", "bin", "doxyindexer,2.exe"))
            os.remove(os.path.join(self.name, "vendor", "doxygen-for-windows", "bin", "doxysearch.cgi,2.exe"))
            os.remove(os.path.join(self.name, "vendor", "doxygen-for-windows", "bin", "libclang,2.dll"))
            os.rename(os.path.join(self.name, "vendor", "doxygen-for-windows", "bin", "doxygen,1.exe"), os.path.join(self.name, "vendor", "doxygen-for-windows", "bin", "doxygen.exe"))
            os.rename(os.path.join(self.name, "vendor", "doxygen-for-windows", "bin", "doxyindexer,1.exe"), os.path.join(self.name, "vendor", "doxygen-for-windows", "bin", "doxyindexer.exe"))
            os.rename(os.path.join(self.name, "vendor", "doxygen-for-windows", "bin", "doxysearch.cgi,1.exe"), os.path.join(self.name, "vendor", "doxygen-for-windows", "bin", "doxysearch.cgi.exe"))
            os.rename(os.path.join(self.name, "vendor", "doxygen-for-windows", "bin", "libclang,1.dll"), os.path.join(self.name, "vendor", "doxygen-for-windows", "bin", "libclang.dll"))
            # Create install script
            os.linesep= '\r\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "doxygen-for-windows.cmd"), 'w') as f:
                f.write(':: Vendor: doxygen support\n')
                path = os.path.join("%CMDER_ROOT%", "vendor", "doxygen-for-windows", "bin")
                f.write('set "PATH={0};%PATH%"\n'.format(path))
            os.linesep= '\r\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "doxygen-for-windows.ps1"), 'w') as f:
                f.write('# Vendor: doxygen support\n')
                path = os.path.join("$env:CMDER_ROOT", "vendor", "doxygen-for-windows", "bin")
                f.write('$env:PATH="PATH={0};" + $env:PATH\n'.format(path))
            os.linesep= '\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "doxygen-for-windows.sh"), 'w') as f:
                f.write('# Vendor: doxygen support\n')
                path = os.path.join("$CMDER_ROOT", "vendor", "doxygen-for-windows", "bin")
                f.write('export "PATH={0}:$PATH"\n'.format(path))
            self._append_to_license_txt("Doxygen", "http://www.doxygen.nl/", "Generate documentation from source code", os.path.join(self.source_folder, "doxygen-LICENSE.txt"))
        
        # 12. MiKTex
        if self.options.with_miktex:
            call(["7z", "x", os.path.join(self.source_folder, "miktex-win64.exe"), "-o%s/%s/%s" % (self.name, "vendor", "miktex-for-windows") ])
            tools.mkdir(os.path.join(self.build_folder, self.name, "vendor", "miktex-for-windows", "bin"))
            # Create ghostscript hack script (Doxygen hardcoded gswin32c.exe for latex. MikTex uses mgs.exe)
            os.linesep= '\r\n'
            with open(os.path.join(self.build_folder, self.name,  "vendor", "miktex-for-windows", "bin", "gswin32c.exe.cmd"), 'w') as f:
                f.write('@ECHO OFF\n')
                f.write('"%~d0%~p0\\..\\texmfs\\install\\miktex\\bin\\mgs.exe" %*\n')
            # Create install script
            os.linesep= '\r\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "miktex-for-windows.cmd"), 'w') as f:
                f.write(':: Vendor: miktex support\n')
                path = os.path.join("%CMDER_ROOT%", "vendor", "miktex-for-windows", "bin")
                f.write('set "PATH={0};%PATH%"\n'.format(path))
                path = os.path.join("%CMDER_ROOT%", "vendor", "miktex-for-windows", "texmfs", "install", "miktex", "bin")
                f.write('set "PATH={0};%PATH%"\n'.format(path))
            os.linesep= '\r\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "miktex-for-windows.ps1"), 'w') as f:
                f.write('# Vendor: miktex support\n')
                path = os.path.join("$env:CMDER_ROOT", "vendor", "miktex-for-windows", "bin")
                f.write('$env:PATH="PATH={0};" + $env:PATH\n'.format(path))
                path = os.path.join("$env:CMDER_ROOT", "vendor", "miktex-for-windows", "texmfs", "install", "miktex", "bin")
                f.write('$env:PATH="PATH={0};" + $env:PATH\n'.format(path))
            os.linesep= '\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "miktex-for-windows.sh"), 'w') as f:
                f.write('# Vendor: miktex support\n')
                path = os.path.join("$CMDER_ROOT", "vendor", "miktex-for-windows", "bin")
                f.write('export "PATH={0}:$PATH"\n'.format(path))
                path = os.path.join("$CMDER_ROOT", "vendor", "miktex-for-windows", "texmfs", "install", "miktex", "bin")
                f.write('export "PATH={0}:$PATH"\n'.format(path))
            self._append_to_license_txt("MiKTex", "https://miktex.org/", "MiKTeX is an implementation of TeX and related programs", os.path.join(self.source_folder, "miktex-LICENSE.txt"))

        # 13. Ninja
        if self.options.with_ninja:
            tools.unzip(os.path.join(self.source_folder, "ninja-win.zip"))
            tools.mkdir(os.path.join(self.build_folder, self.name, "vendor", "ninja-for-windows"))
            os.rename("ninja.exe", os.path.join(self.name, "vendor", "ninja-for-windows", "ninja.exe"))
            # Create install script
            os.linesep= '\r\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "ninja-for-windows.cmd"), 'w') as f:
                f.write(':: Vendor: ninja support\n')
                path = os.path.join("%CMDER_ROOT%", "vendor", "ninja-for-windows")
                f.write('set "PATH={0};%PATH%"\n'.format(path))
            os.linesep= '\r\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "ninja-for-windows.ps1"), 'w') as f:
                f.write('# Vendor: ninja support\n')
                path = os.path.join("$env:CMDER_ROOT", "vendor", "ninja-for-windows")
                f.write('$env:PATH="PATH={0};" + $env:PATH\n'.format(path))
            os.linesep= '\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "ninja-for-windows.sh"), 'w') as f:
                f.write('# Vendor: ninja support\n')
                path = os.path.join("$CMDER_ROOT", "vendor", "ninja-for-windows")
                f.write('export "PATH={0}:$PATH"\n'.format(path))
            self._append_to_license_txt("Ninja Build", "https://ninja-build.org/", "Small build system with a focus on speed", os.path.join(self.source_folder, "ninja-LICENSE.txt"))
            
        # Final. Pack everything
        shutil.copyfile(os.path.join(self.source_folder, "packaging", "package.iss"), "package.iss")
        tools.replace_in_file("package.iss", '@name@', self.name)
        tools.replace_in_file("package.iss", '@version@', self.version)
        tools.replace_in_file("package.iss", '@author@', self.author)
        tools.replace_in_file("package.iss", '@url@', self.url)
        tools.replace_in_file("package.iss", '@conan_version@', self._conan_version)
        tools.replace_in_file("package.iss", '@output_base_name@', "%s-%s-%s-%s" % (self.name, self.version, self.settings.arch, self._installertype))
        iscc_command= ["iscc", "/Q"]
        if self.options.with_git:
            iscc_command.append("/Dwith_git")
        if self.options.with_cmake:
            iscc_command.append("/Dwith_cmake")
        if self.options.with_bazel:
            iscc_command.append("/Dwith_bazel")
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
        if self.options.with_graphviz:
            iscc_command.append("/Dwith_graphviz")
        if self.options.with_doxygen:
            iscc_command.append("/Dwith_doxygen")
        if self.options.with_miktex:
            iscc_command.append("/Dwith_miktex")
        if self.options.with_ninja:
            iscc_command.append("/Dwith_ninja")
        iscc_command.append("package.iss")
        call(iscc_command)
        
    def package(self):
        self.copy("README.md")
        self.copy("README.txt")
        self.copy("LICENSE.txt")
        self.copy("%s-%s-%s-%s.exe" % (self.name, self.version, self.settings.arch, self._installertype))
 
