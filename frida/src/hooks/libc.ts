import Logger from "../logger";

const TRACE_FOPEN = false ;


function _copy_file(src:string|null, dest:string)
{
    const File = Java.use('java.io.File');
    const FileInputStream = Java.use('java.io.FileInputStream');
    const FileOutputStream = Java.use('java.io.FileOutputStream');
    const BufferedInputStream = Java.use('java.io.BufferedInputStream');
    const BufferedOutputStream = Java.use('java.io.BufferedOutputStream');
 
    var destinationFile = File.$new.overload('java.lang.String').call(File, dest);
    if ( destinationFile.exists() ) return true ;

    var sourceFile = File.$new.overload('java.lang.String').call(File, src);

    if (sourceFile.exists() && sourceFile.canRead()) {

        var fileInputStream = FileInputStream.$new.overload('java.io.File').call(FileInputStream, sourceFile);
        var bufferedInputStream = BufferedInputStream.$new.overload('java.io.InputStream').call(BufferedInputStream, fileInputStream);


        var data = 0;
        var i;
        var output = '';
        while ((data = bufferedInputStream.read()) != -1) {
            output += String.fromCharCode(data) ;
        }

        var sp = output.split('\n');
        var ret = false ;
        for ( i = 0 ; i < sp.length ; i ++ )
        {
            if ( sp[i].indexOf('State:') !== -1 )
            {
            }
            else if ( sp[i].indexOf('TracerPid:') !== -1 )
            {
                console.log('chagne ' + sp[i] + ' to "TracerPid:      0"');
                if ( sp[i] == 'TracerPid:      0') continue;
                sp[i] = 'TracerPid:      0';
                ret = true ;
            }
            else if (sp[i].indexOf('frida') !== -1 || sp[i].indexOf('Frida') !== -1 ) 
            {
                sp[i] = '';
            }
        }
        if ( ret === false ) return false ;

        output = sp.join('\n');

        destinationFile.createNewFile();
        var fileOutputStream = FileOutputStream.$new.overload('java.io.File').call(FileOutputStream, destinationFile);
        var bufferedOutputStream = BufferedOutputStream.$new.overload('java.io.OutputStream').call(BufferedOutputStream, fileOutputStream);
        for (i = 0 ; i < output.length ; i ++ )
            bufferedOutputStream.write(output.charCodeAt(i));

        bufferedInputStream.close();
        fileInputStream.close(); 
        bufferedOutputStream.close();
        fileOutputStream.close();
        return true ;
    }
    else {
        console.log('Error : File cannot read.')
    }
}

function is_wanted_filename(path: string|null)
{
    if ( path )
    {
        if ( path.indexOf('/proc') !== -1 )
        {
            if ( path.indexOf('/status' ) !== -1 ) return true ;
            if ( path.indexOf('/maps') !== -1 ) return true ;
        }
    }
    return false ;
}

var FDInfo:{ [id: number]: string; } = {};

function hook_open()
{
    let func_name = 'hook_open';
    let addr:NativePointer | null = null ;

    addr = Module.findExportByName('libc.so', "open") ;
    if ( !addr )
        Logger.ERROR(func_name, "Failed to find open in libc.so");
    else
        Interceptor.attach(addr, {
            onEnter: function(args) 
            {
                let path = args[0].readCString() ;
                this.path = path ;

                if ( path && is_wanted_filename(path) )
                {
                    
                    let new_path = "/sdcard/Android/data/com.playrix.township/files/status_" + this.threadId + '_' + path.replaceAll('/','_') ;
                    Java.perform(function(){ 
                        if ( _copy_file(path, new_path) )
                        {
                            args[0] = Memory.allocUtf8String(new_path)
                            Logger.DEBUG(func_name, 'open', {path: path, mode: args[1], new_path:new_path} );
                        }
                        else 
                        {
                            Logger.DEBUG(func_name, 'open', {path: path, mode: args[1]} );
                        }
                    });
                }
            },
            onLeave: function(retval) {
                FDInfo[retval.toInt32()] = this.path ;
            }
        });
}
var global_xml_fp:any = null ;

