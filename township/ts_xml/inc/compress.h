#include <inc/types.h>

#ifndef _TS_HTTP_COMPRESS_HEADER_FILE_INCLUDED_
#define _TS_HTTP_COMPRESS_HEADER_FILE_INCLUDED_

bool ts_compress(_BYTE *message, unsigned int size, TSBINARY *pCompressed);
bool ts_decompress(_BYTE *message, unsigned int size, TSBINARY *pDecompressed);


#endif //_TS_HTTP_COMPRESS_HEADER_FILE_INCLUDED_
