from conans import ConanFile, tools
import os
import shutil
import jinja2
import subprocess
import tempfile
from datetime import datetime

class VsToolVersion:
    def __init__(self, name, modified, build, Name, CommonToolsEnv, Architecture):
        self.name = name
        self.modified = modified
        self.build = build
        self.Name = Name
        self.GuiArgs = "/icon \"%" + CommonToolsEnv + "%..\\IDE\\devenv.exe\""
        extra_call = ""
        extra_path= ""
        if CommonToolsEnv == "VS150COMNTOOLS":
            extra_call = "call \"%ConEmuDir%\\..\\barbarian-extra\\vswhere_find_vs2017.bat\" &amp; "
            extra_path = "Auxiliary\\Build\\"
        elif CommonToolsEnv == "VS160COMNTOOLS":
            extra_call = "call \"%ConEmuDir%\\..\\barbarian-extra\\vswhere_find_vs2019.bat\" &amp; "
            extra_path = "Auxiliary\\Build\\"
        if CommonToolsEnv == "WINDOWSSDK7":
            self.Cmd1 = "call \"C:\\Program Files\\Microsoft SDKs\\Windows\\v7.1\\Bin\\SetEnv.cmd\" &amp; cmd /k \"\"%ConEmuDir%\\..\\init.bat\"\""
        else:
            self.Cmd1 = extra_call + "call \"%" + CommonToolsEnv + "%..\\..\\VC\\" + extra_path + "vcvarsall.bat\" " + Architecture + " &amp; cmd /k \"\"%ConEmuDir%\\..\\init.bat\"\""
        self.Count = "1"
        self.Hotkey = "0"
        self.Flags = "0"
        self.Active = "1"

