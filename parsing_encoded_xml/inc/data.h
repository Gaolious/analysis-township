#include "inc/types.h"
#include "inc/macro.h"

#ifndef _DATA_HEADER_FILE_INCLUDED_
#define _DATA_HEADER_FILE_INCLUDED_

///////////////////////////////////////////////////////////
// boost::vector ? std::vector ?
///////////////////////////////////////////////////////////
struct TSVector {
    _BYTE *pData;
    _DWORD size;
    _DWORD capacity;

    TSVector() {
        this->pData = NULL;
        this->size = 0;
        this->capacity = 0;
    }

    ~TSVector() {
        SAFE_DELETE(this->pData);
    }
};


///////////////////////////////////////////////////////////
// header 
///////////////////////////////////////////////////////////
typedef struct _Header_ {
    _BYTE type;   // 1 byte
    _DWORD hash_length: 24; // 3 byte
    _DWORD hash_seed; // 4 byte
} TOWNSHIP_XML_HEADER  __attribute__(( aligned(1)));

// struct.1byte 
// .text:A1003B08 mov     eax, [ecx]
// .text:A1003B0A cmp     byte ptr [eax], 79h ; 'y'
// struct.3byte [eax+1] << 0 | [eax+2] << 8 | [eax+3] << 16
// .text:A1003B13 movzx   ecx, byte ptr [eax+1]
// .text:A1003B17 movzx   edx, byte ptr [eax+2]
// .text:A1003B1B shl     edx, 8
// .text:A1003B1E or      edx, ecx
// .text:A1003B20 movzx   edi, byte ptr [eax+3]
// .text:A1003B24 shl     edi, 10h
// .text:A1003B27 or      edi, edx
// struct.4byte
// .text:A1003B29 mov     eax, [eax+4]
// .text:A1003B2C mov     [esp+8], eax

///////////////////////////////////////////////////////////
// header type
///////////////////////////////////////////////////////////
#define HEADER_TYPE_45H (0x45)

#endif