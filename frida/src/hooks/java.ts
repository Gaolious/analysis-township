import { url } from "inspector";
import { off } from "process";
import { brotliDecompressSync } from "zlib";
import Logger from "../logger";

let func_name = 'hook_java';

function hook_createHttpRequest()
{
    let func_name = 'createHttpRequest';
    let activity = Java.use('com.playrix.lib.HttpManager');
    activity.createHttpRequest.overload("com.playrix.lib.HttpManager$HttpRequest").implementation = function(req:any)
    {
        let header = [];
        let i ;
        let content = '';

        let buffer = req.content.value ;
        if (buffer)
        {
            content = Array.from( buffer, function(b:number){
                return ('0' + (b & 0xFF).toString(16)).slice(-2)
            }).join('');
        }
        for ( i = 0 ; i < req.headers.value.length ; i += 2 )
            header.push(req.headers.value[i] + ':' + req.headers.value[i+1]);

        Logger.INFO( func_name, 'createHttpRequest', {
            method : req.method.value,
            url : req.url.value,
            body: content,
            body_len: buffer.length,
            contentType : req.contentType.value,
            headers : header
        });
        
        return this.createHttpRequest(req);
    }

}

function hook_inputstream_read(){
    var is = Java.use("java.io.InputStream");

    is.read.overload().implementation = function(){
        let ret = is.read.overload().call(this);
        Logger.DEBUG('inputstream', 'is.read()', {ret:ret});
        return ret;
    }
    
    // InputStream.read(bytes)
    is.read.overload("[B").implementation = function(bArr:any){
        let ret = is.read.overload("[B").call(this, bArr);
        let result = [];
        for(let i = 0; i < ret && i < 5 ; ++i)
        {
            result.push(bArr[i]);
        }

        Logger.DEBUG('inputstream', 'is.read(byte[] bArr)', {ret:ret, result:result});
        return ret;
    }    
}
function hook_createHttpResponse(){

    let func_name = 'createHttpResponse';
    let activity = Java.use('com.playrix.lib.HttpManager');
    activity.createHttpResponse.overload("okhttp3.Response").implementation = function(req:any)
    {
        let ret = this.createHttpResponse(req);
        let header = [];
        let i;


        for ( i = 0 ; i < ret.headers.value.length ; i += 2 )
            header.push(ret.headers.value[i] + ':' + ret.headers.value[i+1]);

        Logger.INFO( func_name, 'createHttpResponse', {
            code: ret.code.value,
            message: ret.message.value, 
            headers: header,
            body: req.body.value,
        });

        return ret;
    }
}

function hook_httpRequestSync()
{
    let func_name = 'hookHttpReq';
    let activity = Java.use('com.playrix.lib.HttpManager');
    activity.httpRequestSync.overload("long", "com.playrix.lib.HttpManager$HttpRequest").implementation = function(j:number, httpRequest:any)
    {
        Logger.INFO( func_name, 'httpRequestSync', {
            allowRedirects : httpRequest.allowRedirects.value, 
            headers : httpRequest.headers.value,
            method : httpRequest.method.value,
            openTimeout :  httpRequest.openTimeout.value,
            readTimeout :  httpRequest.readTimeout.value,
            url : httpRequest.url.value,
        });
        
        let trace = Thread.backtrace(this.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress) ;
        Logger.TRACE( func_name, 'httpRequestSync', trace); 

        return this.httpRequestSync(j, httpRequest);
    }
}

function hook_httpRequestAsync()
{
    let func_name = 'hookHttpReq';
    let activity = Java.use('com.playrix.lib.HttpManager');
    activity.httpRequestAsync.overload("long", "com.playrix.lib.HttpManager$HttpRequest").implementation = function(j:number, httpRequest:any)
    {
        Logger.INFO( func_name, 'httpRequestAsync', {
            allowRedirects : httpRequest.allowRedirects.value, 
            headers : httpRequest.headers.value,
            method : httpRequest.method.value,
            openTimeout :  httpRequest.openTimeout.value,
            readTimeout :  httpRequest.readTimeout.value,
            url : httpRequest.url.value,
        });
        
        let trace = Thread.backtrace(this.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress) ;
        Logger.TRACE( func_name, 'httpRequestAsync', trace); 

        return this.httpRequestAsync(j, httpRequest);
    }
}

function getGenericInterceptor(className:any, func:any, parameters:any) {
	let args = []
	for (let i = 0; i < parameters.length; i++) { 
        	args.push('arg_' + i) 
    }
    var script = "result = this.__FUNCNAME__(__SEPARATED_ARG_NAMES__);\nlogmessage = '__CLASSNAME__.__FUNCNAME__(' + __SEPARATED_ARG_NAMES__ + ') => ' + result;\nconsole.log(logmessage);\nreturn result;"
    
    script = script.replace(/__FUNCNAME__/g, func);
    script = script.replace(/__SEPARATED_ARG_NAMES__/g, args.join(', '));
    script = script.replace(/__CLASSNAME__/g, className);
    script = script.replace(/\+  \+/g, '+');

    args.push(script)
	console.log(args);
}

function hook_native_GetStringUTFChars() {
    var env = Java.vm.getEnv();
    var handlePointer = env.handle.readPointer();
    console.log("\t[*] env handle: " + handlePointer);
    var GetStringUTFChars = handlePointer.add(0x548).readPointer();
    console.log("\t[*] GetStringUTFChars addr: " + GetStringUTFChars);
    Interceptor.attach(GetStringUTFChars, {
        onEnter: function (args) {
            try{
                var String = Java.use("java.lang.String");
                var str = Java.cast(args[1], String);
                if ( str.toString() == 'township.playrix.com')
                {
                    let trace = Thread.backtrace(this.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress) ;
                    Logger.TRACE( func_name, 'httpRequestAsync', trace);                     
                }
                console.log("\t\t[*] GetStringUTFChars: " + str);
            }
            catch(e) {}
        }
    });
};
 
function hook_native_NewStringUTF() {
    var env = Java.vm.getEnv();
    var handlePointer = env.handle.readPointer();
    console.log("\t[*] env handle: " + handlePointer);
    var NewStringUTF = handlePointer.add(0x538).readPointer();
    console.log("\t[*] NewStringUTF addr: " + NewStringUTF);
    Interceptor.attach(NewStringUTF, {
        onEnter: function (args) {
            try{
                var String = Java.use("java.lang.String");
                var str = Java.cast(args[1], String);
    
                console.log("\t\t[*] NewStringUTF: " + str);
            }
            catch(e) {}
        }
    });
};

function hook_java()
{
    hook_createHttpRequest();
    hook_createHttpResponse();
    // hook_httpRequestSync();
    // hook_httpRequestAsync();
    // hook_string();
    // hook_native_NewStringUTF();
    // hook_native_GetStringUTFChars();
    // hook_inputstream_read();
}

export default hook_java;