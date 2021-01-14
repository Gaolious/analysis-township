#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#include "inc/data.h"
#include "inc/decode.h"
#include "inc/hash.h"
#include "inc/utils.h"

bool deocde_0x45(TSVector *pSrcXML, TSVector *pDestXML) {
    int i, j;
    TOWNSHIP_XML_HEADER *pHeader;

    _BYTE hash_table[0x2d7];
    _DWORD size;
    pHeader = (TOWNSHIP_XML_HEADER *) pSrcXML->pData;

    printf("size of ts xml header : %d\n", sizeof(TOWNSHIP_XML_HEADER));

    if ((pHeader->type ^ 0x3C) != HEADER_TYPE_45H)
        return false;

    if (!generateHashTable_0x2d7((_BYTE *) hash_table, pHeader->hash_length, pHeader->hash_seed + 4))
        return false;

    //    pHeader->hash_length = (pSrcXML->size ^ 0x396A8) + ((pSrcXML->capacity + 8) ^ 0xC5EED);
    size = (pHeader->hash_length - ((pSrcXML->capacity + 8) ^ 0xC5EEDu)) ^ 0x396A8u;

    resizeTSVector(pDestXML, pSrcXML->pData + sizeof(TOWNSHIP_XML_HEADER), size, 0);


    do {
        for (i = 0, j = 0; i < pDestXML->size; i++, j = (j + 1) % 0x2d7) {
            if (i > 0)
                pDestXML->pData[i] -= pDestXML->pData[i - 1];
            pDestXML->pData[i] ^= hash_table[j];
        }
        return true;

    } while (false);


    return false;
}

bool decode(const char *inFilename, const char *outFilename) {
    TSVector encodedXml, decodedXml;
    TOWNSHIP_XML_HEADER *pHeader;

    if (!readFile(inFilename, &encodedXml))
        return false;

    pHeader = (TOWNSHIP_XML_HEADER *) encodedXml.pData;

    switch (pHeader->type ^ 0x3C) {
        case HEADER_TYPE_45H: {
            if (!deocde_0x45(&encodedXml, &decodedXml))
                return false;

            if (!writeFile(outFilename, &decodedXml, true))
                return false;

            return true;
        }
            break;

        default:
            break;
    }

    return false;
}