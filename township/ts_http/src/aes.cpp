#include <inc/types.h>
#include <inc/aes.h>
#include <inc/utils.h>
#include <inc/xmm.h>
#include <inc/macro.h>
#include <string.h>
#include <stdio.h>

// name=[T1], offset[0x02A0A4F8 (44082424)], length[0x00000080 (128)]
_QWORD T1[128] = {
    0x7C84F87C63A5C663ULL, 0x7B8DF67B7799EE77ULL, 0x6BBDD66BF20DFFF2ULL, 0xC55491C56FB1DE6FULL,
    0x0103020130506030ULL, 0x2B7D562B67A9CE67ULL, 0xD762B5D7FE19E7FEULL, 0x769AEC76ABE64DABULL, // 1 ~ 8
    0x829D1F82CA458FCAULL, 0x7D87FA7DC94089C9ULL, 0x59EBB259FA15EFFAULL, 0xF00BFBF047C98E47ULL,
    0xD467B3D4ADEC41ADULL, 0xAFEA45AFA2FD5FA2ULL, 0xA4F753A49CBF239CULL, 0xC05B9BC07296E472ULL, // 9 ~ 16
    0xFD1CE1FDB7C275B7ULL, 0x266A4C2693AE3D93ULL, 0x3F417E3F365A6C36ULL, 0xCC4F83CCF702F5F7ULL,
    0xA5F451A5345C6834ULL, 0xF108F9F1E534D1E5ULL, 0xD873ABD87193E271ULL, 0x153F2A1531536231ULL, // 17 ~ 24
    0xC75295C7040C0804ULL, 0xC35E9DC323654623ULL, 0x96A1379618283018ULL, 0x9AB52F9A050F0A05ULL,
    0x1236241207090E07ULL, 0xE23DDFE2809B1B80ULL, 0x27694E27EB26CDEBULL, 0x759FEA75B2CD7FB2ULL, // 25 ~ 32
    0x839E1D83091B1209ULL, 0x1A2E341A2C74582CULL, 0x6EB2DC6E1B2D361BULL, 0xA0FB5BA05AEEB45AULL,
    0x3B4D763B52F6A452ULL, 0xB3CE7DB3D661B7D6ULL, 0xE33EDDE3297B5229ULL, 0x849713842F715E2FULL, // 33 ~ 40
    0xD168B9D153F5A653ULL, 0xED2CC1ED00000000ULL, 0xFC1FE3FC20604020ULL, 0x5BEDB65BB1C879B1ULL,
    0xCB468DCB6ABED46AULL, 0x394B7239BED967BEULL, 0x4CD4984C4ADE944AULL, 0xCF4A85CF58E8B058ULL, // 41 ~ 48
    0xEF2AC5EFD06BBBD0ULL, 0xFB16EDFBAAE54FAAULL, 0x4DD79A4D43C58643ULL, 0x8594118533556633ULL,
    0xF910E9F945CF8A45ULL, 0x7F81FE7F02060402ULL, 0x3C44783C50F0A050ULL, 0xA8E34BA89FBA259FULL, // 49 ~ 56
    0xA3FE5DA351F3A251ULL, 0x8F8A058F40C08040ULL, 0x9DBC219D92AD3F92ULL, 0xF504F1F538487038ULL,
    0xB6C177B6BCDF63BCULL, 0x21634221DA75AFDAULL, 0xFF1AE5FF10302010ULL, 0xD26DBFD2F30EFDF3ULL, // 57 ~ 64
    0x0C14180CCD4C81CDULL, 0xEC2FC3EC13352613ULL, 0x97A235975FE1BE5FULL, 0x17392E1744CC8844ULL,
    0xA7F255A7C45793C4ULL, 0x3D477A3D7E82FC7EULL, 0x5DE7BA5D64ACC864ULL, 0x7395E673192B3219ULL, // 65 ~ 72
    0x8198198160A0C060ULL, 0xDC7FA3DC4FD19E4FULL, 0x2A7E542A22664422ULL, 0x88830B8890AB3B90ULL,
    0xEE29C7EE46CA8C46ULL, 0x143C2814B8D36BB8ULL, 0x5EE2BC5EDE79A7DEULL, 0xDB76ADDB0B1D160BULL, // 73 ~ 80
    0x32566432E03BDBE0ULL, 0x0A1E140A3A4E743AULL, 0x060A0C0649DB9249ULL, 0x5CE4B85C246C4824ULL,
    0xD36EBDD3C25D9FC2ULL, 0x62A6C462ACEF43ACULL, 0x95A4319591A83991ULL, 0x798BF279E437D3E4ULL, // 81 ~ 88
    0xC8438BC8E732D5E7ULL, 0x6DB7DA6D37596E37ULL, 0xD564B1D58D8C018DULL, 0xA9E049A94ED29C4EULL,
    0x56FAAC566CB4D86CULL, 0xEA25CFEAF407F3F4ULL, 0x7A8EF47A65AFCA65ULL, 0x08181008AEE947AEULL, // 89 ~ 96
    0x7888F078BAD56FBAULL, 0x2E725C2E256F4A25ULL, 0xA6F157A61C24381CULL, 0xC65197C6B4C773B4ULL,
    0xDD7CA1DDE823CBE8ULL, 0x1F213E1F749CE874ULL, 0xBDDC61BD4BDD964BULL, 0x8A850F8A8B860D8BULL, // 97 ~ 104
    0x3E427C3E7090E070ULL, 0x66AACC66B5C471B5ULL, 0x0305060348D89048ULL, 0x0E121C0EF601F7F6ULL,
    0x355F6A3561A3C261ULL, 0xB9D069B957F9AE57ULL, 0xC15899C186911786ULL, 0x9EB9279E1D273A1DULL, // 105 ~ 112
    0xF813EBF8E138D9E1ULL, 0x1133221198B32B98ULL, 0xD970A9D969BBD269ULL, 0x94A733948E89078EULL,
    0x1E223C1E9BB62D9BULL, 0xE920C9E987921587ULL, 0x55FFAA55CE4987CEULL, 0xDF7AA5DF28785028ULL, // 113 ~ 120
    0xA1F859A18C8F038CULL, 0x0D171A0D89800989ULL, 0xE631D7E6BFDA65BFULL, 0x68B8D06842C68442ULL,
    0x99B0299941C38241ULL, 0x0F111E0F2D775A2DULL, 0x54FCA854B0CB7BB0ULL, 0x163A2C16BBD66DBBULL  // 121 ~ 128
};

// name=[Tb1], offset[0x02A0A4FB (44082427)], length[0x00000080 (128)]
_BYTE *Tb1 = (_BYTE *) T1 + 3;

