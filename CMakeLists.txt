cmake_minimum_required(VERSION 2.8.12)
project(cmake_wrapper)

include(conanbuildinfo.cmake)
conan_basic_setup()

if("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU")
  add_definitions("-Wno-cast-qual")
  add_definitions("-Wno-ctor-dtor-privacy")
endif()

add_subdirectory("source_subfolder")
