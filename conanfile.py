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
        self.Cmd1 = extra_call + "call \"%" + CommonToolsEnv + "%..\\..\\VC\\" + extra_path + "vcvarsall.bat\" " + Architecture + " &amp; cmd /k \"\"%ConEmuDir%\\..\\init.bat\"\""
        self.Count = "1"
        self.Hotkey = "0"
        self.Flags = "0"
        self.Active = "1"

class BarbarianConan(ConanFile):
    name = "Barbarian"
    version = "1.9.2"
    _cmder_version = "1.3.18"
    _cmder_version_build = "%s.1106" % _cmder_version
    _cmder_sha256 = "2196bc1880a711c72f2b86df07f7533b72b085fb167d8566d941f0b9a41b5510"
    _git_version = "2.31.1"
    _git_sha256 = "fce2161a8891c4deefdb8d215ab76498c245072f269843ef1a489c4312baef52"
    _python_version = "3.7.9"
    _conan_version = "1.31.4"
    _vswhere_version = "2.8.4"
    _vswhere_sha256="e50a14767c27477f634a4c19709d35c27a72f541fb2ba5c3a446c80998a86419"
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

    def build_requirements(self):
        self.build_requires("7zip/19.00")
        self.build_requires("InnoSetup/6.1.2@%s/%s" % (self.user, self.channel))
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
        tools.download("https://github.com/cmderdev/cmder/releases/download/v%s/cmder_mini.zip" % (self._cmder_version), "cmder_mini.zip", sha256=self._cmder_sha256)
        #tools.download("https://github.com/git-for-windows/git/releases/download/v%s.windows.%s/PortableGit-%s-64-bit.7z.exe" % (".".join(self._git_version.split(".")[0:3]), self._git_version.split(".")[3], self._git_version), "git-for-windows.7z.exe", sha256=self._git_sha256)
        git_versions = self._git_version.split(".")
        if len(git_versions) < 4:
            git_versions.append("1")
        tools.download("https://github.com/git-for-windows/git/releases/download/v%s.windows.%s/PortableGit-%s-64-bit.7z.exe" % (".".join(git_versions[0:3]), git_versions[3],  self._git_version), "git-for-windows.7z.exe", sha256=self._git_sha256)
        # Requirements for pip
        self._url_download_to_temp("https://bootstrap.pypa.io/get-pip.py", temp_name="python_temp")
        # Download vswhere
        tools.download("https://github.com/microsoft/vswhere/releases/download/%s/vswhere.exe" % self._vswhere_version, "vswhere.exe", sha256=self._vswhere_sha256)
        # Basic packages
        self._pip_download_to_temp("pip", temp_name="python_temp")
        self._pip_download_to_temp("wheel", temp_name="python_temp")
        self._pip_download_to_temp("setuptools", temp_name="python_temp")
        # Requirements for conan
        self._pip_tar2whl_to_temp("conan==%s" % self._conan_version, temp_name="conan_temp")
        self._pip_tar2whl_to_temp("future==0.18.2", temp_name="conan_temp")
        self._pip_tar2whl_to_temp("patch-ng==1.17.4", temp_name="conan_temp")
        self._pip_tar2whl_to_temp("pluginbase==1.0.0", temp_name="conan_temp")
        self._pip_download_to_temp("conan==%s" % self._conan_version, temp_name="conan_temp")
        tools.download("https://raw.githubusercontent.com/conan-io/conan/develop/LICENSE.md", "conanio-LICENSE.txt")
         
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
        shutil.copyfile(os.path.join(self.source_folder, "documentation", "logo", "Barbarian.ico"), os.path.join(self.build_folder, self.name, "%s.ico" % self.name))
        shutil.copyfile(os.path.join(self.source_folder, "documentation", "logo", "Barbarian128.png"), os.path.join(self.build_folder, self.name, "%s.png" % self.name))

        # 1c. Append to license
        self._append_to_license_txt("Barbarian", "https://github.com/kwallner/Barbarian", "A Software Development Environment for Conan.io", os.path.join(self.build_folder, self.name, "LICENSE.txt"))
        
        # 1c. Append License of cmder
        self._append_to_license_txt("Cmder", "http://cmder.net/", "Console emulator for Windows", os.path.join(self.build_folder, self.name, "LICENSE-cmder.txt"))
        os.remove(os.path.join(self.build_folder, self.name, "LICENSE-cmder.txt"))
        self._append_to_license_txt("clink-completions", "https://github.com/vladimir-kotikov/clink-completions", "Completion files to clink util", os.path.join(self.build_folder, self.name, "vendor", "clink-completions", "LICENSE"))
        self._append_to_license_txt("ConEmu", "https://conemu.github.io/", "Handy Windows Terminal", os.path.join(self.build_folder, self.name, "vendor", "conemu-maximus5", "ConEmu", "License.txt"))

        # 1d. Update/Replace ConEmu.xml
        self._update_conemu_xml_config()

        # 2. Git
        subprocess.call(["7z", "x", os.path.join(self.source_folder, "git-for-windows.7z.exe"), "-o%s/%s" % (self.name, "vendor/git-for-windows") ])
        # No need for install script. Git is already included (so do not change name)
        os.linesep= '\r\n'
        with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "02_git-for-windows.cmd"), 'w') as f:
            f.write(':: Vendor: git support\n')
            path = os.path.join("%CMDER_ROOT%", "vendor", "git-for-windows", "cmd")
            f.write('set "PATH={0};%PATH%"\n'.format(path))
            path = os.path.join("%CMDER_ROOT%", "vendor", "git-for-windows", "mingw64", "bin")
            f.write('set "PATH={0};%PATH%"\n'.format(path))
            path = os.path.join("%CMDER_ROOT%", "vendor", "git-for-windows", "usr", "bin")
            f.write('set "PATH={0};%PATH%"\n'.format(path))
        os.linesep= '\r\n'
        with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "02_git-for-windows.ps1"), 'w') as f:
            f.write('# Vendor: git support\n')
            path = os.path.join("$env:CMDER_ROOT", "vendor", "git-for-windows", "cmd")
            f.write('$env:PATH="PATH={0};" + $env:PATH\n'.format(path))
            path = os.path.join("$env:CMDER_ROOT", "vendor", "git-for-windows", "mingw64", "bin")
            f.write('$env:PATH="PATH={0};" + $env:PATH\n'.format(path))
            path = os.path.join("$env:CMDER_ROOT", "vendor", "git-for-windows", "usr", "bin")
            f.write('$env:PATH="PATH={0};" + $env:PATH\n'.format(path))
        os.linesep= '\n'
        with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "02_git-for-windows.sh"), 'w') as f:
            f.write('# Vendor: git support\n')
            # Pathes are already correct
        self._append_to_license_txt("Git", "https://git-scm.com", "Distributed version control system", os.path.join(self.build_folder, self.name, "vendor", "git-for-windows", "LICENSE.txt"))
        # Git postinstall
        os.linesep= '\r\n'
        with open(os.path.join(self.build_folder, self.name, "vendor", "git-for-windows", "post-install.bat"), 'w') as f:
            f.write('@echo off\n')
            f.write('rem Git Postinstall\n')
            f.write('\n')
            f.write('rem Removing this script\n')
            f.write('(goto) 2>nul & del "%~f0"\n')
        
        # 3. Python
        shutil.copytree(self.deps_cpp_info["cpython"].rootpath,  os.path.join(self.name, "vendor", "python-for-windows"), ignore = shutil.ignore_patterns('conan*.txt'))
        os.linesep= '\r\n'
        with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "03_python-for-windows.cmd"), 'w') as f:
            f.write(':: Vendor: python support\n')
            path = os.path.join("%CMDER_ROOT%", "vendor", "python-for-windows")
            f.write('set "PATH={0};%PATH%"\n'.format(path))
            path = os.path.join("%CMDER_ROOT%", "vendor", "python-for-windows", "Scripts")
            f.write('set "PATH={0};%PATH%"\n'.format(path))
        os.linesep= '\r\n'
        with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "03_python-for-windows.ps1"), 'w') as f:
            f.write('# Vendor: python support\n')
            path = os.path.join("$env:CMDER_ROOT", "vendor", "python-for-windows")
            f.write('$env:PATH="{0};" + $env:PATH\n'.format(path))
            path = os.path.join("$env:CMDER_ROOT", "vendor", "python-for-windows", "Scripts")
            f.write('$env:PATH="{0};" + $env:PATH\n'.format(path))
        os.linesep= '\n'
        with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "03_python-for-windows.sh"), 'w') as f:
            f.write('# Vendor: python support\n')
            path = os.path.join("$CMDER_ROOT", "vendor", "python-for-windows").replace("\\", "/")
            f.write('export "PATH={0}:$PATH"\n'.format(path))
            path = os.path.join("$CMDER_ROOT", "vendor", "python-for-windows", "Scripts").replace("\\", "/")
            f.write('export "PATH={0}:$PATH"\n'.format(path))
        self._append_to_license_txt("Python", "https://python.org/", "Python Programming Language ",os.path.join(self.name, "vendor", "python-for-windows", "LICENSE"))

        # 4. Conan.io
        self._append_to_license_txt("Conan.io", "https://conan.io/", "C/C++ Package Manager", os.path.join(self.source_folder, "conanio-LICENSE.txt"))

        # 5. Conan Environment Activate
        os.mkdir(os.path.join(self.build_folder, self.name, "vendor", "barbarian-conan_env"))
        # Create conanfile.txt
        os.linesep= '\r\n'
        with open(os.path.join(self.build_folder, self.name, "config", "conan_env.txt"), 'wt') as f:
            f.write('[generators]\n')
            f.write('virtualenv\n')
            f.write('[build_requires]\n')
        shutil.copyfile(
            os.path.join(self.build_folder, self.name, "config", "conan_env.txt"), 
            os.path.join(self.build_folder, self.name, "vendor", "barbarian-conan_env", "conanfile.txt"))
        # Create automation script
        os.linesep= '\r\n'
        with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "05_barbarian-conan_env.cmd"), 'w') as f:
            f.write(':: Vendor: conan activate support\n')
            conan_env_path = os.path.join("%CMDER_ROOT%", "vendor", "barbarian-conan_env")
            f.write('pushd "{0}"\n'.format(conan_env_path))
            f.write('copy ..\\..\\config\\conan_env.txt conanfile.txt\n')
            #f.write('"%CMDER_ROOT%\\vendor\\python-for-windows\\Scripts\\conan" install --update .\n')
            f.write('conan install --update .\n')
            f.write('call activate.bat\n')
            f.write('set "PROMPT=%CONAN_OLD_PROMPT%"\n')
            f.write('popd\n')
        os.linesep= '\r\n'
        with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "05_barbarian-conan_env.ps1"), 'w') as f:
            f.write('# Vendor: conan activate support\n')
            conan_env_path = os.path.join("$env:CMDER_ROOT", "vendor", "barbarian-conan_env")
            f.write('copy ..\\..\\config\\conan_env.txt conanfile.txt\n')
            f.write('pushd "{0}"\n'.format(conan_env_path))
            #f.write('"%CMDER_ROOT%\\vendor\\python-for-windows\\Scripts\\conan" install --update .\n')
            f.write('conan install --update .\n')
            f.write('. .\\activate.ps1\n')
            f.write('popd\n')
        os.linesep= '\n'
        with open(os.path.join(self.build_folder, self.name, "config", "profile.d", "05_barbarian-conan_env.sh"), 'w') as f:
            f.write('# Vendor: conan activate support\n')
            conan_env_path = os.path.join("$CMDER_ROOT", "vendor", "barbarian-conan_env").replace("\\", "/")
            f.write('pushd "{0}"\n'.format(conan_env_path))
            f.write('cp -f ../../config/conan_env.txt conanfile.txt\n')
            #f.write('"%CMDER_ROOT%/vendor/python-for-windows/Scripts/conan" install --update .\n')
            f.write('conan install --update .\n')
            f.write('. ./activate.sh\n')
            f.write('export PS1="$CONAN_OLD_PS1"\n')
            f.write('popd\n')

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
            'output_base_name' : "%s-%s-%s" % (self.name, self.version, self.settings.arch),
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
        self.copy("%s-%s-%s.exe" % (self.name, self.version, self.settings.arch))
