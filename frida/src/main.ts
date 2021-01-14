import Logger from "./logger";
import hook_ssl_pinning from "./hooks/ssl"
import hook_module from "./hooks/module"
import { hook_libgame } from "./hooks/libgame_7.9.5"
import {hook_libc} from "./hooks/libc"
import hook_java from "./hooks/java"

Logger.INFO("MAIN", "start to hook");

function onLoadEmpty(obj:InvocationContext, args:InvocationArguments){}
function onLoadedEmpty(obj:InvocationContext, args:InvocationReturnValue){}

function onLoadedLibgame(obj:InvocationContext, ret:InvocationReturnValue)
{
    hook_libgame();
    for ( let i = 0 ; i < 30 ; i ++)
    {
        Logger.DEBUG('onload libgame.so', 'sleep ' + (i+1) + ' / 30');
        Thread.sleep(1)
    }
}

// function onLoadLibc(obj:InvocationContext, args:Inv ocationReturnValue)
// {
//     hook_libc();
// }

Java.perform(function(){
    hook_ssl_pinning();
    hook_java();
    hook_module.libgame(onLoadEmpty, onLoadedLibgame);
    //hook_module.libc(onLoadEmpty, onLoadLibc);
    hook_libc();
})
