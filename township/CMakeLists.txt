cmake_minimum_required(VERSION 3.10.2)

SET ( CMAKE_BUILD_TYPE Debug )
set(CMAKE_BUILD_TYPE RelWithDebInfo)
SET ( CMAKE_C_FLAGS_DEBUG  "-g" )
SET ( CMAKE_CXX_FLAGS_DEBUG  "-g" )

set(CMAKE_C_COMPILER /usr/bin/gcc)
set(CMAKE_CXX_COMPILER /usr/bin/g++)


set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/lib" CACHE PATH "Archive output dir.")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/lib" CACHE PATH "Library output dir.")
set(CMAKE_PDB_OUTPUT_DIRECTORY     "${CMAKE_CURRENT_SOURCE_DIR}/bin" CACHE PATH "PDB (MSVC debug symbol)output dir.")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/bin" CACHE PATH "Executable/dll output dir.")

#################################################
# PROJECT
#################################################
project (township CXX)

#################################################
# for Google Test
#################################################
enable_testing()

#################################################
# sub
#################################################
add_subdirectory(ts_util)
add_subdirectory(ts_http)
add_subdirectory(ts_xml)
add_subdirectory(zlib-1.2.11)
add_subdirectory(ts_dump)
add_subdirectory(jsoncpp-1.9.4)
##############################################
# set BINARY, INC_PATH, SRCS
##############################################
file(GLOB SRCS "src/*.cpp")

add_executable(${PROJECT_NAME} ${SRCS})

target_link_libraries(${PROJECT_NAME}
    PUBLIC
    ts_util
    ts_http
    ts_xml
    pthread
    ssl
    crypto
)
