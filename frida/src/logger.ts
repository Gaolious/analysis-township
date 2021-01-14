
const MAX_FUNCTION_NAME:number  = 15;

function dumpHex(base_addr: NativePointer, length: number): string
{
    let ret = hexdump(
        base_addr, 
        {
            offset:0, 
            length:length, 
            header:true, 
            ansi:false
        }
    );
    return ret;
}

class Logger
{
    static _SEND(log_level:string, func_name:string, msg:string, data?:any): void
    {
        let message = {
            thread_id: Process.getCurrentThreadId(),
            log_level: log_level,
            function: func_name && func_name.length > MAX_FUNCTION_NAME ? func_name.substr(0,MAX_FUNCTION_NAME): func_name,
            msg: msg,
            data:data,
        }
        send(message);
    }
    static DEBUG(func_name:string, msg:string, data?:any): void
    {
        Logger._SEND('D', func_name, msg, data);
    }
    static INFO(func_name:string, msg:string, data?:any): void
    {
        Logger._SEND('I', func_name, msg, data);
    }
    static ERROR(func_name:string, msg:string, data?:any): void
    {
        Logger._SEND('E', func_name, msg, data);
    }
    static TRACE(func_name:string, msg:string, data?:any): void
    {
        Logger._SEND('T', func_name, msg, data);
    }
    static DUMP(func_name:string, msg:string, data?:any): void
    {
        Logger._SEND('P', func_name, msg, data);
        // Logger._SEND('D', func_name, msg, data);
    }
    static DumpMyString(func_name:string, msg:string, base_addr:NativePointer): void
    {
        let b1 = base_addr.readU8();
        let capa = 0;
        let len = 0 ;
        let addr: NativePointer ;
        if ( b1 & 0x01 )
        {
            capa = base_addr.readU32() - 1 ;
            len = base_addr.add(0x04).readU32();
            addr = base_addr.add(0x08).readPointer();
        }
        else 
        {
            capa = 16 - 1 ;
            len = b1 / 2;
            addr = base_addr.add(0x01);
        }
        Logger.DUMP(func_name, msg + ' len=' + len, dumpHex(addr, len));
    }
}

export default Logger;