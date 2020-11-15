#ifndef _MACRO_HEADER_FILE_INCLUDED_
#define _MACRO_HEADER_FILE_INCLUDED_

#define SAFE_DELETE(x) do { \
    if ( (x) == NULL ) \
        break; \
    delete [](x); \
    (x) = NULL ; \
} while (0)

#endif