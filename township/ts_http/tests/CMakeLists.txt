find_package(Threads REQUIRED)
find_package(GTest)
SET ( CMAKE_C_FLAGS_DEBUG  "-g" )
SET ( CMAKE_CXX_FLAGS_DEBUG  "-g" )
file(GLOB SRCS *.cpp)
SET(BINARY test_ts_http)

ADD_EXECUTABLE(${BINARY} ${SRCS})

add_test(NAME ${BINARY} COMMAND ${BINARY})

TARGET_LINK_LIBRARIES(${BINARY}
    gtest_main
    gtest
    pthread
    ts_http
)

