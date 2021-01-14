#include <string.h>
#include <stdlib.h>

#include <inc/data.h>
#include <inc/decode.h>
#include <inc/hash.h>
#include <inc/utils.h>

#define LOG_TAG  "XML_DECODE"
#include <inc/logger.h>


bool deocde_0x79(TSBINARY *pSrcXML, TSBINARY *pDestXML)
{
    int i, j;
    TOWNSHIP_XML_HEADER *pHeader;
    _BYTE hash_table[0x2d7];
    _DWORD size;
    pHeader = (TOWNSHIP_XML_HEADER *) pSrcXML->data();
    LOG_ENTER_FUNCTION();

    _DWORD len = pSrcXML->size();
    do
    {
        if ((pHeader->type ^ 0x3C) != XML_ENCODE_79)
            break;
        if (!generateHashTable_0x2d7((_BYTE *) hash_table, pHeader->hash_length, pHeader->hash_seed + 4))
            break;

        // 0x10f85a // 400008
        size = (pHeader->hash_length - ( len ^ 0xC5EEDu)) ^ 0x396A8u;
        if ( size != len - 8 )
        {
            LOGE("size is miss match src:%u / dest:%u", pSrcXML->size(), size );
            //size = len - 8 ;
        }
        pDestXML->clear();
        pDestXML->insert(
            pDestXML->end(),
            pSrcXML->data() + sizeof(TOWNSHIP_XML_HEADER),
            pSrcXML->data() + sizeof(TOWNSHIP_XML_HEADER) + size
        );


        for (i = 0, j = 0; i < pDestXML->size(); i++, j = (j + 1) % 0x2d7) {
            if (i > 0)
                (*pDestXML)[i] -= (*pDestXML)[i - 1];
            (*pDestXML)[i] ^= hash_table[j];
        }

        LOG_LEAVE_FUNCTION();
        return true ;
    } while ( false );

    LOG_LEAVE_FUNCTION();
    return false;
}

bool get_decode_key(TSBINARY *pOut, _BYTE val )
{
    const char *v2 ;
    if ( val == 0x41 )
        v2 = "AO[hUyI.o|q@p^ Ms1I7 Zub:a'O4Y'_0;XmZ~vK=nJ#wYCccn^CzJu4<f5ogy]}#K5FIlKnnwT_^dVAZgv]D WIt@sl!i=)qxnWh'QuBgR~yZe"
             "oh-cC@q@>6-VvT2,ZSWlU~th+%0|W_iPl}M0un?pydqul`|ZL`u7rm1L0ewz4c9*fnRZF:8(;&%6[Gn>,LXW9F?QQ41(:5svrGV#{'3)]2/6ln["
             "sYds:qTdBh8OyB<#Q!U%Q'[d+r%)OBOuy]!=}ag0GP6Z~`+9>rF&`_8^}N~X02D)H#}aO)08tqx:,O&fNp{R$W>)MBeLi|RX:.z'5B%g]13Ef y"
             "%K?{RApgk{.1),Z]_l,]v~'mrvB)uG.sw2P%Q+|NQL`>IfyLwd],I?f+ig:o8s#LRMy($0Y2VzXBEV~oph4p/dumT(6x{3Q~&mma)%/~BRcnojy"
             "TfT.yqn&sk9j;ay3pg+,ccJG=TEu2K-*d%IU*Y2N).}{UP_N*x?u9fw$Vgj%AtBG+dRE(:n(tI'b47?szaINkm8{<7jL#t;SJ;I'_vrVCoz!E2y"
             "*<n&RjOeoiOE3[?ILO+?dS@u|]vVIHgivtw#_rlogL?rclJkA2V6dH_av 7aSZ6RBgQbL)fW11b<'GW'M)N#ll^qZ{]:baj@nv9YQy`(8'&w_v("
             "PST6KH0OJB04xx>RC3!kRx*|+25^OSh.X'&N>`m9KfIWo|S2jhbc fTd";
    else
        v2 = "BLD18qQhOwEylkVki91hjILTcIwbEMhUHamjkAzgyIWnl1tqOZvO+7AvOTqn036uyHAQVVbSH3/BzYMjNHTMXvogJBWI1siiMZF2zFzD0GEpuGd"
             "F+WbSIrug4fzHojQ/AAaBx2HT/tZ8hP+ITRc8z9a7ecsrGX+EBq+b3mada6zeJPxE2j47psb/J4Xnx0AEfh+lEb2GLpczI7e3o0BGP9GlmQYPSX"
             "INq87N2D8G175+cBwbMmzdfsIxr9hNGJgLGTFe/NdMP6NoAERNJOij9vzbgwiaOpdvmqBkV2HLp//Pj28HgIc392BrzFQ/slGN0/TqxugL1UY9G"
             "MpmI+GQVDSMzswGVWZ5VMjs4sSvkAmQ/p5AnrRyDoszxO+SKI5HV+OwHS0G7NcKXUMCx32xk6mVNxcpl0DwivGhJuvk/gphiG0b2f0gciQaaDJz"
             "uOJASND397ryTg4EuRYRw8D2A1lNF5lGEkzxMCGi56t4zCLduBcROWbbjBKKZer6enhbgsEytVBmzo4ONfQ+ZFv3sLhaEb72lnMkVKDD3tw7hzA"
             "oL86ObHGLOEGMUY3n9wihn1peBNBTcL3kSfH4/t9KF4qZ3GtXA++WO1h5/0edqVhDygXMUzQ87EZvcGuqLMk6iR08pFBO529aAADg8o9hHKfspY"
             "vwghDW/5HtJGL7CrGpE4Sr8FnvNvv7J3AGa9csWrhMB00P/dupnCafDuJAeCgFL0l";

    pOut->clear();
    pOut->insert(pOut->end(), v2, v2 + strlen(v2));
    return true ;
}

