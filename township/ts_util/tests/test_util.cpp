#include <gtest/gtest.h>

#include <inc/types.h>
#include <inc/utils.h>

/////////////////////////////////////////////////////////////////////////////
// Google Test Naming Category
//
// Prefix      TestCase Name     Test Name
// TestTSXML > TestMurMur2Hash > ShouldReturnExpectedValue_WhenGivenData
//
// TEST_P(TestCaseName, TestName)
/////////////////////////////////////////////////////////////////////////////

namespace TEST_UTIL
{
    TEST(Test_ReverseByte, CheckReverseByte){
        EXPECT_EQ(0x11, ReverseByte((_BYTE) 0x11) );

        EXPECT_EQ(0x2211, ReverseByte((_WORD) 0x1122) );

        EXPECT_EQ(0x44332211u, ReverseByte((_DWORD) 0x11223344u) );

        EXPECT_EQ(0x8877665544332211ull, ReverseByte((_QWORD) 0x1122334455667788u) );
    }

    TEST(Test_HIDWORD, CheckHIDWORD)
    {
        _QWORD a = 0x1122334455667788ull;
        EXPECT_EQ( HIDWORD(a),  0x11223344u );
    }

    TEST(Test_LODWORD, CheckLODWORD)
    {
        _QWORD a = 0x1122334455667788ull;
        EXPECT_EQ( LODWORD(a),  0x55667788u );
    }

    TEST(Test_HIWORD, CheckHIWORD)
    {
        _DWORD a = 0x11223344u;
        EXPECT_EQ( HIWORD(a),  0x1122u );
    }

    TEST(Test_LOWORD, CheckLOWORD)
    {
        _DWORD a = 0x11223344u;
        EXPECT_EQ( LOWORD(a),  0x3344u );
    }

    TEST(Test_SHLD, CheckSHLD)
    {
        _DWORD EAX = 0x01234567u;
        _DWORD EBX = 0x89ABCDEFu;

        EXPECT_EQ( shld(EAX, EBX, 4), 0x12345678u );
        //-----------------------------
        //SHLD EAX,EBX,4
        //EAX = 0x12345678
        //-----------------------------
        //SHRD EAX,EBX,4
        //EAX = 0xF0123456
    }
    TEST(Test_SHRD, CheckSHRD)
    {
        _DWORD EAX = 0x01234567u;
        _DWORD EBX = 0x89ABCDEFu;

        EXPECT_EQ( shrd(EAX, EBX, 4), 0xF0123456u );
        //-----------------------------
        //SHLD EAX,EBX,4
        //EAX = 0x12345678
        //-----------------------------
        //SHRD EAX,EBX,4
        //EAX = 0xF0123456
    }
}