function hook_fopen()
{
    let func_name = 'hook_fopen';
    let module_name = 'fopen';
    let addr:NativePointer | null = null ;

    addr = Module.findExportByName('libc.so', module_name) ;
    if ( !addr )
        Logger.ERROR(func_name, "Failed to find open in libc.so");
    else
        Interceptor.attach(addr, {
            onEnter: function(args) 
            {
                this.path = args[0].readCString() ;
                this.mode = args[1].readCString() ;
                let path = this.path ;

                if ( this.path && is_wanted_filename(this.path) )
                {
                    let new_path = "/sdcard/Android/data/com.playrix.township/files/status_" + this.threadId + '_' + this.path.replaceAll('/','_') ;
                    Java.perform(function(){
                        if ( _copy_file(path, new_path) )
                        {
                            args[0] = Memory.allocUtf8String(new_path)
                            Logger.DEBUG(func_name, 'fopen', {path: path, mode: args[1].readCString(), new_path:new_path} );
                        }
                        else 
                        {
                            Logger.DEBUG(func_name, 'fopen', {path: path, mode: args[1].readCString()} );
                        }
                    });


                    if ( TRACE_FOPEN )
                    {
                        let trace = Thread.backtrace(this.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress) ;
                        Logger.TRACE( func_name, module_name, trace);                        
                    }
                }
            },
            onLeave: function(retval) {
                // if ( this.path && this.path.indexOf('playrix.township') >= 0 && this.path.indexOf('.apk') < 0) 
                // {
                //     Logger.DEBUG(func_name, 'fopen', {path: this.path, mode: this.mode, fp:retval} );
                //     // let trace = Thread.backtrace(this.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress) ;
                //     // Logger.TRACE( func_name, module_name, trace);
                //     // global_xml_fp = retval.toUInt32();
                // }                
            }
        });
}
var bHookStartFread = 0;

function start_hook_fread()
{
    bHookStartFread += 1;
}
function end_hook_fread()
{
    bHookStartFread -= 1;
}

function hook_fread()
{
    let func_name = 'hook_fread';
    let module_name = 'fread';
    let addr:NativePointer | null = null ;

    addr = Module.findExportByName('libc.so', module_name) ;
    if ( !addr )
        Logger.ERROR(func_name, "Failed to find open in libc.so");
    else
        Interceptor.attach(addr, {
            onEnter: function(args) 
            {
                this.destBuff = args[0];
                this.elementSize = args[1];
                this.count = args[2];
                this.fp = args[3];
                //Logger.DEBUG(func_name, 'fread', {destBuff: this.destBuff, elementSize: this.elementSize, count:this.count, fp:this.fp} );
            },
            onLeave: function(retval) {
                if ( bHookStartFread > 0 || this.fp.toUInt32() == global_xml_fp )
                {
                    global_xml_fp = this.fp.toUInt32();
                    Logger.DEBUG(func_name, 'fread', {destBuff: this.destBuff, elementSize: this.elementSize, count:this.count, fp:this.fp, ret:retval} );                
                    Logger.DUMP(func_name, 'fread', hexdump(this.destBuff, {offset:0, length:Math.min(0x10,this.count.toUInt32()), header:true, ansi:false}));
                    // let trace = Thread.backtrace(this.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress) ;
                    // Logger.TRACE( func_name, module_name, trace);                    
                }
            }
        });
}
function hook_fwrite()
{
    let func_name = 'hook_fwrite';
    let module_name = 'fwrite';
    let addr:NativePointer | null = null ;

    addr = Module.findExportByName('libc.so', module_name) ;
    if ( !addr )
        Logger.ERROR(func_name, "Failed to find open in libc.so");
    else
        Interceptor.attach(addr, {
            onEnter: function(args) 
            {
                this.destBuff = args[0];
                this.elementSize = args[1];
                this.count = args[2];
                this.fp = args[3];
            },
            onLeave: function(retval) {
                if ( this.fp.toUInt32() == global_xml_fp )
                {
                    Logger.DEBUG(func_name, module_name, {destBuff: this.destBuff, elementSize: this.elementSize, count:this.count, fp:this.fp, ret:retval} );                
                    Logger.DUMP(func_name, module_name, hexdump(this.destBuff, {offset:0, length:this.count.toUInt32(), header:true, ansi:false}));
                    let trace = Thread.backtrace(this.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress) ;
                    Logger.TRACE( func_name, module_name, trace);                    

                }
            }
        });
}

