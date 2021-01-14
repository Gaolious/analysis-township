#include <unistd.h>
#include <stdarg.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include <inc/types.h>
#include <inc/logger.h>
#include <inc/smart_auto_lock.h>

static SmartAutoLock log_race_lock;

#define BUFFER_SIZE (10240)
#define MAX_FILE_NAME_SIZE (FILENAME_MAX)
static LOG_LEVEL gnDebugLevel = LOG_LEVEL_VERBOSE ;


static char gpBuffer[ BUFFER_SIZE ];
static char gstrFilename [ MAX_FILE_NAME_SIZE + 1 ] = {0, } ;
static char gtmpFilename [ MAX_FILE_NAME_SIZE + 1 ] = "/tmp/township.log" ;

void SetFilenameForLog(const char *strLogFilename, int nDebugLevel )
{
    if ( strLogFilename )
    {
        size_t len ;
        FILE *fp = fopen( strLogFilename, "wt");

        if ( fp )
        {
            len = strlen( strLogFilename );
            if ( len < MAX_FILE_NAME_SIZE - 1  )
            {
                if ( nDebugLevel >= 0 && nDebugLevel < (LOG_LEVEL) LOG_LEVEL_LAST)
                {
                    gnDebugLevel = (LOG_LEVEL)nDebugLevel ;
                    strncpy( gstrFilename, strLogFilename , len ) ;
                }
            }
            fclose(fp);
        }
    }
}

void
LOG(
    LOG_LEVEL log_level,
    const char *strLogTag,
    const char *strfilename,
    const char *strfunction,
    const int nLine,
    const char *fmt,
    ...
)
{
    va_list ap ;
    pid_t nThreadID ;
    char *pFilename = (char *)strfilename ;
    int nIdx = 0 ;
    int i ;
    int len ;


    if ( strLogTag == 0 || *strLogTag == 0 ||
         strfilename == 0 || *strfilename == 0 ||
         strfunction == 0 || *strfunction == 0 )
    {
        return ;
    }

    if ( log_level < gnDebugLevel )
        return ;


    log_race_lock.lock();

    nThreadID = pthread_self();
    memset( gpBuffer, 0x00, sizeof(gpBuffer) ) ;

    nIdx = 0 ;
    len = strlen( pFilename ) ;

    for ( i = len - 1 ; i > 0 ; i -- )
        if ( pFilename[i] == '/' )
        {
            nIdx = i + 1;
            break;
        }

    if ( sizeof(nThreadID) == 8 )
        snprintf( gpBuffer, BUFFER_SIZE, "[%s:%llu][%s():%d] ",strLogTag, (_QWORD)nThreadID, strfunction, nLine );
    else
        snprintf( gpBuffer, BUFFER_SIZE, "[%s:%u][%s():%d] ",strLogTag, nThreadID, strfunction, nLine );


    nIdx = strlen(gpBuffer);

    va_start( ap, fmt );
    if ( nIdx < BUFFER_SIZE )
    {
        vsnprintf( gpBuffer + nIdx , BUFFER_SIZE - nIdx,  fmt, ap ) ;
        nIdx = strlen(gpBuffer);
    }
    va_end(ap);

    if ( nIdx < BUFFER_SIZE )
        gpBuffer[nIdx] = 0x00 ;
    else
        gpBuffer[ BUFFER_SIZE - 1 ] = 0x00 ;

    if ( gstrFilename [ 0 ] )
    {
        FILE *fp = fopen( gstrFilename , "at" );
        if ( fp )
        {
            fprintf(fp, "%s\n", gpBuffer ) ;
            fclose(fp);
        }
    }
    else
    {
        printf( "%s\n", gpBuffer ) ;
    }
    log_race_lock.unlock();
}