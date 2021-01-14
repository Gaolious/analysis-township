
#ifndef _TS_UTIL_LOGGER_HEADER_FILE_INCLUDED_
#define _TS_UTIL_LOGGER_HEADER_FILE_INCLUDED_

#ifndef LOG_TAG
#define LOG_TAG  "DEFAULT"
#endif

typedef enum  _LOG_LEVEL_ {
    LOG_LEVEL_VERBOSE,
    LOG_LEVEL_DEBUG,
    LOG_LEVEL_INFO,
    LOG_LEVEL_WARN,
    LOG_LEVEL_ERROR,

    LOG_LEVEL_LAST
} LOG_LEVEL;

#define LOGV(fmt, args...) \
    LOG( LOG_LEVEL_VERBOSE, LOG_TAG, __FILE__, __FUNCTION__, __LINE__, (fmt), ##args )
#define LOGD(fmt, args...) \
    LOG( LOG_LEVEL_DEBUG, LOG_TAG, __FILE__, __FUNCTION__, __LINE__, (fmt), ##args )
#define LOGD_SMS(fmt, args...) \
    LOG( LOG_LEVEL_DEBUG, LOG_TAG, __FILE__, __FUNCTION__, __LINE__, (fmt), ##args )
#define LOGI(fmt, args...) \
    LOG( LOG_LEVEL_INFO, LOG_TAG, __FILE__, __FUNCTION__, __LINE__, (fmt), ##args )
#define LOGW(fmt, args...) \
    LOG( LOG_LEVEL_WARN, LOG_TAG, __FILE__, __FUNCTION__, __LINE__, (fmt), ##args )
#define LOGE(fmt, args...) \
    LOG( LOG_LEVEL_ERROR, LOG_TAG, __FILE__, __FUNCTION__, __LINE__,(fmt),  ##args )

#define LOG_ENTER_FUNCTION() \
    LOGI( "ENTER function" )
#define LOG_LEAVE_FUNCTION() \
    LOGI( "LEAVE function" )

#ifdef    __cplusplus
extern "C" {
#endif

void LOG( LOG_LEVEL log_level, const char *strLogTag, const char *strfilename, const char *strfunction, const int nLine, const char *fmt, ... );
void SetFilenameForLog(const char *strLogFilename, int nDebugLevel );
void SetTmpFilenameForLog();
char* GetTmpFilenameForLog();


#ifdef    __cplusplus
}
#endif

#endif    /* LOGGER_H */

