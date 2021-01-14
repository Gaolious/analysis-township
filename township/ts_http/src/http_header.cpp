#include <inc/types.h>

void decode_key(TSBINARY *in, TSBINARY *out)
{
    _BYTE val = 0;
    int i ;
    int length = in->size() - 1 ;
    out->resize(in->size());
    
    val = (*in)[length] - (length*length);

    for ( i = 0 ; i < length ; i ++)
    {
        (*out)[i] = val ^ (*in)[ i ];
        val += length ;
    }
    (*out)[length] = 0x00;
}