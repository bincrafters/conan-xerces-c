# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class LibnameConan(ConanFile):
    name = "xerces-c"
    version = "3.2.2"
    description = "Xerces-C++ is a validating XML parser written in a portable subset of C++"
    topics = ("conan", "xerces", "XML", "validation", "DOM", "SAX", "SAX2")
    url = "https://github.com/bincrafters/conan-xerces-c"
    homepage = "http://xerces.apache.org/xerces-c/index.html"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "	Apache-2.0"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    # Options may need to change depending on the packaged library.
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        source_url = "http://apache.rediris.es//xerces/c/3/sources/xerces-c-{}.tar.bz2".format(self.version)
        tools.get(source_url, sha256="1f2a4d1dbd0086ce0f52b718ac0fa4af3dc1ce7a7ff73a581a05fbe78a82bce0")
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        # https://xerces.apache.org/xerces-c/build-3.html
        # TODO : check if we need options for that variants
        cmake.definitions["network-accessor"] = {"Windows": "winsock",
                                                 "Macos": "cfurl",
                                                 "Linux": "socket"}.get(str(self.settings.os))
        cmake.definitions["transcoder"] = {"Windows": "windows",
                                           "Macos": "macosunicodeconverter",
                                           "Linux": "gnuiconv"}.get(str(self.settings.os))
        cmake.definitions["message-loader"] = "inmemory"
        cmake.definitions["xmlch-type"] = "uint16_t"
        cmake.definitions["mutex-manager"] = {"Windows": "windows",
                                              "Macos": "posix",
                                              "Linux": "posix"}.get(str(self.settings.os))
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["xerces-c"]
        if self.settings.os == "Macos":
            frameworks = ['CoreFoundation', 'CoreServices']
            for framework in frameworks:
                self.cpp_info.exelinkflags.append("-framework %s" % framework)
            self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags
        elif self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
