#include <inc/types.h>

#ifndef _TS_HTML_AES_HEADER_FILE_INCLUDED_
#define _TS_HTML_AES_HEADER_FILE_INCLUDED_
typedef struct aes_key_st
{
    unsigned int rd_key[60];
    int rounds;
} AES_KEY;

typedef int (*fnAes)(_BYTE *, _BYTE *, AES_KEY *);

typedef struct aes_data
{
    union{
// random
//    memcpy((void *)a1, (const void *)randomData, len );
//    a1->DA1[15] = 1;
//    a1->DB8[35] = 0LL;
//    a1->DA8[0] = 0LL;
//    a1->DA8[1] = 0LL;
//    a1->DA8[6] = 0LL;
//    a1->DA8[7] = 0LL;
//    a1->DA8[8] = 0LL;
//    a1->DA8[9] = 0LL;
// Encrypt
//    a1->function((_BYTE *)a1, (_BYTE *)&(a1->DA8[4]), a1->ctx);// call sub_A0FD1026 (A08F2F29 if base=0)
//    a1->DA4[3] = _R_DWORD(v5);

// aes body
//    v5 = (unsigned int)len_buff + a1->Ta8[7];
        unsigned char DA1[80]; // 80 * 1byte / 20 * 4byte
        unsigned int DA4[20];
        unsigned long long DA8[10];
    };
    union{
// aes_set_data
//    s->DB4[0] = d0;
//    s->DB4[41] = d0; 42*4(88) bytes
// aes body
//    sub_A0EC7E15(&a1->Ta1[64], (int)&a1->Tb4[4]);
        unsigned char DB1[288];
        unsigned int DB4[72];// 288 * 1byte / 72 * 4 byte
        unsigned long long DB8[36];
    };
    fnAes function;
    AES_KEY *ctx ;
} AES_DATA;

// struct AesCustomData
// {
//     union{
//     	unsigned char Ta1[80]; // 80 * 1byte / 20 * 4byte
//     	unsigned int Ta4[20];
//     	unsigned long long Ta8[5];
// 	};
//     union{
//     	unsigned char Tb1[288];
//     	unsigned int Tb4[72];// 288 * 1byte / 72 * 4 byte
//     	unsigned long long Tb8[9];
//     };
//     hashFunc hash_function;
//     AES_KEY *ctx ;
// };

// incoming.
int encode_string(_BYTE *strKey, int len_strKey, _BYTE *random_data, int len_random_data, _BYTE *strCompressedBody, _BYTE *newBuffer, int len_newBuffer, void *dest, size_t n);
int decode_string(_BYTE *strKey, int len_strKey, _BYTE *random_data, int len_random_data, _BYTE *strCompressedBody, _BYTE *newBuffer, int len_newBuffer, void *dest, size_t n);

// Step 1. AES_KEY
int aes_set_encrypt_key(_BYTE *userKey, int bits, AES_KEY *key); // check complete

// Step 2. AES_DATA
AES_DATA *aes_create_data(AES_KEY *pKey, fnAes fnHash);

// Step 2.1
_DWORD aes_data_initialize(AES_DATA *s, AES_KEY *key, fnAes function); // check complete

// Step 3.
int aes_random(AES_DATA *pData, _BYTE *random_arr, int len); // check complete

// Step 4.
int aes_encode_body(AES_DATA *a1, _BYTE *compressedBody, _BYTE *pBuff, _DWORD lenBuff);
int aes_decode_body(AES_DATA *a1, _BYTE *pInEncoded_body, _BYTE *pBuff, int len_body);

// Step 5.
_BYTE* aes_do_xmm(AES_DATA *a1, void *dest, size_t n);


int aes_encrypt(_BYTE *a1, _BYTE *a2, AES_KEY *ctx); // check complete
_DWORD aes_sub_hash_1(_BYTE *a1, _BYTE *a2); // check complete
int aes_sub_hash_2(_BYTE *a1, _BYTE *a2, _BYTE *a3, _DWORD a4); // check complete
int aes_xmm(_BYTE *a1, _BYTE *a2, unsigned int a3);
#endif