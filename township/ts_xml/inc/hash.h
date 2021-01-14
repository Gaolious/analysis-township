#include "inc/types.h"

#ifndef _HASH_HEADER_FILE_INCLUDED_
#define _HASH_HEADER_FILE_INCLUDED_

_DWORD MurmurHash2 ( const void * key, int len, _DWORD seed );
bool generateHashTable_0x2d7(_BYTE *hash_table, int length, _DWORD seed);

#endif