#include <gtest/gtest.h>

#include <inc/xmm.h>
#include <tuple>
using namespace std;

/////////////////////////////////////////////////////////////////////////////
// Google Test Naming Category
//
// Prefix      TestCase Name     Test Name
// TestTSXML > TestMurMur2Hash > ShouldReturnExpectedValue_WhenGivenData
//
// TEST_P(TestCaseName, TestName)
/////////////////////////////////////////////////////////////////////////////


namespace ns_http_aes_xmm
{
    // __m128i xmmword_0284F970 = { .m128i_u8 = {0x00, 0x00, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00}};
    struct TestXMM : public ::testing::TestWithParam<tuple<__m128i,__m128i>>{};

    TEST_P(TestXMM, ShouldReturnExpectedValue_WhenGivenData){
        int i ;
        tuple<__m128i,__m128i> p = GetParam();
        __m128i in = std::get<0>(p);
        __m128i out = std::get<1>(p);

        __m128i ret = _mm_slli_epi64(in, 3u);

        for ( i = 0 ; i < 2 ; i ++ )
            EXPECT_EQ(out.m128i_u64[i], ret.m128i_u64[i]);
    }

    INSTANTIATE_TEST_CASE_P(
        TestTsHttp,
        TestXMM,
        ::testing::Values(
            make_tuple(
                __m128i{ .m128i_u8 = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xC9, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00} },
                __m128i{ .m128i_u8 = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x48, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00} }
            )
        )
    );
}