// name=[T2], offset[0x02A0A8F8 (44083448)], length[0x00000080 (128)]
_QWORD T2[128] = {
        0x7C7C84F86363A5C6ULL, 0x7B7B8DF6777799EEULL, 0x6B6BBDD6F2F20DFFULL, 0xC5C554916F6FB1DEULL,
        0x0101030230305060ULL, 0x2B2B7D566767A9CEULL, 0xD7D762B5FEFE19E7ULL, 0x76769AECABABE64DULL, // 1 ~ 8
        0x82829D1FCACA458FULL, 0x7D7D87FAC9C94089ULL, 0x5959EBB2FAFA15EFULL, 0xF0F00BFB4747C98EULL,
        0xD4D467B3ADADEC41ULL, 0xAFAFEA45A2A2FD5FULL, 0xA4A4F7539C9CBF23ULL, 0xC0C05B9B727296E4ULL, // 9 ~ 16
        0xFDFD1CE1B7B7C275ULL, 0x26266A4C9393AE3DULL, 0x3F3F417E36365A6CULL, 0xCCCC4F83F7F702F5ULL,
        0xA5A5F45134345C68ULL, 0xF1F108F9E5E534D1ULL, 0xD8D873AB717193E2ULL, 0x15153F2A31315362ULL, // 17 ~ 24
        0xC7C7529504040C08ULL, 0xC3C35E9D23236546ULL, 0x9696A13718182830ULL, 0x9A9AB52F05050F0AULL,
        0x121236240707090EULL, 0xE2E23DDF80809B1BULL, 0x2727694EEBEB26CDULL, 0x75759FEAB2B2CD7FULL, // 25 ~ 32
        0x83839E1D09091B12ULL, 0x1A1A2E342C2C7458ULL, 0x6E6EB2DC1B1B2D36ULL, 0xA0A0FB5B5A5AEEB4ULL,
        0x3B3B4D765252F6A4ULL, 0xB3B3CE7DD6D661B7ULL, 0xE3E33EDD29297B52ULL, 0x848497132F2F715EULL, // 33 ~ 40
        0xD1D168B95353F5A6ULL, 0xEDED2CC100000000ULL, 0xFCFC1FE320206040ULL, 0x5B5BEDB6B1B1C879ULL,
        0xCBCB468D6A6ABED4ULL, 0x39394B72BEBED967ULL, 0x4C4CD4984A4ADE94ULL, 0xCFCF4A855858E8B0ULL, // 41 ~ 48
        0xEFEF2AC5D0D06BBBULL, 0xFBFB16EDAAAAE54FULL, 0x4D4DD79A4343C586ULL, 0x8585941133335566ULL,
        0xF9F910E94545CF8AULL, 0x7F7F81FE02020604ULL, 0x3C3C44785050F0A0ULL, 0xA8A8E34B9F9FBA25ULL, // 49 ~ 56
        0xA3A3FE5D5151F3A2ULL, 0x8F8F8A054040C080ULL, 0x9D9DBC219292AD3FULL, 0xF5F504F138384870ULL,
        0xB6B6C177BCBCDF63ULL, 0x21216342DADA75AFULL, 0xFFFF1AE510103020ULL, 0xD2D26DBFF3F30EFDULL, // 57 ~ 64
        0x0C0C1418CDCD4C81ULL, 0xECEC2FC313133526ULL, 0x9797A2355F5FE1BEULL, 0x1717392E4444CC88ULL,
        0xA7A7F255C4C45793ULL, 0x3D3D477A7E7E82FCULL, 0x5D5DE7BA6464ACC8ULL, 0x737395E619192B32ULL, // 65 ~ 72
        0x818198196060A0C0ULL, 0xDCDC7FA34F4FD19EULL, 0x2A2A7E5422226644ULL, 0x8888830B9090AB3BULL,
        0xEEEE29C74646CA8CULL, 0x14143C28B8B8D36BULL, 0x5E5EE2BCDEDE79A7ULL, 0xDBDB76AD0B0B1D16ULL, // 73 ~ 80
        0x32325664E0E03BDBULL, 0x0A0A1E143A3A4E74ULL, 0x06060A0C4949DB92ULL, 0x5C5CE4B824246C48ULL,
        0xD3D36EBDC2C25D9FULL, 0x6262A6C4ACACEF43ULL, 0x9595A4319191A839ULL, 0x79798BF2E4E437D3ULL, // 81 ~ 88
        0xC8C8438BE7E732D5ULL, 0x6D6DB7DA3737596EULL, 0xD5D564B18D8D8C01ULL, 0xA9A9E0494E4ED29CULL,
        0x5656FAAC6C6CB4D8ULL, 0xEAEA25CFF4F407F3ULL, 0x7A7A8EF46565AFCAULL, 0x08081810AEAEE947ULL, // 89 ~ 96
        0x787888F0BABAD56FULL, 0x2E2E725C25256F4AULL, 0xA6A6F1571C1C2438ULL, 0xC6C65197B4B4C773ULL,
        0xDDDD7CA1E8E823CBULL, 0x1F1F213E74749CE8ULL, 0xBDBDDC614B4BDD96ULL, 0x8A8A850F8B8B860DULL, // 97 ~ 104
        0x3E3E427C707090E0ULL, 0x6666AACCB5B5C471ULL, 0x030305064848D890ULL, 0x0E0E121CF6F601F7ULL,
        0x35355F6A6161A3C2ULL, 0xB9B9D0695757F9AEULL, 0xC1C1589986869117ULL, 0x9E9EB9271D1D273AULL, // 105 ~ 112
        0xF8F813EBE1E138D9ULL, 0x111133229898B32BULL, 0xD9D970A96969BBD2ULL, 0x9494A7338E8E8907ULL,
        0x1E1E223C9B9BB62DULL, 0xE9E920C987879215ULL, 0x5555FFAACECE4987ULL, 0xDFDF7AA528287850ULL, // 113 ~ 120
        0xA1A1F8598C8C8F03ULL, 0x0D0D171A89898009ULL, 0xE6E631D7BFBFDA65ULL, 0x6868B8D04242C684ULL,
        0x9999B0294141C382ULL, 0x0F0F111E2D2D775AULL, 0x5454FCA8B0B0CB7BULL, 0x16163A2CBBBBD66DULL  // 121 ~ 128
};

// name=[Tb2], offset[0x02A0A8FA (44083450)], length[0x00000080 (128)]
_BYTE *Tb2 = (_BYTE *) T2 + 3;