function hook_fclose()
{
    let func_name = 'hook_fclose';
    let module_name = 'fclose';
    let addr:NativePointer | null = null ;

    addr = Module.findExportByName('libc.so', module_name) ;
    if ( !addr )
        Logger.ERROR(func_name, "Failed to find open in libc.so");
    else
        Interceptor.attach(addr, {
            onEnter: function(args) 
            {
                this.fp = args[0];
                if ( this.fp.toUInt32() == global_xml_fp )
                {
                    global_xml_fp = null ;
                    let trace = Thread.backtrace(this.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress) ;
                    Logger.TRACE( func_name, module_name, trace);                    
                }
            },
            onLeave: function(retval) {
            }
        });
}
function hook_fstat()
{
    let func_name = 'hook_fstat';
    let module_name = 'fstat';
    let addr:NativePointer | null = null ;

    addr = Module.findExportByName('libc.so', module_name) ;
    if ( !addr )
        Logger.ERROR(func_name, "Failed to find open in libc.so");
    else
        Interceptor.attach(addr, {
            onEnter: function(args) 
            {
                //let path = args[0].readCString() ;

                //if ( path && is_wanted_filename(path) )
                let fd = args[0].toInt32();
                let path = ''+fd;
                if ( fd in FDInfo )
                {
                    path = FDInfo[fd];
                }
                if ( path && is_wanted_filename(path) )
                    Logger.DEBUG(func_name, module_name, {path:path, arg1: args[1]} );
            },
            onLeave: function(retval) {}
        });
}
function hook_lstat()
{
    let func_name = 'hook_lstat';
    let module_name = 'lstat';
    let addr:NativePointer | null = null ;

    addr = Module.findExportByName('libc.so', module_name) ;
    if ( !addr )
        Logger.ERROR(func_name, "Failed to find open in libc.so");
    else
        Interceptor.attach(addr, {
            onEnter: function(args) 
            {
                let path = args[0].readCString() ;

                if ( path && is_wanted_filename(path) )
                    Logger.DEBUG(func_name, module_name, {path: path, mode: args[1]} );
            },
            onLeave: function(retval) {}
        });
}
function hook_stat()
{
    let func_name = 'hook_stat';
    let module_name = 'stat';
    let addr:NativePointer | null = null ;

    addr = Module.findExportByName('libc.so', module_name) ;
    if ( !addr )
        Logger.ERROR(func_name, "Failed to find open in libc.so");
    else
        Interceptor.attach(addr, {
            onEnter: function(args) 
            {
                let path = args[0].readCString() ;

                if ( path && is_wanted_filename(path) )
                    Logger.DEBUG(func_name, module_name, {path: path, mode: args[1]} );
            },
            onLeave: function(retval) {}
        });
}
function hook_socket(): void 
{
    Process
    .getModuleByName('libc.so')
    .enumerateExports().filter(ex => ex.type === 'function' && ['connect', 'recv', 'send', 'read', 'write'].some(prefix => ex.name.indexOf(prefix) === 0))
    .forEach(ex => {
        Interceptor.attach(ex.address, {
            onEnter: function (args) {
                var fd = args[0].toInt32();
                if (Socket.type(fd) !== 'tcp')
                    return;
                    
                var address: SocketEndpointAddress|null = Socket.peerAddress(fd);
                
                if (address === null)
                    return;
                    
                Logger.DEBUG('hook_socket', ex.name, JSON.stringify(address));
            }
        })
    });
}
function hook_libc(): void
{
    hook_open();
    hook_fopen();
    hook_fread();
    // hook_fwrite();
    // hook_fclose();
    // hook_fstat();
    // hook_lstat();
    // hook_stat();
    hook_socket();
}

// export { hook_libc, start_hook_fread, end_hook_fread } ;
export { hook_libc, start_hook_fread, end_hook_fread}