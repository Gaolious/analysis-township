find_package(Threads REQUIRED)
find_package(GTest)

file(GLOB SRCS *.cpp)
SET(BINARY test_ts_util)

ADD_EXECUTABLE(${BINARY} ${SRCS})

add_test(NAME ${BINARY} COMMAND ${BINARY})

TARGET_LINK_LIBRARIES(${BINARY}
    gtest_main
    gtest
    pthread
    ts_util
)