// name=[T3], offset[0x02A0ACF8 (44084472)], length[0x00000080 (128)]
_QWORD T3[128] = {
        0xF87C7C84C66363A5ULL, 0xF67B7B8DEE777799ULL, 0xD66B6BBDFFF2F20DULL, 0x91C5C554DE6F6FB1ULL,
        0x0201010360303050ULL, 0x562B2B7DCE6767A9ULL, 0xB5D7D762E7FEFE19ULL, 0xEC76769A4DABABE6ULL, // 1 ~ 8
        0x1F82829D8FCACA45ULL, 0xFA7D7D8789C9C940ULL, 0xB25959EBEFFAFA15ULL, 0xFBF0F00B8E4747C9ULL,
        0xB3D4D46741ADADECULL, 0x45AFAFEA5FA2A2FDULL, 0x53A4A4F7239C9CBFULL, 0x9BC0C05BE4727296ULL, // 9 ~ 16
        0xE1FDFD1C75B7B7C2ULL, 0x4C26266A3D9393AEULL, 0x7E3F3F416C36365AULL, 0x83CCCC4FF5F7F702ULL,
        0x51A5A5F46834345CULL, 0xF9F1F108D1E5E534ULL, 0xABD8D873E2717193ULL, 0x2A15153F62313153ULL, // 17 ~ 24
        0x95C7C7520804040CULL, 0x9DC3C35E46232365ULL, 0x379696A130181828ULL, 0x2F9A9AB50A05050FULL,
        0x241212360E070709ULL, 0xDFE2E23D1B80809BULL, 0x4E272769CDEBEB26ULL, 0xEA75759F7FB2B2CDULL, // 25 ~ 32
        0x1D83839E1209091BULL, 0x341A1A2E582C2C74ULL, 0xDC6E6EB2361B1B2DULL, 0x5BA0A0FBB45A5AEEULL,
        0x763B3B4DA45252F6ULL, 0x7DB3B3CEB7D6D661ULL, 0xDDE3E33E5229297BULL, 0x138484975E2F2F71ULL, // 33 ~ 40
        0xB9D1D168A65353F5ULL, 0xC1EDED2C00000000ULL, 0xE3FCFC1F40202060ULL, 0xB65B5BED79B1B1C8ULL,
        0x8DCBCB46D46A6ABEULL, 0x7239394B67BEBED9ULL, 0x984C4CD4944A4ADEULL, 0x85CFCF4AB05858E8ULL, // 41 ~ 48
        0xC5EFEF2ABBD0D06BULL, 0xEDFBFB164FAAAAE5ULL, 0x9A4D4DD7864343C5ULL, 0x1185859466333355ULL,
        0xE9F9F9108A4545CFULL, 0xFE7F7F8104020206ULL, 0x783C3C44A05050F0ULL, 0x4BA8A8E3259F9FBAULL, // 49 ~ 56
        0x5DA3A3FEA25151F3ULL, 0x058F8F8A804040C0ULL, 0x219D9DBC3F9292ADULL, 0xF1F5F50470383848ULL,
        0x77B6B6C163BCBCDFULL, 0x42212163AFDADA75ULL, 0xE5FFFF1A20101030ULL, 0xBFD2D26DFDF3F30EULL, // 57 ~ 64
        0x180C0C1481CDCD4CULL, 0xC3ECEC2F26131335ULL, 0x359797A2BE5F5FE1ULL, 0x2E171739884444CCULL,
        0x55A7A7F293C4C457ULL, 0x7A3D3D47FC7E7E82ULL, 0xBA5D5DE7C86464ACULL, 0xE67373953219192BULL, // 65 ~ 72
        0x19818198C06060A0ULL, 0xA3DCDC7F9E4F4FD1ULL, 0x542A2A7E44222266ULL, 0x0B8888833B9090ABULL,
        0xC7EEEE298C4646CAULL, 0x2814143C6BB8B8D3ULL, 0xBC5E5EE2A7DEDE79ULL, 0xADDBDB76160B0B1DULL, // 73 ~ 80
        0x64323256DBE0E03BULL, 0x140A0A1E743A3A4EULL, 0x0C06060A924949DBULL, 0xB85C5CE44824246CULL,
        0xBDD3D36E9FC2C25DULL, 0xC46262A643ACACEFULL, 0x319595A4399191A8ULL, 0xF279798BD3E4E437ULL, // 81 ~ 88
        0x8BC8C843D5E7E732ULL, 0xDA6D6DB76E373759ULL, 0xB1D5D564018D8D8CULL, 0x49A9A9E09C4E4ED2ULL,
        0xAC5656FAD86C6CB4ULL, 0xCFEAEA25F3F4F407ULL, 0xF47A7A8ECA6565AFULL, 0x1008081847AEAEE9ULL, // 89 ~ 96
        0xF07878886FBABAD5ULL, 0x5C2E2E724A25256FULL, 0x57A6A6F1381C1C24ULL, 0x97C6C65173B4B4C7ULL,
        0xA1DDDD7CCBE8E823ULL, 0x3E1F1F21E874749CULL, 0x61BDBDDC964B4BDDULL, 0x0F8A8A850D8B8B86ULL, // 97 ~ 104
        0x7C3E3E42E0707090ULL, 0xCC6666AA71B5B5C4ULL, 0x06030305904848D8ULL, 0x1C0E0E12F7F6F601ULL,
        0x6A35355FC26161A3ULL, 0x69B9B9D0AE5757F9ULL, 0x99C1C15817868691ULL, 0x279E9EB93A1D1D27ULL, // 105 ~ 112
        0xEBF8F813D9E1E138ULL, 0x221111332B9898B3ULL, 0xA9D9D970D26969BBULL, 0x339494A7078E8E89ULL,
        0x3C1E1E222D9B9BB6ULL, 0xC9E9E92015878792ULL, 0xAA5555FF87CECE49ULL, 0xA5DFDF7A50282878ULL, // 113 ~ 120
        0x59A1A1F8038C8C8FULL, 0x1A0D0D1709898980ULL, 0xD7E6E63165BFBFDAULL, 0xD06868B8844242C6ULL,
        0x299999B0824141C3ULL, 0x1E0F0F115A2D2D77ULL, 0xA85454FC7BB0B0CBULL, 0x2C16163A6DBBBBD6ULL  // 121 ~ 128
};

// name=[Tb3], offset[0x02A0ACF9 (44084473)], length[0x00000080 (128)]
_BYTE *Tb3 = (_BYTE *) T3 + 1;

