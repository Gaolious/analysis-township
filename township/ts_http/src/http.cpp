#include <stdio.h>
#include <sys/socket.h>

#include <string.h>
#include <stdlib.h>

#include <inc/compress.h>
#include <inc/aes.h>
#include <inc/http.h>

#include <openssl/ssl.h>
#include <inc/macro.h>

_BYTE HexToNum(_BYTE a)
{
    _BYTE ret = 0;
    if ( '0' <= a && a <= '9' ) ret = a - '0' ;
    else if ( 'a' <= a && a <= 'z' ) ret = a - 'a' + 10 ;
    else if ( 'A' <= a && a <= 'Z' ) ret = a - 'A' + 10 ;

    return ret & 0x0F ;
}
_BYTE HexToNum(_BYTE a, _BYTE b)
{
    _BYTE ret = ( HexToNum(a) << 4 ) | HexToNum(b);
    return ret & 0xFF;
}
_BYTE numToHex(_BYTE a)
{
    if ( a >= 0 && a <= 9 ) return a + '0';
    else return a - 10 + 'a' ;
}

// fixme : (call by value)TSBINARY to pointer
// text -> compress -> encode
bool encode_http_body(TSBINARY *in_compressed_body, TSBINARY *out_ts_id, TSBINARY *out_http_body)
{
    const char *strKey = "Wucai6oj0sheiX3p";
    int lenKey = strlen(strKey);
    _BYTE rand_data[12]={0,};
    int len_random_data = sizeof(rand_data) / sizeof(rand_data[0]);
    TSBINARY dest;
    int i, idx;

    srand(time(NULL));

    for ( i = 0 ; i < 3 ; i ++ )
        u32p(rand_data)[ i ] = rand() & 0xFFFFFFFF ;

    out_http_body->resize(in_compressed_body->size());
    dest.resize(0x10);
    encode_string(
        (_BYTE *) strKey, lenKey,
        (_BYTE *) rand_data, len_random_data,
        in_compressed_body->data(),
        out_http_body->data(), out_http_body->size(),
        dest.data(), dest.size()
    );

    out_ts_id->resize(
        3 + len_random_data*2 + dest.size() * 2
    );

    idx = 0;
    (*out_ts_id)[idx++] = '0';
    (*out_ts_id)[idx++] = '0';
    (*out_ts_id)[idx++] = '2';

    for ( i = 0 ; i < len_random_data ; i ++ )
    {
        (*out_ts_id)[ idx++ ] = numToHex((rand_data[ i ] & 0xF0) >> 4 );
        (*out_ts_id)[ idx++ ] = numToHex((rand_data[ i ] & 0x0F) >> 0 );
    }

    for ( i = 0 ; i < dest.size() ; i ++ )
    {
        (*out_ts_id)[ idx++ ] = numToHex((dest[ i ] & 0xF0) >> 4 );
        (*out_ts_id)[ idx++ ] = numToHex((dest[ i ] & 0x0F) >> 0 );
    }

    return true;
}

bool decode_http_body(TSBINARY *pInEncodedBody, TSBINARY *pInTsId, TSBINARY *pOutCompressedBody)
{
    const char *strKey = "Wucai6oj0sheiX3p";
    int lenKey = strlen(strKey);
    _BYTE rand_data[12]={0,};
    int len_random_data = sizeof(rand_data) / sizeof(rand_data[0]);
    int i, idx;
    _BYTE dest[0x10]={0,};
    int len_dest = sizeof(rand_data) / sizeof(rand_data[0]);

    for ( i = 0 ; i < len_random_data ; i ++ )
        rand_data[ i ] = HexToNum(
            (*pInTsId)[ 3 + i * 2 + 0 ],
            (*pInTsId)[ 3 + i * 2 + 1 ]
        );

    for ( i = 0 ; i < len_dest ; i ++ )
        dest[ i ] = HexToNum(
            (*pInTsId)[ 3 + len_random_data + i * 2 + 0 ],
            (*pInTsId)[ 3 + len_random_data + i * 2 + 1 ]
        );

    pOutCompressedBody->resize(pInEncodedBody->size());

    decode_string(
        (_BYTE *) strKey, lenKey,
        (_BYTE *) rand_data, len_random_data,
        pInEncodedBody->data(),
        pOutCompressedBody->data(), pOutCompressedBody->size(),
        dest, len_dest
    );

    return true;
}
