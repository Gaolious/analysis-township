#include <inc/types.h>
#include <inc/macro.h>

#ifndef _TS_XML_DATA_HEADER_FILE_INCLUDED_
#define _TS_XML_DATA_HEADER_FILE_INCLUDED_

///////////////////////////////////////////////////////////
// header 
///////////////////////////////////////////////////////////

struct TOWNSHIP_XML_HEADER
{
    _BYTE type ;   // 1 byte
    _DWORD hash_length : 24 ; // 3 byte
    _DWORD hash_seed ; // 4 byte 
} __attribute__(( aligned(1) ));


// start with '<' (0x3C)
#define XML_NO_ENCODE (0x00)

// start with 0x79  (0x79 ^ 0x3C = 0x45)
#define XML_ENCODE_79 (0x45)

// start with 0x7D  (0x70 ^ 0x3C = 0x41)
#define XML_ENCODE_7D (0x41)

// start with 0x5D  (0x50 ^ 0x3C = 0x6C)
#define XML_ENCODE_50 (0X6C)

// start with 0x66  (0x66 ^ 0x3C = 0x5A)
#define XML_ENCODE_66 (0X5A)

// start with 0xAD  (0xAD ^ 0x3C = 0x91)
#define XML_ENCODE_AD (0X91)

#endif