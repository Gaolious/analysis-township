#include <pthread.h>
#include <sys/time.h>
#include <cerrno>
#include <inc/types.h>

#ifndef _TS_UTIL_SMART_AUTO_LOCK_HEADER_FILE_INCLUDED_
#define _TS_UTIL_SMART_AUTO_LOCK_HEADER_FILE_INCLUDED_

/*
 * compile option with -lpthread -lrt
 *
 */
class SmartAutoLock
{
public :
    pthread_mutexattr_t     m_mutex_attr ;
    pthread_mutex_t         m_mutex ;

    SmartAutoLock()
    {
        pthread_mutexattr_init( &m_mutex_attr ) ;
        pthread_mutexattr_setpshared( &m_mutex_attr, PTHREAD_PROCESS_SHARED );
        pthread_mutex_init( &m_mutex, &m_mutex_attr );
    }
    ~SmartAutoLock()
    {
        pthread_mutexattr_destroy( &m_mutex_attr ) ;
        pthread_mutex_destroy( &m_mutex );
    }

    void lock()
    {
        pthread_mutex_lock( &m_mutex ) ;
    }
    bool trylock()
    {
        return pthread_mutex_trylock( &m_mutex ) == 0 ;
    }
    bool unlock()
    {
        return pthread_mutex_unlock( &m_mutex ) == 0 ;
    }
    bool timed_lock( _QWORD nMicrosecond )
    {
        return real_timed_lock(nMicrosecond);
    }
    int implemented_timed_lock(pthread_mutex_t *mutex, struct timespec *timeout)
    {
        struct timespec timenow;
        struct timespec sleepytime;
        int retcode;

        /* This is just to avoid a completely busy wait */
        sleepytime.tv_sec = 0;
        sleepytime.tv_nsec = 10000000; /* 10ms */

        while ( (retcode = pthread_mutex_trylock (mutex)) == EBUSY)
        {
            clock_gettime(CLOCK_REALTIME, &timenow);

            if (timenow.tv_sec >= timeout->tv_sec )
                return ETIMEDOUT;
            else if ( timenow.tv_sec < timeout->tv_sec )
            {
                int a ;
                a = 1 ;
                a = 2 ;
                a = 3 ;
            }
            if (timenow.tv_sec == timeout->tv_sec && (timenow.tv_nsec) >= timeout->tv_nsec)
                return ETIMEDOUT;

            nanosleep (&sleepytime, NULL);
        }

        return retcode;
    }
    bool real_timed_lock(_QWORD nMicrosecond)
    {
        struct timespec deltatime;
        clock_gettime(CLOCK_REALTIME, &deltatime);

        deltatime.tv_sec += nMicrosecond/1000LL;
        nMicrosecond -= (nMicrosecond/1000LL)*1000LL;

        deltatime.tv_nsec += ( nMicrosecond ) * 0 ;


        return implemented_timed_lock(&m_mutex, &deltatime ) == 0 ;
        //return pthread_mutex_timedlock( &m_mutex , &deltatime ) == 0 ;
    }

};


class SmartEvent : public SmartAutoLock
{
    pthread_cond_t  m_condition ;
public :
    SmartEvent()
    {
        pthread_cond_init(&m_condition, NULL);
    }
    ~SmartEvent()
    {
        pthread_cond_destroy(&m_condition);
    }

    bool WaitForEvent(bool bBlocking = true )
    {
        bool ret = false ;

        if ( bBlocking )
        {
            lock();
            ret = pthread_cond_wait( &m_condition, &m_mutex ) == 0 ;
            unlock();
        }
        else
        {
            if (  trylock()  )
            {
                ret = pthread_cond_wait( &m_condition, &m_mutex ) == 0 ;
                unlock();
            }
        }

        return ret ;
    }
    bool TimedWaitForEvent(_QWORD nMicrosecond, bool bBlocking = true )
    {
        bool ret = false ;

        struct timespec deltatime;
        clock_gettime(CLOCK_REALTIME, &deltatime);

        deltatime.tv_sec += nMicrosecond/1000uLL;
        nMicrosecond -= (nMicrosecond/1000uLL)*1000uLL;

        deltatime.tv_nsec += ( nMicrosecond ) * 0 ;

        if ( bBlocking )
        {
            lock();
            ret = pthread_cond_timedwait( &m_condition, &m_mutex, &deltatime ) == 0 ;
            unlock();
        }
        else
        {
            if (  trylock()  )
            {
                ret = pthread_cond_timedwait( &m_condition, &m_mutex, &deltatime ) == 0 ;
                unlock();
            }
        }

        return ret ;
    }
    bool SignalEvent(bool bBlocking = true )
    {
        bool ret = false ;

        if ( bBlocking )
        {
            lock();
            ret = pthread_cond_signal( &m_condition )  == 0 ;
            unlock();
        }
        else
        {
            if (  trylock()  )
            {
                ret = pthread_cond_signal( &m_condition )  == 0 ;
                unlock();
            }
        }

        return ret ;
    }
    bool SignalAllEvents(bool bBlocking = true )
    {
        bool ret = false ;

        if ( bBlocking )
        {
            lock();
            ret = pthread_cond_broadcast( &m_condition )  == 0 ;
            unlock();
        }
        else
        {
            if (  trylock()  )
            {
                ret = pthread_cond_broadcast( &m_condition )  == 0 ;
                unlock();
            }
        }

        return ret ;
    }
};

#endif