// name=[T4], offset[0x02A0B0F8 (44085496)], length[0x00000080 (128)]
_QWORD T4[128] = {
        0x84F87C7CA5C66363ULL, 0x8DF67B7B99EE7777ULL, 0xBDD66B6B0DFFF2F2ULL, 0x5491C5C5B1DE6F6FULL,
        0x0302010150603030ULL, 0x7D562B2BA9CE6767ULL, 0x62B5D7D719E7FEFEULL, 0x9AEC7676E64DABABULL, // 1 ~ 8
        0x9D1F8282458FCACAULL, 0x87FA7D7D4089C9C9ULL, 0xEBB2595915EFFAFAULL, 0x0BFBF0F0C98E4747ULL,
        0x67B3D4D4EC41ADADULL, 0xEA45AFAFFD5FA2A2ULL, 0xF753A4A4BF239C9CULL, 0x5B9BC0C096E47272ULL, // 9 ~ 16
        0x1CE1FDFDC275B7B7ULL, 0x6A4C2626AE3D9393ULL, 0x417E3F3F5A6C3636ULL, 0x4F83CCCC02F5F7F7ULL,
        0xF451A5A55C683434ULL, 0x08F9F1F134D1E5E5ULL, 0x73ABD8D893E27171ULL, 0x3F2A151553623131ULL, // 17 ~ 24
        0x5295C7C70C080404ULL, 0x5E9DC3C365462323ULL, 0xA137969628301818ULL, 0xB52F9A9A0F0A0505ULL,
        0x36241212090E0707ULL, 0x3DDFE2E29B1B8080ULL, 0x694E272726CDEBEBULL, 0x9FEA7575CD7FB2B2ULL, // 25 ~ 32
        0x9E1D83831B120909ULL, 0x2E341A1A74582C2CULL, 0xB2DC6E6E2D361B1BULL, 0xFB5BA0A0EEB45A5AULL,
        0x4D763B3BF6A45252ULL, 0xCE7DB3B361B7D6D6ULL, 0x3EDDE3E37B522929ULL, 0x97138484715E2F2FULL, // 33 ~ 40
        0x68B9D1D1F5A65353ULL, 0x2CC1EDED00000000ULL, 0x1FE3FCFC60402020ULL, 0xEDB65B5BC879B1B1ULL,
        0x468DCBCBBED46A6AULL, 0x4B723939D967BEBEULL, 0xD4984C4CDE944A4AULL, 0x4A85CFCFE8B05858ULL, // 41 ~ 48
        0x2AC5EFEF6BBBD0D0ULL, 0x16EDFBFBE54FAAAAULL, 0xD79A4D4DC5864343ULL, 0x9411858555663333ULL,
        0x10E9F9F9CF8A4545ULL, 0x81FE7F7F06040202ULL, 0x44783C3CF0A05050ULL, 0xE34BA8A8BA259F9FULL, // 49 ~ 56
        0xFE5DA3A3F3A25151ULL, 0x8A058F8FC0804040ULL, 0xBC219D9DAD3F9292ULL, 0x04F1F5F548703838ULL,
        0xC177B6B6DF63BCBCULL, 0x6342212175AFDADAULL, 0x1AE5FFFF30201010ULL, 0x6DBFD2D20EFDF3F3ULL, // 57 ~ 64
        0x14180C0C4C81CDCDULL, 0x2FC3ECEC35261313ULL, 0xA2359797E1BE5F5FULL, 0x392E1717CC884444ULL,
        0xF255A7A75793C4C4ULL, 0x477A3D3D82FC7E7EULL, 0xE7BA5D5DACC86464ULL, 0x95E673732B321919ULL, // 65 ~ 72
        0x98198181A0C06060ULL, 0x7FA3DCDCD19E4F4FULL, 0x7E542A2A66442222ULL, 0x830B8888AB3B9090ULL,
        0x29C7EEEECA8C4646ULL, 0x3C281414D36BB8B8ULL, 0xE2BC5E5E79A7DEDEULL, 0x76ADDBDB1D160B0BULL, // 73 ~ 80
        0x566432323BDBE0E0ULL, 0x1E140A0A4E743A3AULL, 0x0A0C0606DB924949ULL, 0xE4B85C5C6C482424ULL,
        0x6EBDD3D35D9FC2C2ULL, 0xA6C46262EF43ACACULL, 0xA4319595A8399191ULL, 0x8BF2797937D3E4E4ULL, // 81 ~ 88
        0x438BC8C832D5E7E7ULL, 0xB7DA6D6D596E3737ULL, 0x64B1D5D58C018D8DULL, 0xE049A9A9D29C4E4EULL,
        0xFAAC5656B4D86C6CULL, 0x25CFEAEA07F3F4F4ULL, 0x8EF47A7AAFCA6565ULL, 0x18100808E947AEAEULL, // 89 ~ 96
        0x88F07878D56FBABAULL, 0x725C2E2E6F4A2525ULL, 0xF157A6A624381C1CULL, 0x5197C6C6C773B4B4ULL,
        0x7CA1DDDD23CBE8E8ULL, 0x213E1F1F9CE87474ULL, 0xDC61BDBDDD964B4BULL, 0x850F8A8A860D8B8BULL, // 97 ~ 104
        0x427C3E3E90E07070ULL, 0xAACC6666C471B5B5ULL, 0x05060303D8904848ULL, 0x121C0E0E01F7F6F6ULL,
        0x5F6A3535A3C26161ULL, 0xD069B9B9F9AE5757ULL, 0x5899C1C191178686ULL, 0xB9279E9E273A1D1DULL, // 105 ~ 112
        0x13EBF8F838D9E1E1ULL, 0x33221111B32B9898ULL, 0x70A9D9D9BBD26969ULL, 0xA733949489078E8EULL,
        0x223C1E1EB62D9B9BULL, 0x20C9E9E992158787ULL, 0xFFAA55554987CECEULL, 0x7AA5DFDF78502828ULL, // 113 ~ 120
        0xF859A1A18F038C8CULL, 0x171A0D0D80098989ULL, 0x31D7E6E6DA65BFBFULL, 0xB8D06868C6844242ULL,
        0xB0299999C3824141ULL, 0x111E0F0F775A2D2DULL, 0xFCA85454CB7BB0B0ULL, 0x3A2C1616D66DBBBBULL  // 121 ~ 128
};

// name=[rcon], offset[0x02A0B4F8 (44086520)], length[0x0000000A (10)]
_DWORD rcon[10] = {
        0x01000000U, 0x02000000U, 0x04000000U, 0x08000000U, 0x10000000U, 0x20000000U, 0x40000000U, 0x80000000U,
        0x1B000000U, 0x36000000U  // 1 ~ 10
};

_DWORD T[] = {
    0x00000000u, 0x1C200000u, 0x38400000u, 0x24600000u, 0x70800000u, 0x6CA00000u, 0x48C00000u, 0x54E00000u,
    0xE1000000u, 0xFD200000u, 0xD9400000u, 0xC5600000u, 0x91800000u, 0x8DA00000u, 0xA9C00000u, 0xB5E00000u,
};

#if 1 // xmmword
__m128i xmmword_0284F970 = { .m128i_u8 = {0x00, 0x00, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00}};
__m128i xmmword_0284FBC0 = { .m128i_u8 = {0x00, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00}};
__m128i xmmword_0284FBD0 = { .m128i_u8 = {0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00}};
__m128i xmmword_0284FBE0 = { .m128i_u8 = {0x00, 0x00, 0x00, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0x00, 0x00, 0x00, 0x00}};
#endif

AES_DATA gAesData ={0,} ;

