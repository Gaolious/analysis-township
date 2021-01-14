#include <gtest/gtest.h>

#include <inc/types.h>
#include <inc/http_header.h>

/////////////////////////////////////////////////////////////////////////////
// Google Test Naming Category
//
// Prefix      TestCase Name     Test Name
// TestTSXML > TestMurMur2Hash > ShouldReturnExpectedValue_WhenGivenData
//
// TEST_P(TestCaseName, TestName)
/////////////////////////////////////////////////////////////////////////////

namespace HTTP_HEADER_DECODE
{
    struct param {
        const char *ret ;
        int len ;
        const char *data;
    };
    struct TestHttpHeaderKey : public ::testing::TestWithParam<param>{};

    TEST_P(TestHttpHeaderKey, ShouldReturnExpectedValue_WhenGivenData){
        param p = GetParam();
        TSBINARY out ;
        TSBINARY in(p.data, p.data + p.len + 1 );
        decode_key( &in, &out);

        EXPECT_GT(out.size(), 1);
        EXPECT_EQ( out[ out.size() - 1 ], (_BYTE)0x00 );
        out.pop_back();

        EXPECT_EQ( p.len, out.size() );

        printf("%s\n", out.data());
        for ( int i = 0 ; i < p.len ; i ++ )
            EXPECT_EQ(p.ret[i] , out[i]);
    }
    
    INSTANTIATE_TEST_CASE_P(
        TestTsHttp,
        TestHttpHeaderKey,
        ::testing::Values(
            param{"SaveLocalInfo", 13, "WphNt*1>\x00\x30\xe8\xf5\xcf\xad"},
            param{"?cityId=", 8, "\x79\x2D\x3F\x2A\x1F\x27\x12\x43\x86"},
            param{"POST", 4, "\x1B\x00\x00\x03\x5B"},
            param{"ts-bver", 7, "\x38\x20\x77\x03\x1E\x0A\x04\x7D"},
            param{"ts-fver", 7, "\x39\x27\x76\x04\x1F\x15\x05\x7E"},
            param{"ts-bp", 5, "\x3A\x20\x75\x3F\x12\x67"},
            param{"ts-gpid", 7, "\x25\x2B\x72\x01\x1D\x1D\x1F\x82"},
            param{"AESENC", 6, "\x18\x1A\x36\x2E\x3F\x34\x7D"},
            param{"Content-type", 12, "\x19\x09\x1C\x0A\xEF\xF8\xD6\x83\xCE\xBF\xA2\xBB\xEA"},
            param{"application/octet-stream", 24, "\x3B\x02\xFA\xCE\xD3\xB1\x8B\x76\x73\x5D\x24\x4D\x15\xF1\xDE\xA7\xAE\xDF\x79\x56\x48\x37\x0B\xEF\x9A"},
            param{"AESENCZIP", 9, "\x1A\x21\x3E\x33\x31\xCB\xCB\xD3\xF3\xAC"},
            param{"002", 3, "\x55\x58\x59\x6E"},
            param{"ts-id", 5, "\x12\x18\x5D\x1C\x1E\x7F"},
            param{"Content-type", 12, "\x2A\x1A\xEF\xF9\xFC\xCB\xC5\x90\xBD\xAC\x91\x88\xF9"},
            param{"application/json", 16, "\x08\x09\xF9\xF5\xC0\xDA\xA8\xAD\x80\x96\x67\x36\x43\x4A\x26\x37\x69"},
            param{"001", 3, "\x5A\x5D\x41\x73"},
            param{"ts-id", 5, "\x1F\x03\x58\x13\x1B\x84"},
            param{"ts-token", 8, "\x02\x0D\xAB\xFA\xF9\xF5\xC3\xC0\xB6"},
            param{"SendDeviceId", 12, "\x2B\xE1\xFE\xF8\xEC\xD1\xB6\xA5\xBB\x81\xB9\x98\x08"},
            param{"deviceid", 8, "\x1D\xE4\xFF\xF8\xFA\xC4\xC0\xD5\xB9"},
            param{"SendDeviceInfo", 14, "\x28\xEC\xF9\xC1\xF7\xA4\xB9\xB4\x88\x9C\x4E\x7B\x45\x5E\x3F"},
            param{"device-info", 11, "\x18\xE2\xE4\xF4\xCB\xD6\x93\xA0\xBA\xB9\x85\xF5"},
            param{"DoRequest.UException", 20, "\xDD\xC2\x93\xB0\x98\x88\x74\x56\x4D\x63\x34\x30\xF1\xFE\xD4\xB5\xAD\x84\x6E\x7B\x29"},
            param{"DoRequest.Exception", 19, "\xD7\xC9\xEB\xA9\xAE\x87\x60\x6B\x5F\x10\x14\x1C\x14\xEF\xED\xC4\xAA\xB9\x87\xFC"},
            param{"Wucai6oj0sheiX3p", 16, "\xB3\x81\x67\x75\x4D\x02\x2B\x3E\x54\x07\xEC\xF1\xCD\xEC\xF7\xA4\xE4"}
        )
    );
}
