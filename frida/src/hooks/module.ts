import Logger from "./../logger"

type onEnterType = (obj: InvocationContext, args: InvocationArguments) => void;
type onLeaveType = (obj: InvocationContext, args: InvocationReturnValue) => void;

function libgame(fnOnEnter:onEnterType, fnOnLeave:onLeaveType)
{
    let func_name = 'hook_module';
    let addr = null;
    let i ;
    let loaded_libgame = 0 ;

    addr = Module.findExportByName(null, 'android_dlopen_ext');
    if ( !addr )
    {
        Logger.ERROR(func_name, "Failed to find android_dlopen_ext", {addr:addr});
    }
    else 
    {
        Logger.INFO(func_name, "Found android_dlopen_ext", {addr:addr});

        Interceptor.attach(addr, {
            onEnter: function(args) {
                try{
                    let path:string | null = args[0].readCString();
                
                    if ( path && path.indexOf('libgame.so') >= 0)
                    {
                        Logger.INFO(func_name, 'onEnter libgame.so');
                        loaded_libgame = 1;
                        fnOnEnter(this, args);
                    }
                }
                catch (e) {
                    console.log(e);
                }
            },
            onLeave: function(retval){
                if ( loaded_libgame )
                {
                    loaded_libgame = 0;
                    Logger.INFO(func_name, 'onLeave libgame.so');
                    fnOnLeave(this, retval);
                }
            }

        })
    }

}

function libc(fnOnEnter:onEnterType, fnOnLeave:onLeaveType)
{
    let func_name = 'hook_module';
    let addr = null;
    let i ;
    let loaded_libc = 0 ;

    addr = Module.findExportByName(null, 'dlopen');
    if ( !addr )
    {
        Logger.ERROR(func_name, "Failed to find dlopen", {addr:addr});
    }
    else 
    {
        Logger.INFO(func_name, "Found dlopen", {addr:addr});

        Interceptor.attach(addr, {
            onEnter: function(args) {
                try{
                    let path:string | null = args[0].readCString();
                
                    if ( path && path.indexOf('libc.so') >= 0)
                    { 
                        Logger.INFO(func_name, 'onEnter libc.so');
                        loaded_libc = 1;
                        fnOnEnter(this, args);
                    }
                }
                catch(e) {
                    console.log(e);
                }
            },
            onLeave: function(retval){
                if ( loaded_libc )
                {
                    loaded_libc = 0;
                    Logger.INFO(func_name, 'onLeave libc.so');
                    fnOnLeave(this, retval);
                }
            }

        })
    }

}
const hook_module = {
    libgame,
    libc
};

export default hook_module;