// https://github.com/CryptoExperts/wb_contest_submission_server/blob/master/aes.c
// 1
//  Expand the cipher key into the encryption key schedule.
int aes_set_encrypt_key(_BYTE *userKey, int bits, AES_KEY *key) { // complete
    int i, j;
    int ret = -1;
    _DWORD v4;
    _DWORD v6;

    if (!userKey || !key)
        return ret;

    if (bits == 0x80 || bits == 0x100 || (ret = -2, bits == 192)) {
        if (bits == 0x80)
            key->rounds = 0x0A;
        else if (bits == 192)
            key->rounds = 0x0C;
        else
            key->rounds = 0x0E;

        for (i = 0; i < 4; i++)
            key->rd_key[i] = ReverseByte(u32p(userKey)[i]);

        if (bits == 0x80) {
            for (i = 0, j = 0; i < 0x28; i += 4, j++) {
                v6 = key->rd_key[i + 3];

                v4 = LB0(u32p(T4)[RB3(v6)] ) ^ LB1(u32p(Tb3)[RB0(v6)]) ^ LB2(u32p(Tb2)[RB1(v6)]) ^ LB3(u32p(Tb1)[RB2(v6)]);

                key->rd_key[i + 4] = key->rd_key[i + 0] ^ v4 ^ rcon[j];
                key->rd_key[i + 5] = key->rd_key[i + 1] ^ key->rd_key[i + 4];
                key->rd_key[i + 6] = key->rd_key[i + 2] ^ key->rd_key[i + 5];
                key->rd_key[i + 7] = key->rd_key[i + 3] ^ key->rd_key[i + 6];
            }
        } else {
            // TODO
        }

        ret = 0;
    }


    return ret;
}

// 2
int aes_encrypt(_BYTE *a1, _BYTE *a2, AES_KEY *ctx) { // a1 : 4*4byte , a2 4*4byte
    _DWORD s0, s1, s2, s3, v6;
    _DWORD v32, d3=0, d2=0, d1=0, d0=0;
    _DWORD *rk = ctx->rd_key;

    s0 = rk[0] ^ ReverseByte(u32p(a1)[0]);
    s1 = rk[1] ^ ReverseByte(u32p(a1)[1]);
    s2 = rk[2] ^ ReverseByte(u32p(a1)[2]);
    s3 = rk[3] ^ ReverseByte(u32p(a1)[3]);

    v6 = ctx->rounds / 2u ;

    for ( int i = 0 ; i < v6 ; i ++ )
    {
        rk += 4;
        d3 = rk[0] ^ u32p(T1)[RB1(s2)] ^ u32p(T2)[RB0(s3)] ^ u32p(T3)[RB3(s0)] ^ u32p(T4)[RB2(s1)];
        d2 = rk[1] ^ u32p(T1)[RB1(s3)] ^ u32p(T2)[RB0(s0)] ^ u32p(T3)[RB3(s1)] ^ u32p(T4)[RB2(s2)];
        d1 = rk[2] ^ u32p(T1)[RB1(s0)] ^ u32p(T2)[RB0(s1)] ^ u32p(T3)[RB3(s2)] ^ u32p(T4)[RB2(s3)];
        d0 = rk[3] ^ u32p(T1)[RB1(s1)] ^ u32p(T2)[RB0(s2)] ^ u32p(T3)[RB3(s3)] ^ u32p(T4)[RB2(s0)];

        if (i == v6 - 1) break;

        rk += 4;
        s0 = rk[0] ^ u32p(T1)[RB1(d1)] ^ u32p(T2)[RB0(d0)] ^ u32p(T3)[RB3(d3)] ^ u32p(T4)[RB2(d2)];
        s1 = rk[1] ^ u32p(T1)[RB1(d0)] ^ u32p(T2)[RB0(d3)] ^ u32p(T3)[RB3(d2)] ^ u32p(T4)[RB2(d1)];
        s2 = rk[2] ^ u32p(T1)[RB1(d3)] ^ u32p(T2)[RB0(d2)] ^ u32p(T3)[RB3(d1)] ^ u32p(T4)[RB2(d0)];
        s3 = rk[3] ^ u32p(T1)[RB1(d2)] ^ u32p(T2)[RB0(d1)] ^ u32p(T3)[RB3(d0)] ^ u32p(T4)[RB2(d3)];
    }

    rk += 4 ;

    u32p(a2)[0] = ReverseByte(
            rk[ 0 ] ^ (LB3(u32p(Tb1)[RB3(d3)]) | LB2(u32p(Tb2)[RB2(d2)]) | LB1(u32p(Tb3)[RB1(d1)]) | LB0(u32p(T4)[RB0(d0)]))
        );

    u32p(a2)[1] = ReverseByte(
            rk[ 1 ] ^ (LB3(u32p(Tb1)[RB3(d2)]) | LB2(u32p(Tb2)[RB2(d1)]) | LB1(u32p(Tb3)[RB1(d0)]) | LB0(u32p(T4)[RB0(d3)]))
    );

    u32p(a2)[2] = ReverseByte(
            rk[ 2 ] ^ (LB3(u32p(Tb1)[RB3(d1)]) | LB2(u32p(Tb2)[RB2(d0)]) | LB1(u32p(Tb3)[RB1(d3)]) | LB0(u32p(T4)[RB0(d2)]))
    );

    u32p(a2)[3] = ReverseByte(
            rk[ 3 ] ^ (LB3(u32p(Tb1)[RB3(d0)]) | LB2(u32p(Tb2)[RB2(d3)]) | LB1(u32p(Tb3)[RB1(d2)]) | LB0(u32p(T4)[RB0(d1)]))
    );
}

_QWORD __PAIR__(_DWORD a, _DWORD b)
{
    _QWORD ret = a ;
    ret = ( ret << 32u ) | b ;
    return ret ;
}
_QWORD __PAIR_R__(_DWORD a, _DWORD b, _DWORD n)
{
    _QWORD ret = __PAIR__(a,b);
    return ret >> n ;
}
#define __PAIR_R1__(a,b) __PAIR_R__(a,b,1u)
#define __PAIR_R2__(a,b) __PAIR_R__(a,b,2u)
#define __PAIR_R3__(a,b) __PAIR_R__(a,b,3u)
#define __PAIR_R4__(a,b) __PAIR_R__(a,b,4u)


