#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from conans import ConanFile, CMake, tools

class LuajitConan(ConanFile):
    name = "luajit"
    version = "2.0.5"
    license = "MIT"
    url = "https://github.com/int010h/conan-luajit"
    homepage = "https://github.com/int010h/LuaJIT"
    description = "LuaJIT is a Just-In-Time (JIT) compiler for the Lua programming language."
    author = "Konstantin Nadejin <nadejin.konstantin@gmail.com>"
    topics = ("conan", "luajit", "lua", "jit")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    exports = "LICENSE"
    exports_sources = ["CMakeLists.txt", "luajit.patch"]
    generators = "cmake"
    _source_subfolder = "source_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        sha256 = "9ec8cb329922c9eb3854dc5e6433cfc8a7da81936afada34ede67f8c863a2e40"
        tools.get("{}/archive/v{}.tar.gz".format(self.homepage, self.version), sha256=sha256)
        extracted_dir = "LuaJIT-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure()
        return cmake

    def build(self):
        tools.patch(base_path=self._source_subfolder, patch_file="luajit.patch")
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("COPYRIGHT", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(["m", "dl"])
        self.env_info.path.append(os.path.join(self.package_folder, 'bin'))
