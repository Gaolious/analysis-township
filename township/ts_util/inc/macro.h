#ifndef _MACRO_HEADER_FILE_INCLUDED_
#define _MACRO_HEADER_FILE_INCLUDED_

#define SAFE_DELETE(x) do { \
    if ( (x) == NULL ) \
        break; \
    delete [](x); \
    (x) = NULL ; \
} while (0)



#define u8p(x) ( (_BYTE *)(x) )
#define u16p(x) ( (_WORD *)(x) )
#define u32p(x) ( (_DWORD *)(x) )
#define u64p(x) ( (_QWORD *)(x) )
#define u128p(x) ( (_DQWORD *)(x) )

// RB0(1111 1111 2222 2222 3333 3333 4444 4444) => 0000 0000 0000 0000 0000 0000 4444 4444
// RB1(1111 1111 2222 2222 3333 3333 4444 4444) => 0000 0000 0000 0000 0000 0000 3333 3333
// RB2(1111 1111 2222 2222 3333 3333 4444 4444) => 0000 0000 0000 0000 0000 0000 2222 2222
// RB3(1111 1111 2222 2222 3333 3333 4444 4444) => 0000 0000 0000 0000 0000 0000 1111 1111
#define RB0(x) ( ( (_DWORD)(x) >> 0u  ) & 0xFFu  )
#define RB1(x) ( ( (_DWORD)(x) >> 8u  ) & 0xFFu  )
#define RB2(x) ( ( (_DWORD)(x) >> 16u ) & 0xFFu  )
#define RB3(x) ( ( (_DWORD)(x) >> 24u ) & 0xFFu  )

// LB1(1111 1111 2222 2222 3333 3333 4444 4444) => 0000 0000 0000 0000 4444 4444 0000 0000
// LB2(1111 1111 2222 2222 3333 3333 4444 4444) => 0000 0000 4444 4444 0000 0000 0000 0000
#define LB0(x) ( ( (_DWORD)(x) << 0u  ) & 0x000000FFu)
#define LB1(x) ( ( (_DWORD)(x) << 8u  ) & 0x0000FF00u)
#define LB2(x) ( ( (_DWORD)(x) << 16u ) & 0x00FF0000u)
#define LB3(x) ( ( (_DWORD)(x) << 24u ) & 0xFF000000u)

#endif