_DWORD aes_data_initialize(AES_DATA *s, AES_KEY *key, fnAes function)
{
    _DWORD m21; // ST28_4
    _DWORD m20; // ST4C_4
    _DWORD m23; // ecx
    _BYTE v6; // al
    _DWORD m22; // edx
    _DWORD m11; // ST14_4
    _DWORD m12; // ecx
    _DWORD n21; // ST1C_4
    _DWORD m13; // ST18_4
    _DWORD n22; // ST20_4
    _DWORD n11; // edx
    _DWORD m10; // ebx
    _DWORD n23; // ecx
    _DWORD n20; // edi
    _DWORD n12; // ST30_4
    _DWORD n13; // eax
    _DWORD n10; // ebx
    _DWORD result; // eax
    int i ;

    memset(s, 0, 0x170u);

    s->function = function;
    s->ctx = key;

    function(s->DB1, s->DB1, key);

    m21 = ReverseByte(s->DB4[0]);
    m20 = ReverseByte(s->DB4[1]);
    m23 = ReverseByte(s->DB4[2]);
    m22 = ReverseByte(s->DB4[3]);

    v6 = s->DB1[15];

    s->DB4[0] = m20;
    s->DB4[1] = m21;
    s->DB4[2] = m22;
    s->DB4[3] = m23 ;


    result = m23;

    m10 = (_DWORD)__PAIR_R1__(m21, m20);
    m11 = -(v6 & 1) & 0xE1000000 ^ (m21 >> 1);
    m12 = (_DWORD)__PAIR_R1__(m23, m22);
    m13 = (_DWORD)__PAIR_R1__(m20, m23);

    n20 = (_DWORD)__PAIR_R1__(m11, m10) ;
    n21 = -(m12 & 1) & 0xE1000000 ^ (m11 >> 1);
    n22 = __PAIR_R1__(m13, m12 );
    n23 = (_DWORD)__PAIR_R1__(m10 , m13);

    n10 = (_DWORD)__PAIR_R1__(n21, n20);
    n11 = -(n22 & 1) & 0xE1000000 ^ (n21 >> 1);
    n12 = (_DWORD)__PAIR_R1__(n23, n22);
    n13 = (_DWORD)__PAIR_R1__(n20, n23);
    int j, k, t ;

    _DWORD M[4][4] = {
        {0,   0,   0,   0},
        {m10, m11, m12, m13},
        {m20, m21, m22, m23},
    };
    _DWORD N[4][4] = {
        {0,   0,   0,   0},
        {n10, n11, n12, n13 },
        {n20, n21, n22, n23 },
    };

    for ( j = 0 ; j < 4 ; j ++ )
    {
        M[3][j] = M[1][j] ^ M[2][j];
        N[3][j] = N[1][j] ^ N[2][j];
    }

    t = 4 ;
    for ( i = 0 ; i < 4 ; i ++ )
        for ( j = 0 ; j < 4 ; j ++ )
            for ( k = 0 ; k < 4 ; k ++ )
                s->DB4[t++] = M[i][k] ^ N[j][k];
    return result;
}

/**
 * .text:02424CAE ; _DWORD __cdecl aes_hash_with_random(AES_DATA *a1, _BYTE *randomData, _DWORD le
 * */

int aes_random(AES_DATA *pData, _BYTE *randomData, int len)
{
    int v3;
    _BYTE *v4 ;
    _DWORD v5 = 0; // edi
    signed int v6; // eax
    unsigned int v7; // edx
    int v8; // eax
    _BYTE *v9; // edi
    _DWORD result; // eax
    unsigned int v11; // [esp+8h] [ebp-24h]
    unsigned int v12; // [esp+18h] [ebp-14h]
    pData->DB8[35] = 0LL;
    pData->DA8[0] = 0LL;
    pData->DA8[1] = 0LL;
    pData->DA8[6] = 0LL;
    pData->DA8[7] = 0LL;
    pData->DA8[8] = 0LL;
    pData->DA8[9] = 0LL;

    v3 = len;
    v4 = randomData;

    if ( len == 12 )
    {
        // DA4[0], DA4[1], DA4[2] =
        memcpy((void *)pData, (const void *)randomData, len );
        pData->DA1[15] = 1;
        v5 = 2;
    }
    else
    {
        if (len < 0x10 )
        {
            v7 = len;
        }
        else
        {
            v11 = (len - 16) & 0xFFFFFFF0;
            do
            {
                v12 = v3;
                v6 = -16;
                do
                {
                    pData->DA1[v6 + 16] ^= v4[v6 + 16];
                    ++v6;
                }
                while ( v6 );
                aes_sub_hash_1((_BYTE *)pData, (_BYTE *)&pData->DB4[4]);
                v4 += 16;
                v3 = v12 - 16;
            }
            while ( v12 - 16 > 0xF );
            v7 = len - 16 - v11;
            v3 = len;
            v4 = &randomData[v11 + 16];
        }
        if ( v7 )
        {
            v8 = 0;
            do
            {
                pData->DA1[v8] ^= v4[v8];
                ++v8;
            }
            while ( v7 != v8 );
            v9 = &pData->DB1[16];
            aes_sub_hash_1((_BYTE *)pData, (_BYTE *)&pData->DB4[4]);
            v3 = len;
        }
        else
        {
            v9 = &pData->DB1[16];
        }
        pData->DA1[11] ^= v3 >> 29;
        pData->DA1[12] ^= v3 >> 21;
        pData->DA1[13] ^= v3 >> 13;
        pData->DA1[14] ^= v3 >> 5;
        pData->DA1[15] ^= 8 * (_BYTE)v3;
        aes_sub_hash_1((_BYTE *)pData, (_BYTE *)v9);
        v5 = ReverseByte(pData->DA4[3]) + 1;
    }
    pData->function((_BYTE *)pData, (_BYTE *)&(pData->DA8[4]), pData->ctx);// call sub_A0FD1026 (A08F2F29 if base=0)
    pData->DA4[3] = ReverseByte(v5);
    return v5 >> 16u;
}

