##############################################
# static library
##############################################

cmake_minimum_required(VERSION 3.10.2)

##############################################
# set BINARY, INC_PATH, SRCS
##############################################
SET(BINARY ts_util)
SET(INC_PATH ${CMAKE_CURRENT_SOURCE_DIR})
file(GLOB SRCS "src/*.cpp")

add_library(${BINARY} STATIC ${SRCS})

target_include_directories(${BINARY}
    PUBLIC
    ${INC_PATH}
)

target_link_libraries(${BINARY}
        PUBLIC
        pthread
        ssl
        crypto
        jsoncpp_static
        )

add_subdirectory(tests)