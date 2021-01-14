find_package(Threads REQUIRED)
find_package(GTest)

file(GLOB SRCS *.cpp)
SET(BINARY test_ts_xml)

ADD_EXECUTABLE(${BINARY} ${SRCS} test_decode.cpp)

add_test(NAME ${BINARY} COMMAND ${BINARY})

TARGET_LINK_LIBRARIES(${BINARY}
    gtest_main
    gtest
    pthread
    ts_xml
)