int aes_encode_body(AES_DATA *a1, _BYTE *compressedBody, _BYTE *pBuff, _DWORD lenBuff)
{
    _QWORD v5; // kr00_8
    _BYTE *pInData; // esi
    _DWORD v13; // ecx
    _BYTE *pOutData; // [esp+14h] [ebp-38h]
    _BYTE *pOutTmp;
    unsigned int nRemain; // [esp+18h] [ebp-34h]
    fnAes v50; // [esp+34h] [ebp-18h]
    int v52; // [esp+38h] [ebp-14h]
    int i, j;

    v5 = lenBuff + a1->DA8[7];
    if ( v5 > 0xFFFFFFFE0LL )
        return -1;
    v50 = a1->function;
    a1->DA8[7] = v5;
    if ( a1->DB4[71] )
    {
        aes_sub_hash_1(&a1->DA1[64], &a1->DB1[16]);
        a1->DB4[71] = 0;
    }

    v13 = ReverseByte(a1->DA4[3]);
    pInData = compressedBody;
    pOutData = pBuff;

    for (nRemain = lenBuff ; nRemain > 0xC00 ; nRemain -= 0xC00 )
    {
        pOutTmp = pOutData;
        for ( i = 0 ; i < 192 ; i ++ )
        {
            v50((_BYTE *)a1, (_BYTE *)&a1->DA1[16], a1->ctx);
            a1->DA4[3] = ReverseByte(++v13);
            for ( j = 0 ; j < 4 ; j ++ )
                u32p(pOutTmp)[j] = u32p(pInData)[j] ^ a1->DA4[j + 4];
            pOutTmp += 16;
            pInData += 16;
        }

        aes_sub_hash_2((_BYTE *)&a1->DB1[16], (_BYTE *)&a1->DA1[64], (_BYTE *)pOutData, 0xC00);
        pOutData = pOutTmp;
    }
    if ( (v52 = nRemain & 0xFFFFFFF0u) ) {
        pOutTmp = pOutData;
        for (; nRemain >= 0x10; nRemain -= 0x10) {
            v50((_BYTE *) a1, (_BYTE *) &a1->DA1[16], a1->ctx);
            a1->DA4[3] = ReverseByte(++v13);
            for (j = 0; j < 4; j++)
                u32p(pOutTmp)[j] = u32p(pInData)[j] ^ a1->DA4[j + 4];
            pOutTmp += 16;
            pInData += 16;
        }
        aes_sub_hash_2(&a1->DB1[16], &a1->DA1[64], pOutData, v52);
        pOutData = pOutTmp;
    }

    if ( nRemain )
    {
        v50((_BYTE *)a1, &a1->DA1[16], a1->ctx);
        a1->DA4[3] = ReverseByte(++v13);
        for ( i = 0 ; i < nRemain ; i ++ )
        {
            pOutData[i] = pInData[i] ^ a1->DA1[i + 16];
            a1->DA1[i + 64] ^= pOutData[i];
        }
        a1->DB4[70] = nRemain;
    }
    else
    {
        a1->DB4[70] = 0;
    }
    return 0;
}

int aes_decode_body(AES_DATA *a1, _BYTE *pInEncoded_body, _BYTE *pBuff, int len_body)
{
    _QWORD v5; // kr00_8
    _BYTE *pOutData; // esi
    int v13; // ecx
    _BYTE *pOutTmp; // edi
    _BYTE * pInData; // esi
    unsigned int nRemain; // [esp+14h] [ebp-38h]
    fnAes v45; // [esp+34h] [ebp-18h]
    int i, j ;

    v5 = len_body + a1->DA8[7];
    if ( v5 > 0xFFFFFFFE0LL )
        return -1;
    v45 = a1->function;
    a1->DA8[7] = v5;
    if ( a1->DB4[71] )
    {
        aes_sub_hash_1(&a1->DA1[64], (_BYTE *)&a1->DB4[4]);
        a1->DB4[71] = 0;
    }

    v13 = ReverseByte(a1->DA4[3]);
    pInData = pInEncoded_body;
    pOutData = pBuff;

    for ( nRemain = len_body ; nRemain >= 0xC00 ; nRemain -= 0xC00 )
    {
        aes_sub_hash_2((_BYTE *)(&a1->DB4[4]), &a1->DA1[64], pInData, 0xC00);
        pOutTmp = pOutData;
        for ( i = 0 ; i < 192 ; i ++ )
        {
            v45((_BYTE *)a1, (_BYTE *)&a1->DA4[4], a1->ctx);
            a1->DA4[3] = ReverseByte(++v13);
            for ( j = 0 ; j < 4 ; j ++ )
                u32p(pOutTmp)[j] = u32p(pInData)[j] ^ a1->DA4[j + 4];

            pOutTmp += 16;
            pInData += 16;
        }
        pOutData = pOutTmp;
    }

    if (nRemain & 0xFFFFFFF0 )
    {
        aes_sub_hash_2((_BYTE *)&a1->DB4[4], &a1->DA1[64], pInData, nRemain & 0xFFFFFFF0);
        pOutTmp = pOutData;

        for ( ; nRemain >= 0x10 ; nRemain -= 0x10 )
        {
            v45((_BYTE *)a1, &a1->DA1[16], a1->ctx);
            a1->DA4[3] = ReverseByte(++v13);
            for ( j = 0 ; j < 4 ; j ++ )
                u32p(pOutTmp)[j] = u32p(pInData)[j] ^ a1->DA4[j + 4];
            pOutTmp += 16;
            pInData += 16;
        }

        pOutData = pOutTmp;
    }

    if ( nRemain )
    {
        v45((_BYTE *)a1, &a1->DA1[16], a1->ctx);

        a1->DA4[3] = ReverseByte(++v13);

        for ( i = 0 ; i < nRemain ; i ++ )
        {
            a1->DA1[i + 64] ^= pInData[i];
            pOutData[i] = a1->DA1[i + 16] ^ pInData[i];
        }
    }
    return 0;
}

_DWORD aes_sub_hash_1(_BYTE *a1, _BYTE *a2) // InvMixColumns
{
    _DWORD d0, d1, d2, d3; // ecx
    _DWORD s0, s1, s2, s3; // edx
    _DWORD result; // eax
    int i ;
    _DWORD idx ;

    d0 = d1 = d2 = d3 = 0 ;
    for ( i = 15 ; i >= 0 ; i -- )
    {
        idx = 4 * ( a1[ i ] & 0xFu);
        s0 = u32p(a2)[idx + 0] ^ shld(d0, d1, 0x1C);
        s1 = u32p(a2)[idx + 1] ^ u32p(T)[d3 & 0xF] ^ (d0 >> 4);
        s2 = u32p(a2)[idx + 2] ^ shld(d2, d3, 0x1C);
        s3 = u32p(a2)[idx + 3] ^ shld(d1, d2, 0x1C);

        idx = (a1[ i ] & 0xFFFFFFF0u) >> 2u;
        d0 = u32p(a2)[idx + 1] ^ u32p(T)[s2 & 0xF] ^ (s1 >> 4);
        d1 = u32p(a2)[idx + 0] ^ shld(s1, s0, 0x1C );
        d2 = u32p(a2)[idx + 3] ^ shld(s0, s3, 0x1C );
        d3 = u32p(a2)[idx + 2] ^ shld(s3, s2, 0x1C );
    }

    u32p(a1)[0] = ReverseByte(d0) ;
    u32p(a1)[1] = ReverseByte(d1) ;
    u32p(a1)[2] = ReverseByte(d2) ;
    u32p(a1)[3] = ReverseByte(d3) ;

    result = d3 >> 16;
    return result;
}

