cmake_minimum_required(VERSION 3.10.2)

# SET ( CMAKE_BUILD_TYPE Debug )

SET(CMAKE_C_FLAGS_DEBUG "-g -O0")

set(CMAKE_C_COMPILER /usr/bin/gcc)
set(CMAKE_CXX_COMPILER /usr/bin/g++)

#################################################
# PROJECT
#################################################
project(encode CXX)


set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/lib" CACHE PATH "Archive output dir.")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/lib" CACHE PATH "Library output dir.")
# set(CMAKE_PDB_OUTPUT_DIRECTORY     "${CMAKE_BINARY_DIR}/bin" CACHE PATH "PDB (MSVC debug symbol)output dir.")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}" CACHE PATH "Executable/dll output dir.")

##############################################
# set BINARY, INC_PATH, SRCS
##############################################
set(BINARY ${PROJECT_NAME})
file(GLOB SRCS "src/*.cpp")
file(GLOB INCS "src/*.cpp")

add_executable(${BINARY} ${SRCS} ${INCS})

target_include_directories(${BINARY}
        PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}
        )