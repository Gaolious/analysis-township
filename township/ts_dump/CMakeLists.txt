##############################################
##############################################

cmake_minimum_required(VERSION 3.10.2)

project (ts_dump CXX)

##############################################
# set BINARY, INC_PATH, SRCS
##############################################
SET(BINARY ts_dump)
SET(INC_PATH ${CMAKE_CURRENT_SOURCE_DIR})
file(GLOB SRCS "src/*.cpp")

add_executable(${BINARY} ${SRCS})

file(COPY
        ${CMAKE_CURRENT_SOURCE_DIR}/inc
        DESTINATION ${CMAKE_BINARY_DIR}/bin
        )
file(COPY
        ${CMAKE_CURRENT_SOURCE_DIR}/x86
        DESTINATION ${CMAKE_BINARY_DIR}/bin
        )

target_include_directories(${BINARY}
    PUBLIC
    ${INC_PATH}
)

TARGET_LINK_LIBRARIES(${BINARY}
        ts_util
        ts_http
        ts_xml
    )
