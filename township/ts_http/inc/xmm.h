//
// Created by gaoli on 2020-12-02.
//

#include <inc/types.h>
#ifndef _TS_HTML_XMM_HEADER_FILE_INCLUDED_
#define _TS_HTML_XMM_HEADER_FILE_INCLUDED_

union __m128i {
    char            m128i_i8[16];
    short           m128i_i16[8];
    int             m128i_i32[4];
    long long       m128i_i64[2];
    unsigned char       m128i_u8[16];
    unsigned short      m128i_u16[8];
    unsigned int        m128i_u32[4];
    unsigned long long  m128i_u64[2];
} __attribute__(( aligned(1) )) ;

__m128i _mm_loadu_si128 (__m128i const* mem_addr);
__m128i _mm_load_si128 (__m128i const* mem_addr);

void _mm_store_si128 (__m128i* mem_addr, __m128i a);
void _mm_storeu_si128 (__m128i* mem_addr, __m128i a);

__m128i _mm_slli_epi64 (__m128i a, int imm8);
__m128i _mm_srli_epi64 (__m128i a, int imm8);

__m128i _mm_xor_si128 (__m128i a, __m128i b);
__m128i _mm_or_si128 (__m128i a, __m128i b);
__m128i _mm_and_si128 (__m128i a, __m128i b);

#endif
