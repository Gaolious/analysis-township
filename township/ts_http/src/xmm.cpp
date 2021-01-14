
#include <inc/xmm.h>

__m128i _mm_loadu_si128 (__m128i const* mem_addr)
{
    return *mem_addr;
}
__m128i _mm_load_si128 (__m128i const* mem_addr)
{
    return *mem_addr;
}

void _mm_store_si128 (__m128i* mem_addr, __m128i a)
{
    *mem_addr = a ;
}
void _mm_storeu_si128 (__m128i* mem_addr, __m128i a)
{
    *mem_addr = a ;
}

__m128i _mm_slli_epi64 (__m128i a, int n)
{
    __m128i b = a ;
    b.m128i_u64[1] <<= n;
    return b;
}
__m128i _mm_srli_epi64(__m128i a, int n)
{
    __m128i b = a ;
    b.m128i_u64[1] >>= n;
    return b;
}

__m128i _mm_xor_si128 (__m128i a, __m128i b)
{
    int i ;
    __m128i ret ;
    for ( i = 0 ; i < sizeof(a.m128i_u64) / sizeof(a.m128i_u64[0]) ; i ++ )
        ret.m128i_u64[ i ] = a.m128i_u64[ i ] ^ b.m128i_u64[ i ] ;
    return ret ;
}
__m128i _mm_or_si128 (__m128i a, __m128i b)
{
    int i ;
    __m128i ret ;
    for ( i = 0 ; i < sizeof(a.m128i_u64) / sizeof(a.m128i_u64[0]) ; i ++ )
        ret.m128i_u64[ i ] = a.m128i_u64[ i ] | b.m128i_u64[ i ] ;
    return ret ;
}
__m128i _mm_and_si128 (__m128i a, __m128i b)
{
    int i ;
    __m128i ret ;
    for ( i = 0 ; i < sizeof(a.m128i_u64) / sizeof(a.m128i_u64[0]) ; i ++ )
        ret.m128i_u64[ i ] = a.m128i_u64[ i ] & b.m128i_u64[ i ] ;
    return ret ;
}