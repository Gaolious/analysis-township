#include <inc/types.h>
#include <inc/macro.h>

#ifndef _TS_UTIL_HEADER_FILE_INCLUDED_
#define _TS_UTIL_HEADER_FILE_INCLUDED_


template <typename T>
void _swap(T &a, T &b)
{
    T c = a ; 
    a = b ; 
    b = c;
}

template <typename T>
T ReverseByte(T a)
{
    int i, s, m;
    int shiftBits;
    T ret = 0, lmask, rmask ;

    s = sizeof(a);
    m = s / 2 ;
    if ( m < 1 ) return a ;

    for ( i = 0 ; i < m ; i ++ )
    {
        shiftBits = (m-i)*2 ;
        rmask = ( (T)0xFF ) << ( i * 8 );
        lmask = ( (T)0xFF ) << ((s-i-1) * 8);

        ret |= ( (a & rmask) << ((shiftBits-1) * 8));
        ret |= ( (a & lmask) >> ((shiftBits-1) * 8));
    }
    return ret ;
}

#define HIDWORD(x) (u32p(&x)[1])
#define LODWORD(x) (u32p(&x)[0])

#define HIWORD(x) (u16p(&x)[1])
#define LOWORD(x) (u16p(&x)[0])


template <typename T>
T shld(T a, T b, int shift)
{
    int i, s = sizeof(T)*8 ;
    _DWORD _a ;
    _DWORD _b ;

    shift %= s ;

    _a = a << shift;
    _b = b << shift ;
    _a |= b >> (s - shift) ;
    _b |= a >> (s - shift) ;
    return _a ;
}
template <typename T>
T shrd(T a, T &b, int shift)
{
    int i, s = sizeof(T)*8 ;
    _DWORD _a ;
    _DWORD _b ;

    shift %= s ;

    _a = a >> shift;
    _b = b >> shift ;
    _a |= b << (s - shift) ;
    _b |= a << (s - shift) ;
    return _a ;
}

// HEX String  : "A9 32 93 1F 91 A1 00 12"
// DATA String : "\xA9\x32\x93\x1F\x91\xA1\x00\x12
// DATA Array  : { 0xA9, 0x32, 0x93, 0x1F, 0x91, 0xA1, 0x00, 0x12 }
// DATA Literal : 0x1F9332A9u
// DATA Literal String : "0x1F9332A9u"

void DataToLiteralString(TSBINARY *pBuff, unsigned int offset, int datasize, TSBINARY *pOut);

bool readFile(TSBINARY *pFilename, TSBINARY *pOutBuff);
bool writeFile(TSBINARY *pFilename, TSBINARY *pInBuff, bool overwrite);

#endif