bool deocde_0x7d(TSBINARY *pSrcXML, TSBINARY *pDestXML)
{
    int i, j ;
    TSBINARY key;

    LOG_ENTER_FUNCTION();

    if ( ((*pSrcXML)[0] ^ 0x3C) != XML_ENCODE_7D )
        return false;

    get_decode_key(&key, (*pSrcXML)[0] ^ 0x3C);

    LOGI("Src length : %u", pSrcXML->size());

    pDestXML->resize(pSrcXML->size());
    for ( i = 0, j = 0 ; i < pSrcXML->size() ; i ++, j = ( j + 1 ) % key.size() )
        (*pDestXML)[ i ] = (*pSrcXML)[ i ] ^ key[ j ];

    LOGI("Dest length : %u", pDestXML->size());

    LOG_LEAVE_FUNCTION();
    return true;
}

bool deocde_0x50(TSBINARY *pSrcXML, TSBINARY *pDestXML)
{
    int i, j ;
    TSBINARY key;
    LOG_ENTER_FUNCTION();
    do
    {
        if ( ((*pSrcXML)[0] ^ 0x3C) != XML_ENCODE_50 )
            break;

        get_decode_key(&key, (*pSrcXML)[0] ^ 0x3C);

        pDestXML->resize(pSrcXML->size());
        for ( i = 0, j = 0 ; i < pSrcXML->size() ;  i++ , j = ( j + 1 ) % key.size())
        {
            if ( i > 0 )
                pDestXML->data()[ i ] -= pDestXML->data()[ i - 1 ] ;
            pDestXML->data()[ i ] = (*pSrcXML)[ i ] ^ key[ j ];
        }

        LOG_LEAVE_FUNCTION();
        return true ;
    } while (false);

    LOG_LEAVE_FUNCTION();
    return false ;
}

