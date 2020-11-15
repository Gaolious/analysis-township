#include <string.h>
#include <random>

#include "inc/data.h"
#include "inc/utils.h"
#include "inc/hash.h"

_DWORD get_random()
{
  std::random_device rd;
  std::mt19937 gen(rd());
  std::uniform_int_distribution<_DWORD> dis(0, 0xFFFFFFFF);
  return dis(gen);
}

bool encode_0x45(TSVector *pSrcXML, TSVector *pDestXML, _DWORD seed)
{
    TOWNSHIP_XML_HEADER *pHeader ;
    int header_size = sizeof(TOWNSHIP_XML_HEADER);
    _BYTE hash_table[0x2d7];
    int i, j ;
    _BYTE *pDest ;
    _BYTE prev, curr ;

    resizeTSVector(pDestXML, pSrcXML->pData, pSrcXML->size, header_size );

    pHeader = (TOWNSHIP_XML_HEADER *)pDestXML->pData ;

    pHeader->type = 0x79 ;
    pHeader->hash_length = ( pSrcXML->size ^ 0x396A8 ) + ( (pSrcXML->capacity + 8) ^ 0xC5EED ) ;
    pHeader->hash_seed = seed ;

    if (!generateHashTable_0x2d7((_BYTE *)hash_table, pHeader->hash_length, pHeader->hash_seed + 4) )
        return false ;    

    prev = 0 ;
    for ( i = header_size , j = 0 ; i < pDestXML->size ; i ++, j = (j+1) % 0x2d7 )
    {
        curr = pDestXML->pData[i];
        pDestXML->pData[i] ^= hash_table[ j ];
        pDestXML->pData[i] += prev ;
        prev = curr ;
    }

    return true ;
}

_DWORD getSeed(TSVector *pXml)
{
    int i ;
    _DWORD sum, cum_sum ;
    _DWORD seed, rand_value ;

    sum = 1 ;
    cum_sum = 0 ;

    for ( int i = 0 ; i < pXml->size ; i ++ )
    {
        sum += pXml->pData[ i ] ;
        cum_sum += sum ;
    }

    cum_sum <<= 0x10;
    
    seed = ( ( sum | cum_sum ) >> 0x10 ) ^ (_WORD)(sum) ;
    
    rand_value = get_random() ;
    
    if ( rand_value != 0 )
        seed |= (rand_value << 16);
    else
        seed |= 0x12340000;

    return seed;
}

bool encode(const char *inFilename, const char *outFilename)
{
    _DWORD seed ;
    TSVector decodedXml, encodedXml;

    if (!readFile(inFilename, &decodedXml))
        return false ;

    seed = getSeed(&decodedXml);

    if (!encode_0x45( &decodedXml, &encodedXml, seed ))
        return false ;

    if ( !writeFile(outFilename, &encodedXml, true) )
        return false ;
    
    return true ;
}