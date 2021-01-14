#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/stat.h>
#include <inc/types.h>
#include <inc/utils.h>

#define LOG_TAG  "TS_UTIL"
#include <inc/logger.h>

bool isLE()
{
    unsigned int n = 0x11223344u;
    return u8p(&n)[0] == 0x11;
}
bool isBE()
{
    unsigned int n = 0x11223344u;
    return u8p(&n)[0] == 0x44;
}

char ToHex(_BYTE a, bool lower = true)
{
    a &= 0xf;

    if ( 0 <= a && a <= 9 )
        return '0' + a ;

    if ( lower )
        return 'a' + (a-10);
    else
        return 'A' + (a-10);
}


// HEX String  : "A9 32 93 1F 91 A1 00 12"
// DATA String : "\xA9\x32\x93\x1F\x91\xA1\x00\x12
// DATA Array  : { 0xA9, 0x32, 0x93, 0x1F, 0x91, 0xA1, 0x00, 0x12 }
// DATA Literal : 0x1F9332A9u
// DATA Literal String : "0x1F9332A9u"
// LittleEndian
void DataToLiteralString(TSBINARY *pBuff, int offset, int datasize, TSBINARY *pOut)
{
    const char *prefix = "0x";
    int s, e, inc ;

    pOut->clear();

    if ( isLE() )
    {
        s = offset + datasize - 1 ;
        e = s - datasize ;
        inc = -1 ;
    }
    else
    {
        s = offset ;
        e = s + datasize ;
        inc = 1 ;
    }

    pOut->push_back('0');
    pOut->push_back('x');

    for ( int i = s ; i != e ; i += inc )
    {
        pOut->push_back(ToHex( (_BYTE)((pBuff->data()[i] >> 4) & 0x0F), true ));
        pOut->push_back(ToHex( (_BYTE)((pBuff->data()[i] >> 0) & 0x0F), true ));
    }

    if ( datasize >= 4 )
        pOut->push_back('u');
    if ( datasize >= 8 )
        pOut->push_back('l'),pOut->push_back('l');

    pOut->push_back(0x00);
}

void checkFilename(TSBINARY *pFilename)
{
    if( pFilename && pFilename->size() > 0 )
    {
        if ( pFilename->data()[ pFilename->size() - 1 ] != 0x00 )
            pFilename->push_back(0x00);
    }
}

/**
 *
 * @param pFilename [in] input filename
 * @param pOutBuff [out] read data
 * @return
 *      true    Success
 *      false   Fail
 */
bool readFile(TSBINARY *pFilename, TSBINARY *pOutBuff)
{
    _DWORD capacity;
    size_t n, remain ;
    char *filename ;
    FILE *fp ;
    struct stat _stat ;
    _BYTE buff[1024+1];

    LOG_ENTER_FUNCTION();
    do
    {
        checkFilename(pFilename);
        LOGI("read file : %s", pFilename->data());
        if (!pFilename || !(filename = (char *)pFilename->data()) )
        {
            LOGE("parameter inFilename is Null");
            break;
        }

        if ( stat(filename, &_stat) != 0 )
        {
            LOGE("Failed to get stat %s", filename);
            break;
        }

        fp = fopen((const char *)pFilename->data(), "rb");

        if ( !fp )
        {
            LOGE("Failed to read %s", pFilename->data());
            break;
        }

        capacity = _stat.st_size ;
        if ( capacity > 300000 )
            capacity = (capacity / 100000 + 1) * 100000;

        pOutBuff->resize(capacity);
        pOutBuff->clear();
        remain = _stat.st_size ;

        while ( remain > 0 ){
            n = fread(buff, 1, sizeof(buff)-1, fp);
            if ( n <= 0 )
                break;
            pOutBuff->insert(pOutBuff->end(), (_BYTE *)buff, (_BYTE *)buff+n);
            remain -= n ;
        }
        fclose(fp);

        return true ;

    } while (false);

    LOG_LEAVE_FUNCTION();
    return false ;
}

bool writeFile(TSBINARY *pFilename, TSBINARY *pInBuff, bool overwrite = false)
{
    char *filename ;
    FILE *fp ;
    struct stat _stat ;

    do
    {
        checkFilename(pFilename);

        if ( !pFilename || !(filename = (char *)pFilename->data()) )
        {
            LOGE("parameter inFilename is Null");
            break;
        }

        if ( !overwrite && access(filename, F_OK) != -1 )
        {
            LOGE("Failed to writeFile : %s", filename);
            break;
        }

        if ( (fp = fopen(filename, "wb")) == NULL )
        {
            LOGE("Failed to writeFile : %s", filename);
            break;
        }

        fwrite((void *)pInBuff->data(), sizeof(_BYTE), pInBuff->size(), fp);

        fclose(fp);

        return true;

    } while (false);

    return false ;
}
