from conans import ConanFile, tools
from subprocess import call
import os
import shutil

class BarbarianConan(ConanFile):
	name = "Barbarian"
	version = "1.3.6"
	generators = "txt", "virtualenv"
	url = "http://github.com/kwallner/Barbarian"
	settings = {"os": ["Windows"], "arch": ["x86_64"]}
	exports_sources = [ "LICENSE.txt", "README.md" ]
	no_copy_source = True
	#options = {"with_git": [True, False], "with_cmake": [True, False], "with_python": [True, False], "with_conanio": [True, False], "with_vscode": [True, False], "with_vim": [True, False]}
	#default_options = "with_git=True", "with_cmake=True", "with_python=True", "with_conanio=True", "with_vscode=True", "with_vim=True"
	options = {"with_cmake": [True, False],  "with_conanio": [True, False], "with_vim": [True, False], "with_vscode": [True, False]}
	default_options = "with_cmake=True", "with_conanio=True", "with_vim=True"

	def build_requirements(self):
		self.build_requires("7z_installer/1.0@conan/stable")

	def source(self):
		tools.download("https://github.com/cmderdev/cmder/releases/download/v1.3.6/cmder.zip", "cmder.zip")
		tools.download("https://cmake.org/files/v3.12/cmake-3.12.0-win64-x64.zip", "cmake-win64.zip")
		tools.download("https://repo.continuum.io/miniconda/Miniconda3-latest-Windows-x86_64.exe", "Miniconda3.exe")
		#tools.download("https://go.microsoft.com/fwlink/?Linkid=850641", "vscode-win64.zip")
		tools.download("https://bintray.com/veegee/generic/download_file?file_path=vim7.4.2207_x64.exe", "vim7.4.2207_x64.exe", verify=False)
		
	def build(self):
		# 1. Cmder
		tools.unzip(os.path.join(self.source_folder, "cmder.zip"))

		# Create profile directory
		tools.mkdir(os.path.join(self.build_folder, "config", "profile.d"))
		
		# 3. CMake
		if self.options.with_cmake:
			tools.unzip(os.path.join(self.source_folder, "cmake-win64.zip"), destination = "vendor")
			os.rename(os.path.join(self.build_folder, "vendor", "cmake-3.12.0-win64-x64"), os.path.join(self.build_folder, "vendor", "cmake-for-windows"))

			with open(os.path.join(self.build_folder, "config", "profile.d", "cmake-for-windows.cmd"), 'w') as f:
				f.write(':: Vendor: cmake support\n')
				path = os.path.join("%CMDER_ROOT%", "vendor", "cmake-for-windows", "bin")
				f.write('set "PATH={0};%PATH%"'.format(path))

		# 4. Python
		call([os.path.join(self.source_folder, "Miniconda3.exe"), "/InstallationType=JustMe", "/RegisterPython=0", "/S", "/AddToPath=0", "/D=%s" %(os.path.join(self.build_folder, "vendor", "Miniconda3")) ])

		# 5. Conan.io
		if self.options.with_conanio:
			# If a specific version of conan should be used change "conan" to e.g. "conan==1.4.4"
			call([os.path.join(self.build_folder, "vendor", "Miniconda3", "python.exe"), "-m", "pip", "install", "conan", "--no-warn-script-location"])

		# 6. vim 
		if self.options.with_vim:
			call(["7z", "x", os.path.join(self.source_folder, "vim7.4.2207_x64.exe"), "-aoa", "-o%s" % (os.path.join(self.build_folder, "vendor", "vim-for-windows"))])
			
			with open(os.path.join(self.build_folder, "config", "profile.d", "vim-for-windows.cmd"), 'w') as f:
				f.write(':: Vendor: vim support\n')
				path = os.path.join("%CMDER_ROOT%", "vendor", "vim-for-windows", "vim74")
				f.write('set "PATH={0};%PATH%"'.format(path))

		# # 7. VS Code + Extensions
		# if self.options.with_vscode:
		# 	tools.unzip(os.path.join(self.source_folder, "vscode-win64.zip"), destination = os.path.join("vendor", "vscode-for-windows"))
		# 	path=os.path.join(self.build_folder, "vender", "vscode-for-windows", "bin", "code.cmd")
		# 	call([path, "--install-extension", "ms-vscode.cpptools"])
		# 	call([path, "--install-extension", "ms-python.python"])
		# 	call([path, "--install-extension", "MS-CEINTL.vscode-language-pack-de"])
		# 	call([path, "--install-extension", "PeterJausovec.vscode-docker"])
		# 	call([path, "--install-extension", "twxs.cmake"])


		# 	with open(os.path.join("config", "profile.d", "vscode-for-windows.cmd"), 'w') as f:
		# 		path = os.path.join(self.build_folder, "%CMDER_ROOT%", "vendor", "vscode-for-windows")
		# 		f.write(':: Vendor: vscode support\n')
		# 		f.write('set "PATH={0};%PATH%"\n'.format(path))
		# 		f.write('\n')
			
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
			self.env_info.path.insert(0, os.path.join(self.package_folder, "vendor", "cmake-for-windows", "bin"))
		if self.options.with_vim:
			self.env_info.path.insert(0, os.path.join(self.package_folder, "vendor", "vim-for-windows", "vim74"))
		# if self.options.with_vscode:
		#  	self.env_info.path.insert(0, os.path.join(self.package_folder, "vendor", "vscode-for-windows"))
		
		self.env_info.path.insert(0, os.path.join(self.package_folder, "bin"))
		self.env_info.path.insert(0, self.package_folder)