int aes_sub_hash_2(_BYTE *a1, _BYTE *a2, _BYTE *a3, _DWORD a4)
{
    int result; // eax
    _DWORD v7; // ecx
    _DWORD s0, s1, s2, s3; // edi
    _DWORD d0, d1, d2, d3;
    int i; // [esp+10h] [ebp-28h]
    _DWORD idx;
    result = a4;
    do
    {
        d0 = d1 = d2 = d3 = 0 ;
        for ( i = 15; i >= 0 ; i -- )
        {
            v7 = (_BYTE)(a2[i] ^ a3[i]);
            idx = 4 * (v7 & 0xF);
            s0 = u32p(a1)[idx + 0] ^ shld(d0, d1, 0x1C);
            s1 = u32p(a1)[idx + 1] ^ u32p(T)[d3 & 0xF] ^ (d0 >> 4);
            s2 = u32p(a1)[idx + 2] ^ shld(d2, d3, 0x1C);
            s3 = u32p(a1)[idx + 3] ^ shld(d1, d2, 0x1C);

            idx = (v7 & 0xFFFFFFF0u) >> 2;

            d0 = u32p(a1)[idx + 1] ^ u32p(T)[s2 & 0xF] ^ (s1 >> 4);
            d1 = u32p(a1)[idx + 0] ^ shld(s1, s0, 0x1C) ;
            d2 = u32p(a1)[idx + 3] ^ shld(s0, s3, 0x1C);
            d3 = u32p(a1)[idx + 2] ^ shld(s3, s2, 0x1C);
        }

        u32p(a2)[0] = ReverseByte(d0) ;
        u32p(a2)[1] = ReverseByte(d1) ;
        u32p(a2)[2] = ReverseByte(d2) ;
        u32p(a2)[3] = ReverseByte(d3) ;

        a3 += 16;
        result -= 16;
    }
    while ( result );
    return result;
}

int aes_xmm_hash(_BYTE* a1, _BYTE* a2, int a3)
{
    int result; // eax
    int v4; // edi

    result = 0;
    if ( a3 )
    {
        v4 = 0;
        do
        {
            result |= u8p(a2)[v4] ^ u8p(a1)[v4];
            ++v4;
        }
        while ( a3 != v4 );
    }
    return result;
}

int aes_xmm(__m128i *a1, _BYTE *a2, unsigned int a3)
{
    __m128i v3; // xmm7
    __m128i v6; // xmm0
    __m128i v7; // xmm3
    __m128i v8; // xmm1
    __m128i v9; // xmm5
    __m128i v10; // xmm4
    __int32 v11; // eax
    __int32 v12; // eax
    int result; // eax

    int a = sizeof(__m128i);
    v3 = _mm_loadu_si128(a1 + 3);
    _mm_storeu_si128(a1 + 3, _mm_slli_epi64(v3, 3u));

    if ( a1[22].m128i_i32[2] || a1[22].m128i_i32[3] )
        aes_sub_hash_1((_BYTE *)a1[4].m128i_i8, (_BYTE *)a1[6].m128i_i8);

    v6 = _mm_srli_epi64(v3, 5u);
    v7 = _mm_load_si128((const __m128i *)&xmmword_0284FBC0);
    v8 = _mm_srli_epi64(v3, 0x15u);
    v9 = _mm_load_si128((const __m128i *)&xmmword_0284FBD0);
    v10 = _mm_load_si128((const __m128i *)&xmmword_0284F970);
    _mm_storeu_si128(
        a1 + 4,
        _mm_xor_si128(
            _mm_loadu_si128(a1 + 4),
            _mm_or_si128(
                _mm_or_si128(
                    _mm_or_si128(
                        _mm_or_si128(_mm_and_si128(v6, (__m128i)xmmword_0284FBE0), _mm_and_si128(_mm_srli_epi64(v3, 0x25u), v7)),
                        _mm_and_si128(_mm_srli_epi64(v3, 0x35u), v9)),
                    _mm_slli_epi64(
                        _mm_or_si128(
                            _mm_or_si128(_mm_and_si128(v8, v9), _mm_or_si128(_mm_and_si128(v6, v7), _mm_slli_epi64(v3, 0x1Bu))),
                            _mm_and_si128(_mm_slli_epi64(v3, 0xBu), v10)),
                        0x20u)),
                _mm_and_si128(v8, v10))));

    aes_sub_hash_1((_BYTE *)a1[4].m128i_i8, (_BYTE *)a1[6].m128i_i8);

    v11 = a1[2].m128i_i32[0];
    a1[4].m128i_i32[1] ^= a1[2].m128i_u32[1];
    a1[4].m128i_i32[0] ^= v11;
    v12 = a1[2].m128i_i32[2];
    a1[4].m128i_i32[3] ^= a1[2].m128i_u32[3];
    a1[4].m128i_i32[2] ^= v12;
    if ( a2 && a3 <= 0x10 )
        result = aes_xmm_hash((_BYTE *)a1[4].m128i_i32, a2, a3);
    else
        result = -1;
    return result;

}

int aes_xmm(_BYTE *a1, _BYTE *a2, unsigned int a3)
{
    return aes_xmm((__m128i *)(a1), a2, a3);
}

_BYTE* aes_do_xmm(AES_DATA *a1, void *dest, size_t n)
{
    size_t v3; // eax

    aes_xmm((__m128i *)a1, NULL, 0);

    v3 = 16;
    if ( n < 0x10 )
        v3 = n;

    return (_BYTE *)memcpy(dest, (const void *)&(a1->DA8[8]), v3);
}

AES_DATA *aes_create_data(AES_KEY *pKey, fnAes func)
{
    AES_DATA *pData = &gAesData ;
    memset(pData, 0x00, sizeof(AES_DATA));

    if ( func )
        aes_data_initialize(pData, pKey, func);

    return pData;
}

int encode_string(_BYTE *strKey, int len_strKey, _BYTE *random_data, int len_random_data, _BYTE *strCompressedBody, _BYTE *newBuffer, int len_newBuffer, void *dest, size_t n)
{
    AES_KEY key = {0, };
    AES_DATA *pData ;

    // strKey = 'Wucai6oj0sheiX3p'
    if (aes_set_encrypt_key(strKey, 8 * len_strKey, &key) )
    {
        return -1;
    }

    pData = aes_create_data(&key, aes_encrypt);
    if ( !pData )
    {
        return -1;
    }

    aes_random(pData, random_data, len_random_data);

    if (aes_encode_body(pData, strCompressedBody, newBuffer, (_DWORD)len_newBuffer) )
    {
        return -1;
    }

    if ( dest )
        aes_do_xmm(pData, dest, n);

    // release. (do nothing.)
}

int decode_string(_BYTE *strKey, int len_strKey, _BYTE *random_data, int len_random_data, _BYTE *strCompressedBody, _BYTE *newBuffer, int len_newBuffer, void *dest, size_t n)
{
    AES_KEY key = {0, };
    AES_DATA *pData ;

    // strKey = 'Wucai6oj0sheiX3p'
    if (aes_set_encrypt_key(strKey, 8 * len_strKey, &key) )
    {
        return -1;
    }

    pData = aes_create_data(&key, aes_encrypt);
    if ( !pData )
    {
        return -1;
    }

    aes_random(pData, random_data, len_random_data);

    if (aes_decode_body(pData, strCompressedBody, newBuffer, len_newBuffer) )
    {
        return -1;
    }

    if ( dest )
        aes_do_xmm(pData, dest, n);

    // release. (do nothing.)
}