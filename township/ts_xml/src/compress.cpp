#include <inc/types.h>

#include <zlib.h>
#include <stdlib.h>
#include <string.h>

#define TS_ZLIB_LEVEL (-1)
#define TS_ZLIB_METHOD (8)
#define TS_ZLIB_WINDOW_BITS (31)
#define TS_ZLIB_MEM_LEVEL (8)
#define TS_ZLIB_STRATEGY (0)

const int CHUNK = 1024 ;
//int __cdecl sub_1D6E942(int a1, unsigned int a2, _DWORD *a3)
bool ts_compress(_BYTE *message, unsigned int size, TSBINARY *pCompressed)
{
    int len ;
    int have ;
    unsigned char buff_in[ CHUNK ];
    unsigned char buff_out[ CHUNK ];
    z_stream strm = {0, };
    int err;

    deflateInit2(&strm, TS_ZLIB_LEVEL, TS_ZLIB_METHOD, TS_ZLIB_WINDOW_BITS, TS_ZLIB_MEM_LEVEL, TS_ZLIB_STRATEGY );

    pCompressed->clear();

    for ( int i = 0 ; i < size ; i += CHUNK)
    {
        len = (size - i ) > CHUNK ? CHUNK : (size-i) ;
        memcpy( buff_in, message + i, len );
        strm.avail_in = len ;
        strm.next_in = buff_in;

        do {
            strm.avail_out = CHUNK;
            strm.next_out = buff_out;

            err = deflate(&strm, Z_NO_FLUSH);
            if ( err == Z_STREAM_ERROR ) return false ;
            have = CHUNK - strm.avail_out ;
            pCompressed->insert(pCompressed->end(), buff_out, buff_out + have );
        } while ( strm.avail_out == 0 );
    }
    return true;
}

bool ts_decompress(_BYTE *message, unsigned int size, TSBINARY *pDecompressed)
{
    unsigned int len ;
    unsigned char buff_in[ CHUNK ];
    unsigned char buff_out[ CHUNK ];
    unsigned int have ;
    TSBINARY out ;
    z_stream strm = {0, };
    _BYTE *in;
    int err;

    err = inflateInit2(&strm, TS_ZLIB_WINDOW_BITS);

    pDecompressed->clear();

    for ( int i = 0 ; i < size ; i += CHUNK)
    {
        len = ( size - i ) > CHUNK ? CHUNK : size - i;

        memcpy( buff_in, message + i, len);
        strm.avail_in = len ;
        strm.next_in = buff_in ;
        if ( strm.avail_in == 0 ) break;

        do
        {
            strm.avail_out = CHUNK,
            strm.next_out = buff_out;
            err = inflate(&strm, Z_NO_FLUSH);
            if ( err == Z_STREAM_ERROR ) return false ;
            have = CHUNK - strm.avail_out ;
            pDecompressed->insert(pDecompressed->end(), buff_out, buff_out + have);
        } while ( strm.avail_out == 0 );
    }
    inflateEnd(&strm);
    return true ;
}