class BarbarianConan(ConanFile):
    name = "Barbarian"
    version = "2.0.0-rc3"
    _cmder_version = "1.3.14"
    _cmder_version_build = "%s.982" % _cmder_version
    _git_version = "2.26.0"
    _cmake_version = "3.17.1"
    _python_version = "3.7.7"
    _conan_version = "1.24.0"
    _vswhere_version = "2.8.4"
    _kdiff_version = "0.9.98"
    _winmerge_version = "2.16.6"
    _gitext_version = "3.3.1"
    _gitext_version_build = "%s.7897" % _gitext_version
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
    options = {"with_cmake": [True, False], "with_kdiff3" : [True, False], "with_winmerge" : [True, False], "with_gitext" : [True, False]}
    default_options = {"with_cmake" : True, "with_kdiff3" : True, "with_winmerge" : True, "with_gitext" : True}

    @property
    def _installertype_set(self):
        if self.options.with_cmake and self.options.with_kdiff3 and self.options.with_winmerge and self.options.with_gitext:
            return ""
        return "-custom"

    @property
    def _installertype(self):
        return self._installertype_set

    def build_requirements(self):
        self.build_requires("7zip/19.00@%s/%s" % (self.user, self.channel))
        self.build_requires("InnoSetup/6.0.3@kwallner/testing")
        self.build_requires("cpython/%s@%s/%s" % (self._python_version, self.user, self.channel))

    def _url_download_to_temp(self, url, temp_name):
        tools.download(url, os.path.join(temp_name, os.path.basename(url)))

    def _pip_download_to_temp(self, pkg_name, temp_name):
        subprocess.run([
            "pip",
            "download",
            "--only-binary=:all:",
            "--no-binary=:none:",
            "--platform", "win_amd64", 
            "--python-version", "%s" % ("".join(self._python_version.split(".")[0:2])),
            "--implementation", "cp",
            "--find-links=.", 
            "--isolated", 
            pkg_name ], cwd=temp_name, check=True)
    
    def _pip_tar2whl_to_temp(self, pkg_name, temp_name):
        with tempfile.TemporaryDirectory() as tmpdirname:
            with tools.chdir(tmpdirname): 
                subprocess.run([
                    "pip",
                    "download",
                    "--no-deps",
                    "--platform", "win_amd64", 
                    "--python-version", "%s" % ("".join(self._python_version.split(".")[0:2])),
                    "--implementation", "cp",
                    "--find-links=.", 
                    "--isolated", 
                    pkg_name], check=True)
                (tar_file,)= [ filename for filename in os.listdir(".") if filename.endswith(".tar.gz") ]
                tools.untargz(tar_file)
                with tools.chdir(tar_file.replace(".tar.gz", "")): 
                    tools.replace_in_file("setup.py", "from distutils.core import setup", "from setuptools import setup", strict=False)
                    subprocess.run([
                        "python",
                        "setup.py",
                        "bdist_wheel",
                        "-d", os.path.join(self.source_folder, temp_name)], check=True)

    def source(self):
        tools.download("https://github.com/cmderdev/cmder/releases/download/v%s/cmder_mini.zip" % (self._cmder_version), "cmder_mini.zip", sha256="5d5c05fb60404b819d0e2730c04bd1e0e5cb6ef1227b78a5790ed1b935687d84")
        tools.download("https://github.com/git-for-windows/git/releases/download/v%s.windows.1/PortableGit-%s-64-bit.7z.exe" % (".".join(self._git_version.split(".")[0:3]), self._git_version), "git-for-windows.7z.exe", sha256="f14aeccf0b63700c13a9c3829c4b9a6d3933d6cc5adfbc52b5aa62921725fb73")
        if self.options.with_cmake:
            tools.download("https://cmake.org/files/v%s.%s/cmake-%s-win64-x64.zip" % (self._cmake_version.split(".")[0], self._cmake_version.split(".")[1], self._cmake_version), "cmake-win64.zip", sha256="a5af7a2fe73f34070456397e940042e4469f072126c82974f44333ac43d478b1")
        tools.download("https://github.com/microsoft/vswhere/releases/download/%s/vswhere.exe" % self._vswhere_version, "vswhere.exe", sha256="e50a14767c27477f634a4c19709d35c27a72f541fb2ba5c3a446c80998a86419")
        if self.options.with_kdiff3:
            tools.download("https://netix.dl.sourceforge.net/project/kdiff3/kdiff3/%s/KDiff3-64bit-Setup_%s-2.exe" % (self._kdiff_version, self._kdiff_version), "kdiff3-win64.exe", sha256="d630ab0fdca3b4f1a85ab7e453f669fdc901cb81bb57f7e20de64c02ac9a1eeb")
        if self.options.with_winmerge:
            tools.download("https://netix.dl.sourceforge.net/project/winmerge/stable/%s/winmerge-%s-x64-exe.zip" % (self._winmerge_version, self._winmerge_version), "winmerge-win64.exe.zip", sha256="f7fcf1167c6332664eb1e75bcdd822369a0716cc1faae3fd4101a88a88fca963")
            tools.download("https://raw.githubusercontent.com/WinMerge/winmerge/master/LICENSE.md", "winmerge-LICENSE.txt")
        if self.options.with_gitext:
            tools.download("https://github.com/gitextensions/gitextensions/releases/download/v%s/GitExtensions-%s.msi" % (self._gitext_version, self._gitext_version_build), "gitext.exe", sha256="8a2cf10a8d14444d60485a462c649c48d44f41ff1283b4e7e72a00165c19e54f")
            tools.download("https://raw.githubusercontent.com/gitextensions/gitextensions/master/LICENSE.md", "gitext-LICENSE.txt")
        # Requirements for pip
        self._url_download_to_temp("https://bootstrap.pypa.io/get-pip.py", temp_name="python_temp")
        # Basic packages
        self._pip_download_to_temp("pip", temp_name="python_temp")
        self._pip_download_to_temp("wheel", temp_name="python_temp")
        self._pip_download_to_temp("setuptools", temp_name="python_temp")
        # Requirements for conan
        self._pip_tar2whl_to_temp("conan==%s" % self._conan_version, temp_name="conan_temp")
        self._pip_tar2whl_to_temp("future==0.18.2", temp_name="conan_temp")
        self._pip_tar2whl_to_temp("patch-ng==1.17.4", temp_name="conan_temp")
        self._pip_tar2whl_to_temp("pluginbase==0.7", temp_name="conan_temp")
        self._pip_download_to_temp("conan==%s" % self._conan_version, temp_name="conan_temp")
        tools.download("https://raw.githubusercontent.com/conan-io/conan/develop/LICENSE.md", "conanio-LICENSE.txt")
        # Requirements for pylint 
        self._pip_tar2whl_to_temp("wrapt==1.11.2", temp_name="python_temp") 
        self._pip_download_to_temp("pylint", temp_name="python_temp")
         
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
        shutil.copyfile(os.path.join(self.source_folder, "vswhere.exe"), os.path.join(output_dir, "vswhere.exe"))
        shutil.copyfile(os.path.join(self.source_folder, "configuration", "helpers", "vswhere_find_vs2017.bat"), os.path.join(output_dir, "vswhere_find_vs2017.bat"))
        shutil.copyfile(os.path.join(self.source_folder, "configuration", "helpers", "vswhere_find_vs2019.bat"), os.path.join(output_dir, "vswhere_find_vs2019.bat"))
        vs_versions = {
            #"Windows SDK 7" : "WINDOWSSDK7", 
            "VS 2010" : "VS100COMNTOOLS",
            #"VS 2012" : "VS110COMNTOOLS",
            #"VS 2013" : "VS120COMNTOOLS",
            "VS 2015" : "VS140COMNTOOLS",
            "VS 2017" : "VS150COMNTOOLS",
            "VS 2019" : "VS160COMNTOOLS"
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
        self._append_to_license_txt("Barbarian", "https://github.com/kwallner/Barbarian", "A Software Development Environment for Conan.io", os.path.join(self.build_folder, self.name, "LICENSE.txt"))
        
        # 1c. Append License of cmder
        self._append_to_license_txt("Cmder", "http://cmder.net/", "Console emulator for Windows", os.path.join(self.build_folder, self.name, "LICENSE-cmder.txt"))
        os.remove(os.path.join(self.build_folder, self.name, "LICENSE-cmder.txt"))
        self._append_to_license_txt("Clink", "http://mridgers.github.io/clink/", "Powerful Bash-style command line editing for cmd.exe", os.path.join(self.build_folder, self.name, "vendor", "clink", "LICENSE"))
        self._append_to_license_txt("clink-completions", "https://github.com/vladimir-kotikov/clink-completions", "Completion files to clink util", os.path.join(self.build_folder, self.name, "vendor", "clink-completions", "LICENSE"))
        self._append_to_license_txt("ConEmu", "https://conemu.github.io/", "Handy Windows Terminal", os.path.join(self.build_folder, self.name, "vendor", "conemu-maximus5", "ConEmu", "License.txt"))

        # 1d. Update/Replace ConEmu.xml
        self._update_conemu_xml_config()

        # 2. Git
        subprocess.call(["7z", "x", os.path.join(self.source_folder, "git-for-windows.7z.exe"), "-o%s/%s" % (self.name, "vendor/git-for-windows") ])
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
        # Git postinstall
        os.linesep= '\r\n'
        with open(os.path.join(self.build_folder, self.name, "vendor", "git-for-windows", "post-install.bat"), 'w') as f:
            f.write('@echo off\n')
            f.write('rem Git Postinstall\n')
            f.write('\n')
            f.write('rem Remove this script\n')
            f.write('(goto) 2>nul & del "%~f0"\n')
            
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
                path = os.path.join("$CMDER_ROOT", "vendor", "cmake-for-windows", "bin").replace("\\", "/")
                f.write('export "PATH={0}:$PATH"\n'.format(path))
            self._append_to_license_txt("CMake", "https://cmake.org/", "Cross-Plattform Build System", os.path.join(self.build_folder, self.name, "vendor", "cmake-for-windows", "doc", "cmake", "Copyright.txt"))

        # 3b. Bazel ... REMOVED

        # 4. Python
        shutil.copytree(self.deps_cpp_info["cpython"].rootpath,  os.path.join(self.name, "vendor", "python-for-windows"), ignore = shutil.ignore_patterns('conan*.txt'))
        os.linesep= '\r\n'
        with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "python-for-windows.cmd"), 'w') as f:
            f.write(':: Vendor: python support\n')
            path = os.path.join("%CMDER_ROOT%", "vendor", "python-for-windows", "bin")
            f.write('set "PATH={0};%PATH%"\n'.format(path))
            path = os.path.join("%CMDER_ROOT%", "vendor", "python-for-windows", "Scripts")
            f.write('set "PATH={0};%PATH%"\n'.format(path))
        os.linesep= '\r\n'
        with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "python-for-windows.ps1"), 'w') as f:
            f.write('# Vendor: python support\n')
            path = os.path.join("$env:CMDER_ROOT", "vendor", "python-for-windows", "bin")
            f.write('$env:PATH="{0};" + $env:PATH\n'.format(path))
            path = os.path.join("$env:CMDER_ROOT", "vendor", "python-for-windows", "Scripts")
            f.write('$env:PATH="{0};" + $env:PATH\n'.format(path))
        os.linesep= '\n'
        with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "python-for-windows.sh"), 'w') as f:
            f.write('# Vendor: python support\n')
            path = os.path.join("$CMDER_ROOT", "vendor", "python-for-windows", "bin").replace("\\", "/")
            f.write('export "PATH={0}:$PATH"\n'.format(path))
            path = os.path.join("$CMDER_ROOT", "vendor", "python-for-windows", "Scripts").replace("\\", "/")
            f.write('export "PATH={0}:$PATH"\n'.format(path))
        self._append_to_license_txt("Python", "https://python.org/", "Python Programming Language ",os.path.join(self.name, "vendor", "python-for-windows", "LICENSE"))

        # 5. Conan.io
        self._append_to_license_txt("Conan.io", "https://conan.io/", "C/C++ Package Manager", os.path.join(self.source_folder, "conanio-LICENSE.txt"))

        # 7. KDiff3
        if self.options.with_kdiff3:
            subprocess.call(["7z", "x", os.path.join(self.source_folder, "kdiff3-win64.exe"), "-o%s/%s" % (self.name, "vendor/kdiff3-for-windows"), '-x!$PLUGINSDIR', '-x!Uninstall.exe' ])
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
                path = os.path.join("$CMDER_ROOT", "vendor", "kdiff3-for-windows").replace("\\", "/")
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
                path = os.path.join("$CMDER_ROOT", "vendor", "winmerge-for-windows", "bin").replace("\\", "/")
                f.write('export "PATH={0}:$PATH"\n'.format(path))
                f.write('alias winmerge=WinMergeU.exe\n')
            self._append_to_license_txt("WinMerge", "http://winmerge.org/", "Open Source differencing and merging tool for Windows", os.path.join(self.source_folder, "winmerge-LICENSE.txt"))

        # 9. GitExt
        if self.options.with_gitext:
            subprocess.call(["7z", "x", os.path.join(self.source_folder, "gitext.exe"), "-o%s/%s" % (self.name, "vendor/gitext-for-windows") ])
            tools.mkdir(os.path.join(self.build_folder, self.name, "vendor", "gitext-for-windows", "bin"))
            # Create run script
            #with open(os.path.join(self.build_folder, self.name, "vendor", "gitext-for-windows", "gitext.bat"), 'w') as f:
            #    f.write('@echo off\n')
            #    f.write('start "%~dp0GitExtensions.exe" %*\n')
            # Create install script
            os.linesep= '\r\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "gitext-for-windows.cmd"), 'w') as f:
                f.write(':: Vendor: gitext support\n')
                path = os.path.join("%CMDER_ROOT%", "vendor", "gitext-for-windows")
                f.write('set "PATH={0};%PATH%"\n'.format(path))
            os.linesep= '\r\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "gitext-for-windows.ps1"), 'w') as f:
                f.write('# Vendor: gitext support\n')
                path = os.path.join("$env:CMDER_ROOT", "vendor", "gitext-for-windows")
                f.write('$env:PATH="PATH={0};" + $env:PATH\n'.format(path))
            os.linesep= '\n'
            with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "gitext-for-windows.sh"), 'w') as f:
                f.write('# Vendor: gitext support\n')
                path = os.path.join("$CMDER_ROOT", "vendor", "gitext-for-windows").replace("\\", "/")
                f.write('export "PATH={0}:$PATH"\n'.format(path))
            self._append_to_license_txt("Git Extensions", "http://gitextensions.github.io/", "Graphical user interface for Git", os.path.join(self.source_folder, "gitext-LICENSE.txt"))

        # 10. Graphviz ... REMOVED

        # 11. Doxygen ... REMOVED

        # 12. MiKTex ... REMOVED

        # 13. Ninja ... REMOVED

        # 14. Notepad ... REMOVED
            
        # 15. Pandoc ... REMOVED
            
        # 16. Ruby ... REMOVED

        # Final. Pack everything
        os.makedirs(self.package_folder, exist_ok=True)
        jinja2_env = jinja2.Environment(
            loader= jinja2.FileSystemLoader(os.path.join(self.source_folder, "packaging")), 
            trim_blocks=True, 
            lstrip_blocks=True, 
            undefined=jinja2.StrictUndefined)
        jinja2_package_template = jinja2_env.get_template("package.iss.j2")

        jinja_model = {
            'name' : self.name,
            'description' : self.description,
            'version' : self.version,
            'author' : self.author,
            'options' : self.options,
            'url' : self.url,   
            'output_dir' : self.package_folder,
            'output_base_name' : "%s-%s-%s%s" % (self.name, self.version, self.settings.arch, self._installertype),
            'python_temp' : os.path.join(self.source_folder, "python_temp"),
            'conan_temp' : os.path.join(self.source_folder, "conan_temp")
            }

        with open("package.iss", 'w') as f:
            f.write(jinja2_package_template.render(jinja_model))

        iscc_command= ["iscc", "/Q"]
        iscc_command.append("package.iss")
        subprocess.call(iscc_command)

    def package(self):
        self.copy("README.md")
        self.copy("README.txt")
        self.copy("LICENSE.txt")
        self.copy("%s-%s-%s%s.exe" % (self.name, self.version, self.settings.arch, self._installertype))
