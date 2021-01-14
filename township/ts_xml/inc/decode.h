#ifndef _DECODE_HEADER_FILE_INCLUDED_
#define _DECODE_HEADER_FILE_INCLUDED_

bool decode(const char *inFilename, const char *outFilename);
bool decode(TSBINARY *pInFilename, TSBINARY *pOutFilename);


bool deocde_0x79(TSBINARY *pSrcXML, TSBINARY *pDestXML);
bool deocde_0x7d(TSBINARY *pSrcXML, TSBINARY *pDestXML);
bool deocde_0x50(TSBINARY *pSrcXML, TSBINARY *pDestXML);
bool deocde_0x66(TSBINARY *pSrcXML, TSBINARY *pDestXML);
bool deocde_0xAD(TSBINARY *pSrcXML, TSBINARY *pDestXML);

#endif