bool deocde_0x66(TSBINARY *pSrcXML, TSBINARY *pDestXML)
{
    int i, j ;
    TSBINARY key;
    LOG_ENTER_FUNCTION();

    do {
        if ( ((*pSrcXML)[0] ^ 0x3C) != XML_ENCODE_66 )
            break;

        get_decode_key(&key, 66);

        pDestXML->resize(pSrcXML->size());
        for ( i = 0, j = 0 ; i < pSrcXML->size() ; i ++, j = ( j + 1 ) % key.size() )
        {
            (*pDestXML)[i] = (*pSrcXML)[i];
            if ( i > 0 )
                (*pDestXML)[i] -= (*pDestXML)[i-1];

            (*pDestXML)[i] ^= key[j];
        }

        LOG_LEAVE_FUNCTION();
        return true;
    } while (false);

    LOG_LEAVE_FUNCTION();
    return false;
}

bool deocde_0xAD(TSBINARY *pSrcXML, TSBINARY *pDestXML)
{
    int i, j ;
    TSBINARY key;
    LOG_ENTER_FUNCTION();

    do {
        if ( ((*pSrcXML)[0] ^ 0x3C) != XML_ENCODE_AD )
            break;

        get_decode_key(&key, 88);

        pDestXML->resize(pSrcXML->size());
        for ( i = 0, j = 0 ; i < pSrcXML->size() ; i ++, j = ( j + 1 ) % key.size() )
        {
            (*pDestXML)[i] = (*pSrcXML)[i];
            if ( i > 0 )
                (*pDestXML)[i] -= (*pDestXML)[i-1];

            (*pDestXML)[i] ^= key[j];
        }
        LOG_LEAVE_FUNCTION();
        return true ;
    } while (false);

    LOG_LEAVE_FUNCTION();
    return false;
}

bool decode(TSBINARY *pInFilename, TSBINARY *pOutFilename)
{
    bool ret = false;
    TSBINARY encodedXml, decodedXml ;
    TOWNSHIP_XML_HEADER *pHeader ;

    LOG_ENTER_FUNCTION();

    do
    {
        if ( !readFile(pInFilename, &encodedXml) )
        {
            LOGE("Failed to read File");
            break;
        }

        pHeader = (TOWNSHIP_XML_HEADER *)encodedXml.data();

        switch ( pHeader->type ^ 0x3C )
        {
            case XML_NO_ENCODE : // start with '<'
            {
                if ( !writeFile(pOutFilename, &decodedXml, true) )
                {
                    LOGE("Failed to write decoded data");
                    break ;
                }
                ret = true ;
            }
            break;
            case XML_ENCODE_79: // start with 0x79
            {
                 if ( !deocde_0x79(&encodedXml, &decodedXml) )
                 {
                     LOGE("Failed to decode (0x79^0x3C)");
                     break ;
                 }

                 if ( !writeFile(pOutFilename, &decodedXml, true) )
                 {
                     LOGE("Failed to write decoded data");
                     break ;
                 }
                 ret = true ;
            }
            break;
            case XML_ENCODE_7D: // start with 0x7D
            {
                if ( !deocde_0x7d(&encodedXml, &decodedXml) )
                {
                    LOGE("Failed to decode (0x7D^0x3C)");
                    break ;
                }

                if ( !writeFile(pOutFilename, &decodedXml, true) )
                {
                    LOGE("Failed to write decoded data");
                    break ;
                }
                ret = true ;
            }
            break;
            case XML_ENCODE_50: // start with 0x50
            {
                if ( !deocde_0x50(&encodedXml, &decodedXml) )
                {
                    LOGE("Failed to decode (0x50^0x3C)");
                    break ;
                }

                if ( !writeFile(pOutFilename, &decodedXml, true) )
                {
                    LOGE("Failed to write decoded data");
                    break ;
                }
                ret = true ;
            }
            break;

            case XML_ENCODE_66:
            {
                if (!deocde_0x66(&encodedXml, &decodedXml)) {
                    LOGE("Failed to decode (0x66^0x3C)");
                    break;
                }

                if (!writeFile(pOutFilename, &decodedXml, true)) {
                    LOGE("Failed to write decoded data");
                    break;
                }
                ret = true;
                break;
            }
            case XML_ENCODE_AD:
            {
                // sub_9F064576(&v34, 88);
                if (!deocde_0xAD(&encodedXml, &decodedXml)) {
                    LOGE("Failed to decode (0x50^0x3C)");
                    break;
                }

                if (!writeFile(pOutFilename, &decodedXml, true)) {
                    LOGE("Failed to write decoded data");
                    break;
                }
                ret = true;
                break;
            }

            default :
            {
                LOGE("Failed to decode encodedXml. Unknown Header : 0x%02X", encodedXml[0]);
                ret = false ;
            }
            break;
        }
    } while ( false );

    LOG_LEAVE_FUNCTION();

    return ret ;
}

