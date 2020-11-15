#include <stdlib.h>
#include <string.h>

#include "inc/types.h"
#include "inc/hash.h"

_DWORD MurmurHash2 ( const void * key, int len, _DWORD seed )
{
    const _DWORD m = 0x5bd1e995;
    const int r = 24;
    
    _DWORD h = seed ^ len;
    _DWORD k;
    
    const unsigned char * data = (const unsigned char *)key;
    
    while(len >= 4)
    {
        _DWORD k = *(_DWORD *)data;
        
        k *= m;
        k ^= k >> r;
        k *= m;

        h *= m;
        h ^= k;

        data += 4;
        len -= 4;
    }

    switch(len)
    {
        case 3: h ^= data[2] << 16;
        case 2: h ^= data[1] << 8;
        case 1: h ^= data[0];
            h *= m;
    };

    h ^= h >> 13;
    h *= m;
    h ^= h >> 15;

    return h;
} 

bool generateHashTable_0x2d7(_BYTE *hash_table, int length, _DWORD seed)
{
    int i, j ;
    _DWORD hash ;
    _BYTE *p ;

    if ( !hash_table)
        return false ;

    memset(hash_table, 0x00, 0x2d7);

    p = (_BYTE *)&hash ;

    hash = seed ;
    for ( i = 0 ; i < 0x2d7 ; )
    {
        hash = MurmurHash2((const void *)&hash, 4, length);
        for ( j = 0 ; j < 4 && i < 0x2d7 ; j ++, i ++ )
            hash_table[ i ] = p[ j ] ;
    }
    return true ;
}
