#include "inc/data.h"
#include "inc/macro.h"

#ifndef _UTILS_HEADER_FILE_INCLUDED_
#define _UTILS_HEADER_FILE_INCLUDED_

bool readFile(const char *inFilename, TSVector *pXml);

bool writeFile(const char *outFilename, TSVector *pXml, bool overwrite = false);

bool resizeTSVector(TSVector *pVector, _DWORD capacity);

bool resizeTSVector(TSVector *pVector, _BYTE *pBuffer, _DWORD length, _DWORD offset);

#endif