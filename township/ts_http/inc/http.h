#include <inc/types.h>

#ifndef TOWNSHIP_HTTP_H
#define TOWNSHIP_HTTP_H

// App -> Server : Request
bool encode_http_body(TSBINARY *in_compressed_body, TSBINARY *out_ts_id, TSBINARY *out_http_body);

// Server -> App : Response
// sub_73CA37
bool decode_http_body(TSBINARY *pInEncodedBody, TSBINARY *pInTsId, TSBINARY *pOutCompressedBody);


// sub_49A346
// Resp body의 data field를 decode ?
#endif //TOWNSHIP_HTTP_H
