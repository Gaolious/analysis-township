#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <sys/stat.h>
#include "inc/utils.h"

const int READ_SIZE = 1 << 15;

template<typename A>
A min(A a, A b) {
    return (a < b) ? a : b;
}


bool readFile(const char *inFilename, TSVector *pXml) {
    struct stat _stat;
    FILE *fp = NULL;
    do {
        if (!inFilename) {
            fprintf(stderr, "inFilename is NULL\n");
            break;
        }
        if (!pXml) {
            fprintf(stderr, "pXml is NULL\n");
            break;
        }

        if (stat(inFilename, &_stat) != 0) {
            fprintf(stderr, "Failed to open in-file");
            break;
        }
        if ((fp = fopen(inFilename, "rb")) == NULL) {
            fprintf(stderr, "Failed to open in-file");
            break;
        }

        pXml->size = _stat.st_size;
        if (pXml->size < 1) {
            fprintf(stderr, "filesize is 0");
            break;
        }
        resizeTSVector(pXml, pXml->size);
        fread((void *) pXml->pData, sizeof(_BYTE), pXml->size, fp);
        fclose(fp);
        return true;

    } while (false);

    return false;
}

bool writeFile(const char *outFilename, TSVector *pXml, bool overwrite) {
    FILE *fp = NULL;
    do {
        if (!outFilename) {
            fprintf(stderr, "outFilename is NULL\n");
            break;
        }
        if (!pXml) {
            fprintf(stderr, "pXml is NULL\n");
            break;
        }
        if (!overwrite && access(outFilename, F_OK) != -1) {
            fprintf(stderr, "%s is exist\n", outFilename);
            break;
        }

        if ((fp = fopen(outFilename, "wb")) == NULL) {
            perror("Failed to open in-file");
            break;
        }

        fwrite((void *) pXml->pData, sizeof(_BYTE), pXml->size, fp);
        fclose(fp);
        return true;

    } while (false);

    return false;
}


bool resizeTSVector(TSVector *pVector, _DWORD capacity) {
    _BYTE *pBuffer = NULL;
    _DWORD size;

    if (!pVector) return false;

    if (capacity > 300000)
        capacity = (capacity / 100000 + 1) * 100000;
    else
        capacity = 300000;

    if (pVector->capacity < capacity) {
        pBuffer = new _BYTE[capacity];

        if (pVector->pData && pVector->size > 0) {
            size = min(pVector->size, capacity);
            memcpy((void *) pBuffer, (void *) pVector->pData, size);
            SAFE_DELETE(pVector->pData);
        }

        pVector->pData = pBuffer;
        pVector->capacity = capacity;
    }
    return true;
}

bool resizeTSVector(TSVector *pVector, _BYTE *pBuffer, _DWORD length, _DWORD offset) {
    if (!resizeTSVector(pVector, offset + length))
        return false;

    memcpy((void *) (pVector->pData + offset), (void *) pBuffer, length);
    pVector->size = length + offset;
    return true;
}