bool decode(const char *pInFilename, const char *pOutFilename)
{
    TSBINARY in(pInFilename, pInFilename + strlen(pInFilename) + 1);
    TSBINARY out(pOutFilename, pOutFilename + strlen(pOutFilename) + 1);

    return decode(&in, &out);
}
/*
1. 저장된 데이터를 dump 한 후,

barn에 추가 / 삭제 했을 때 어떤 변화가 있는지

- LocalInfo.xml
- mGameInfo.xml



2. LocalInfo.xml 그리고 mGameInfo.xml 파일은 어떻게 받아오는가. ?

maybe_readStream_2,3,4

-----------------------------------------------------

struct XmlFile
{
    unsigned char [20];
    FILE *fp ;
};

*(FILE **)(a1 + 20)

-----------------------------------------------------
unsigned int __cdecl sub_9F124CF7(int *pFileData, unsigned int a2, bool *a3)
-----------------------------------------------------

pFileData : 0xA6D80000
A6D80000  7D 3D 34 07 21 47 43 0E  4F 5C 51 7C 31 1C 74 28  }=4.!GC.O\Q|1.t(

 v5 = *(_BYTE *)*pFileData ^ 0x3C; //  v5 = 0x41

    v2 = "BLD18qQhOwEylkVki91hjILTcIwbEMhUHamjkAzgyIWnl1tqOZvO+7AvOTqn036uyHAQVVbSH3/BzYMjNHTMXvogJBWI1siiMZF2zFzD0GEpuGd"
         "F+WbSIrug4fzHojQ/AAaBx2HT/tZ8hP+ITRc8z9a7ecsrGX+EBq+b3mada6zeJPxE2j47psb/J4Xnx0AEfh+lEb2GLpczI7e3o0BGP9GlmQYPSX"
         "INq87N2D8G175+cBwbMmzdfsIxr9hNGJgLGTFe/NdMP6NoAERNJOij9vzbgwiaOpdvmqBkV2HLp//Pj28HgIc392BrzFQ/slGN0/TqxugL1UY9G"
         "MpmI+GQVDSMzswGVWZ5VMjs4sSvkAmQ/p5AnrRyDoszxO+SKI5HV+OwHS0G7NcKXUMCx32xk6mVNxcpl0DwivGhJuvk/gphiG0b2f0gciQaaDJz"
         "uOJASND397ryTg4EuRYRw8D2A1lNF5lGEkzxMCGi56t4zCLduBcROWbbjBKKZer6enhbgsEytVBmzo4ONfQ+ZFv3sLhaEb72lnMkVKDD3tw7hzA"
         "oL86ObHGLOEGMUY3n9wihn1peBNBTcL3kSfH4/t9KF4qZ3GtXA++WO1h5/0edqVhDygXMUzQ87EZvcGuqLMk6iR08pFBO529aAADg8o9hHKfspY"
         "vwghDW/5HtJGL7CrGpE4Sr8FnvNvv7J3AGa9csWrhMB00P/dupnCafDuJAeCgFL0l";



0x7D ^ 0x3C = 0x41 = 65
0x50 ^ 0x3C = 0x6C = 108
 * */