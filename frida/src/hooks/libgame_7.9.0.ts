import { memoryUsage, off } from "process";
import Logger from "../logger";

const is_arm64 = false ;

/**
 * Access to /proc/[pid]/status 
 *           /proc/self/status 
 *           /proc/../task/[pid]/status
 *           /proc/../task/self/status
 */
function hook_proc_status(base_addr: NativePointer): void
{
    // .text:0000000001F180B4 ; =============== S U B R O U T I N E =======================================
    // .text:0000000001F180B4
    // .text:0000000001F180B4
    // .text:0000000001F180B4 sub_1F180B4                             ; CODE XREF: sub_765FD4:loc_7666C4↑p
    // .text:0000000001F180B4                                         ; sub_1527514↑j ...    
    //
    // .text:0000000001F180E8 ;   try {
    // .text:0000000001F180E8                 ADRP            X2, #aProc@PAGE ; "/proc/"
    // .text:0000000001F180EC                 ADD             X2, X2, #aProc@PAGEOFF ; "/proc/"
    // .text:0000000001F180F0                 ADD             X0, SP, #0xD0+var_B8
    // .text:0000000001F180F4                 MOV             W3, #6
    // .text:0000000001F180F8                 MOV             X1, XZR
    // .text:0000000001F180FC                 BL              sub_79E180
    // .text:0000000001F180FC ;   } // starts at 1F180E8
    // .text:0000000001F18100                 LDR             X8, [X0,#0x10]
    // .text:0000000001F18104                 LDR             Q0, [X0]
    // .text:0000000001F18108                 STR             X8, [SP,#0xD0+var_90]
    // .text:0000000001F1810C                 STR             Q0, [SP,#0xD0+var_A0]
    // .text:0000000001F18110                 STP             XZR, XZR, [X0,#8]
    // .text:0000000001F18114                 STR             XZR, [X0]
    // .text:0000000001F18118 ;   try {
    // .text:0000000001F18118                 ADRP            X1, #aStatus_0@PAGE ; "/status"
    // .text:0000000001F1811C                 ADD             X1, X1, #aStatus_0@PAGEOFF ; "/status"
    // .text:0000000001F18120                 ADD             X0, SP, #0xD0+var_A0
    // .text:0000000001F18124                 MOV             W2, #7
    // .text:0000000001F18128                 BL              sub_77A14C   

    let addr = null;
    let i ;
    let loaded_libc = 0 ;
    let func_name = 'proc_status';
    let offset ;
    if ( is_arm64 )
        offset = 0x1F180B4 ;
    else 
        offset = 0x20738D8 ;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            Logger.INFO(func_name, 'called');
        }, 
        onLeave: function(retval) {
            Logger.DEBUG(func_name, 'return new value(0x0)', {old_ret:retval});
            retval.replace(ptr('0x0'));
        }
    })
}

/**
 * check if exists 
 *           /system/bin/su
 *           /system/xbin/su
 *           /data/local/xbin/su
 *           /data/local/bin/su
 *           /sbin/su
 *           /sbin/magisk
 *           /sbin/magiskhide
 *           /sbin/magiskpolicy
 *           /system/sd/xbin/su
 *           /system/bin/failsafe/su
 *           /system/xbin/bstk/su
 *           /dev/sbin/bind/su
 *           /dev/sbin/bind/magisk
 *           /dev/sbin/bind/magiskhide
 *           /dev/sbin/bind/magiskpolicy
 *           /init.magisk.rc
 *           /init.superuser.rc
 *           /su
 *           /su/lib/libsupol.so
 */
function hook_check_rooting(base_addr: NativePointer): void 
{
    let addr = null;
    let i ;
    let loaded_libc = 0 ;
    let func_name = 'check_rooting';
    let offset ;
    if (is_arm64) offset = 0x1F190F4;
    else offset = 0x2074AF3 ;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            Logger.INFO(func_name, 'called');
        }, 
        onLeave: function(retval) {
            Logger.DEBUG(func_name, 'return new value(0x0)', {old_ret:retval});
            retval.replace(ptr('0x0'));
        }
    })    
}

/**
 * check if exist
 *      FINGERPRINT
 *              "vbox86p|ttvm_hdragon|(^andyos/)"
 *              genymotion, tiantianvm, google_sdk, sdk_x86, vbox86p, goldfish, vbox86, ttVM_x86
 *      /dev   
 *              vboxguest,vboxuser,memuuser, memufp, memufp_audio, memufp_command, memufp_ime, memufp_memud, memufp_vinput, bst_gps, bstpgaipc, qemu_pipe, vmci,
 *      / 
 *              fstab.andy,ueventd.andy.rc,init.andy.rc,init.andy.cloud.rc,init.andy.desktop.rc,fstab.nox,init.nox.rc,ueventd.nox.rc,ueventd.android_x86.rc,x86.prop,ueventd.ttVM_x86.rc,init.ttVM_x86.rc,init.vbox86.rc,ueventd.vbox86.rc
 *      /etc
 *              init.microvirt.sh,,init.nox.sh,,init.andy.sh,,vmci-reachability.andy.sh,logging.andy.sh
 *      /system/lib/egl
 *              libGLES_bst.so, libEGL_emulation.so, libGLESv1_CM_emulation.so, libGLESv2_emulation.so, libEGL_swiftshader.so, libGLESv1_CM_swiftshader.so, libGLESv2_swiftshader.so, libGLESv2_tiantianVM.so, 
 *      /vendor/lib/egl
 *              libGLES_bst.so, libEGL_emulation.so, libGLESv1_CM_emulation.so, libGLESv2_emulation.so, libEGL_swiftshader.so, libGLESv1_CM_swiftshader.so, libGLESv2_swiftshader.so, libGLESv2_tiantianVM.so, 
 *      /system/lib
 *              libbstfolder_jni.so, libpga.so, libnoxd.so, libnoxspeedup.so, vboxguest.ko, vboxsf.ko, libmicrovirt.so, memuguest.ko, memusf.ko, vmci.ko, vmhgfs.ko, libvmware-rpc.so, andypipe.ko, libandy-hostconn-server.so, libandy-proto-cpp.so, libandybattery.so, libandyprop.so, 
 *      /system/bin
 *              bstfolder_ctl, bstfolderd, bstshutdown, bstshutdown_core, bstsvcmgrtest, bstsyncfsenable_nox, nox, nox-prop, nox-vbox-sf, noxd, noxscreen, noxspeedup, shellnox, memud, microvirt-prop, microvirt-vbox-sf, microvirt_setprop, microvirtd, mount.vboxsf, andy-hostconn-server, andy-prop, andy-prop-binder-service, andy-prop-zmq-server, andy-reachability, andy-vbox-sf, mount.vmhgfs, 
 *      /system/usr/keychars
 *              nox_gpio.kcm
 *      /system/usr/keylayout
 *              nox_gpio.kl,Andy_Virtual_Input.kl,Andy_Virtual_Joystick.kl,
 *      ...
 */
function hook_check_emulator(base_addr: NativePointer): void 
{
    let addr = null;
    let i ;
    let loaded_libc = 0 ;
    let func_name = 'check_emulator';
    let offset ;
    if (is_arm64)
        offset = 0x1F1B1E4;
    else
        offset = 0x2077719;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            Logger.INFO(func_name, 'called');
        }, 
        onLeave: function(retval) {
            Logger.DEBUG(func_name, 'return new value(0x0)', {old_ret:retval});
            retval.replace(ptr('0x0'));
        }
    })      
}
function hook_sub_0x2D0052(base_addr: NativePointer): void 
{
    let addr = null;
    let i ;
    let loaded_libc = 0 ;
    let func_name = 'sub_0x2D0052';
    let offset ;
    if (is_arm64)
        offset = 0x2D0052;
    else
        offset = 0x2D0052;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            let msg = args[1].readCString();
            if ( msg=='i' || msg == 'new' || msg == '/dev/urandom' || msg == 'text/plain' || msg == 'POST' )
            {
                Logger.INFO(func_name, 'called', {a1:args[0], a2:msg});
                let trace = Thread.backtrace(this.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress) ;
                Logger.TRACE( func_name, 'sub_0x2D0052', trace);                  
            }
        }, 
        onLeave: function(retval) {
        }
    })      
}

// function hook_proc_maps(base_addr: NativePointer): void 
// {
//     let addr = null;
//     let i ;
//     let loaded_libc = 0 ;
//     let func_name = 'proc_maps';
//     let offset = 0x1F2A384;

//     Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
//     Interceptor.attach( base_addr.add(offset), {
//         onEnter: function(args) {
//             Logger.INFO(func_name, 'called');
//         }, 
//         onLeave: function(retval) {
//             Logger.DEBUG(func_name, '(NEED CHECK) return', {old_ret:retval});
//         }
//     })      
// }
// function hook_sub_1F18268(base_addr: NativePointer): void 
// {
//     let addr = null;
//     let i ;
//     let loaded_libc = 0 ;
//     let func_name = 'sub_1F18268';
//     let offset = 0x1F18268;

//     Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
//     Interceptor.attach( base_addr.add(offset), {
//         onEnter: function(args) {
//             Logger.INFO(func_name, 'called');
//         }, 
//         onLeave: function(retval) {
//             Logger.DEBUG(func_name, 'return (replace to 0x0)', {old_ret:retval});
//             retval.replace(ptr('0x0'));
//         }
//     })      
// }
// function hook_sub_816C84(base_addr: NativePointer): void 
// {
//     {
//         let addr = null;
//         let i ;
//         let loaded_libc = 0 ;
//         let func_name = 'sub_816C84';
//         let offset = 0x816C84;
    
//         Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
//         Interceptor.attach( base_addr.add(offset), {
//             onEnter: function(args) {
//                 Logger.INFO(func_name, 'called');
//             }, 
//             onLeave: function(retval) {
//                 // 뭔지 모를 주소값..
//                 //              0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  0123456789ABCDEF
//                 // 731857b5c8  48 6b d1 14 73 00 00 00 40 56 55 19 73 00 00 00  Hk..s...@VU.s...
//                 // 731857b5d8  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
//                 // 731857b5e8  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
//                 // 731857b5f8  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................                
//                 Logger.DEBUG(func_name, '(NEED CHECK) return', {old_ret:retval});
//                 // let dump = hexdump(retval, {offset:0, length:64, header:true, ansi:false});
//                 // Logger.DUMP(func_name, '', dump)
//             }
//         })      
//     }
// }

function binaryToHexToAscii(array:any, readLimit:number) {
    var result = [];
    // read 100 bytes #performance
    //console.log(array);
    readLimit = readLimit || 100;

    for (var i = 0; i < readLimit; ++i) 
    {
        let t = '0' + (array[i] & 0xFF).toString(16);
        result.push('\\x' + t.slice(-2));
    }
    return '"' + result.join('') + '"';
}
function dumpHex(base_addr: NativePointer, length: number): string
{
    let ret = '';
    if ( length > 100 )
    {
        ret = 'original size : ' + length + '. and cut 100\n';
        length = 100;
    }
    if ( 0 ) {
        let arr:any = base_addr.readByteArray(length);
        let arr2 = new Uint8Array(arr);

        
        ret = binaryToHexToAscii(arr2, length);
        return ret;
    }
    if (1)
    {
        ret += hexdump(
            base_addr, 
            {
                offset:0, 
                length:length, 
                header:true, 
                ansi:false
            }
        );
    }
    return ret;
}
function dumpMyString(base_addr: NativePointer): string
{
    let size = base_addr.readU32();
    let ptr: NativePointer ;
    let capacity: number ;

    if ( size & 1 )
    {
        size = size - 1 ;
        capacity = base_addr.add(4).readU32();
        ptr = base_addr.add(8).readPointer();
    }
    else 
    {
        size = size >> 1 ;
        ptr = base_addr.add(0);
    }
    let ret = '';
    // if ( size > 100 )
    // {
    //     ret = 'original size : ' + size + '. and cut 100\n';
    //     size = 100;
    // }

    ret += hexdump(
        ptr, 
        {
            offset:0, 
            length:size, 
            header:true, 
            ansi:false
        }
    );
    return ret;

}
function hook_header_value(base_addr: NativePointer): void 
{
    let addr = null;
    let i ;
    let loaded_libc = 0 ;
    let func_name = 'encode_http_header_value';
    let offset = 0x9F37C414 - 0x9EC40000;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            if (Maybe_Create_Headers_is_called)
            {
                this.p1 = args[0];
                this.p2 = args[1];
                this.p3 = args[2];
    
                Logger.DUMP(func_name, 'Input param1', dumpMyString(this.p1) );
                Logger.DUMP(func_name, 'Input param2', dumpMyString(this.p2) );
                Logger.DUMP(func_name, 'Input param3', dumpMyString(this.p3) );
            }
        }, 
        onLeave: function(retval) {
            if (Maybe_Create_Headers_is_called)
            {
                Logger.DUMP(func_name, 'Output param1', dumpMyString(this.p1) );
                Logger.DUMP(func_name, 'Output param2', dumpMyString(this.p2) );
                Logger.DUMP(func_name, 'Output param3', dumpMyString(this.p3) );
            }
        }
    })       
}
function hook_decode_http_header_key(base_addr: NativePointer): void 
{
    let addr = null;
    let i ;
    let loaded_libc = 0 ;
    let func_name = 'decode_http_header_key';
    let offset = 0xA0C966D7 - 0x9EC40000;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p1 = args[0];
            this.p2 = args[1];
            this.p3 = args[2];

            //let len = this.p3.readU32();
            //Logger.DUMP(func_name, 'Input param1', dumpMyString(this.p1) );
            Logger.DEBUG(func_name, 'Input param1', dumpHex(this.p1, 0xff ) );
            Logger.DUMP(func_name, 'Input param2', dumpHex(this.p2, 0xff ) );
            Logger.DUMP(func_name, 'Input param3', dumpHex(this.p3, 4) );
        }, 
        onLeave: function(retval) {
            //let len = this.p3.readU32();
            // Logger.DUMP(func_name, 'Output param1', dumpMyString(this.p1) );
            // Logger.DUMP(func_name, 'Output param2', dumpHex(this.p2, len ) );
            // Logger.DUMP(func_name, 'Output param3', dumpHex(this.p3, 4) );
        }
    })         
}
// function unsigned int __cdecl sub_9F082662(int a1, MyString *a2, MyString *a3)
function hook_sub_9F082662(base_addr: NativePointer): void 
{
    let addr = null;
    let i ;
    let loaded_libc = 0 ;
    let func_name = 'sub_9F082662';
    let offset = 0x9F082662 - 0x9EC40000;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p1 = args[0];
            this.p2 = args[1];
            this.p3 = args[2];

            Logger.DUMP(func_name, 'Input param1', dumpHex(this.p1, 0xFF) );
            Logger.DUMP(func_name, 'Input param2', dumpMyString(this.p2) );
            Logger.DUMP(func_name, 'Input param3', dumpMyString(this.p3) );
        }, 
        onLeave: function(retval) {
            let len = this.p3.readU32();
            Logger.DUMP(func_name, 'Output param1', dumpHex(this.p1, 0xFF) );
            Logger.DUMP(func_name, 'Output param2', dumpMyString(this.p2) );
            Logger.DUMP(func_name, 'Output param3', dumpMyString(this.p2) );
        }
    })         
}
var Maybe_Create_Headers_is_called = false ;
// MyString *__cdecl Maybe_Concat(MyString *a1, void *src, size_t n)
function hook_Maybe_Concat(base_addr: NativePointer): void 
{
    let addr = null;
    let i ;
    let loaded_libc = 0 ;
    let func_name = 'Maybe_Concat';
    let offset = 0x9EF13A34 - 0x9EC40000;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            if (Maybe_Create_Headers_is_called)
            {
                this.p1 = args[0];
                this.p2 = args[1];
                this.p3 = args[2];

                //Logger.DUMP(func_name, 'Input src', dumpHex(this.p2, this.p3) );
            }
        }, 
        onLeave: function(retval) {
            if (Maybe_Create_Headers_is_called)
            {
                //Logger.DUMP(func_name, 'Output', retval );
            }          
        }
    })         
}
function hook_Maybe_Create_Headers(base_addr: NativePointer): void 
{
    //9F080A93
    let addr = null;
    let i ;
    let loaded_libc = 0 ;
    let func_name = 'Maybe_Create_Headers';
    let offset = 0x9F080A93 - 0x9EC40000;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            Maybe_Create_Headers_is_called = true ;
            Logger.DEBUG(func_name, 'is_called');
        }, 
        onLeave: function(retval) {
            Maybe_Create_Headers_is_called = false ;
            Logger.DEBUG(func_name, 'is_leave');
        }
    })         
}
function hook_encode_string_aes(base_addr: NativePointer):void 
{
    // .text:A07291A0 ; int __cdecl encode_string_aes(_BYTE *strKey, int len_strKey, _BYTE *random_data, int len_random_data, _BYTE *strCompressedBody, _BYTE *newBuffer, int len_newBuffer, void *dest, size_t n)
   
    let addr = null;
    let i ;
    let loaded_libc = 0 ;
    let func_name = 'encodeBody';
    let offset = 0xA07291A0 - 0x9EC40000;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.pKey = args[0];
            this.nKey = args[1].toInt32();
            this.pRand = args[2];
            this.nRand = args[3].toInt32();
            this.pBody = args[4];
            this.pBuff = args[5];
            this.nBuff = args[6].toInt32();
            this.pDest = args[7];
            this.nDest = args[8].toInt32();
        }, 
        onLeave: function(retval) {
            Logger.DUMP(func_name, 'Output pKey len=' + this.nKey, dumpHex(this.pKey, this.nKey) );
            Logger.DUMP(func_name, 'Output pRand len=' + this.nRand, dumpHex(this.pRand, this.nRand) );
            Logger.DUMP(func_name, 'Output pBody len=' + this.nBuff, dumpHex(this.pBody, this.nBuff) );
            Logger.DUMP(func_name, 'Output pBuff len=' + this.nBuff, dumpHex(this.pBuff, this.nBuff) ); // http body
            Logger.DUMP(func_name, 'Output pDest len=0x10', dumpHex(this.pDest, this.nDest) );
        }
    })       
}
function hook_decode_string_aes(base_addr: NativePointer):void 
{
    // .text:A07291A0 ; int __cdecl encode_string_aes(_BYTE *strKey, int len_strKey, _BYTE *random_data, int len_random_data, _BYTE *strCompressedBody, _BYTE *newBuffer, int len_newBuffer, void *dest, size_t n)
   
    let addr = null;
    let i ;

    let loaded_libc = 0 ;
    let func_name = 'decodeAes';
    let offset = 0x01AE9337;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.pKey = args[0];
            this.nKey = args[1].toInt32();
            this.pRand = args[2];
            this.nRand = args[3].toInt32();
            this.pBody = args[4];
            this.pBuff = args[5];
            this.nBuff = args[6].toInt32();
            this.pDest = args[7];
            this.nDest = args[8].toInt32();
        }, 
        onLeave: function(retval) {
            Logger.DEBUG(func_name, 'Output pKey len=' + this.nKey, dumpHex(this.pKey, this.nKey) );
            Logger.DEBUG(func_name, 'Output pRand len=' + this.nRand, dumpHex(this.pRand, this.nRand) );
            Logger.DEBUG(func_name, 'Output pBody len=' + this.nBuff, dumpHex(this.pBody, this.nBuff) );
            Logger.DEBUG(func_name, 'Output pBuff len=' + this.nBuff, dumpHex(this.pBuff, this.nBuff) ); // http body
            Logger.DEBUG(func_name, 'Output pDest len=0x10', dumpHex(this.pDest, this.nDest) );
        }
    })       
}
function hook_aes_setup(base_addr: NativePointer):void 
{
    // .text:A1071A14 ; signed int __cdecl encode_aes_setup(_BYTE *a1, int a2, AES_CONTEXT *a3)
    let addr = null;
    let i ;
    let loaded_libc = 0 ;
    let func_name = '1.aes_setup';
    let offset = 0xA1071A14 - 0x9EC40000;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            if (Maybe_Create_Headers_is_called)
            {
                // (_BYTE *a1, int a2, AES_CONTEXT *a3)
                this.a1 = args[0];
                this.a2 = args[1]; // len * 8
                this.a3 = args[2]; // size = 60 * 4 + 1*4
                this.len_a3 = 60 * 4 + 1*4
                dump_AesTable(base_addr);
                Logger.DUMP(func_name, 'Input a1 len=' + this.a2, dumpHex(this.a1, this.a2/8) );
                Logger.DUMP(func_name, 'Input a3 len=' + this.len_a3, dumpHex(this.a3, this.len_a3) );
            }
        }, 
        onLeave: function(retval) {
            if (Maybe_Create_Headers_is_called)
            {
                dump_AesTable(base_addr);
                Logger.DEBUG(func_name, 'Output ret =' + retval);
                Logger.DUMP(func_name, 'Output a1 len=' + this.a2, dumpHex(this.a1, this.a2/8) );
                Logger.DUMP(func_name, 'Output a3 len=' + this.len_a3, dumpHex(this.a3, this.len_a3) );
            }          
        }
    })       
}
let len_aes_key = 60*4 + 4;
let len_aes_data = 0x178;
function LogAES_DATA(func_name:string, inout_title: string, addr:NativePointer): void 
{
    Logger.DUMP(func_name, inout_title + ' AES_DATA len=' + len_aes_data, dumpHex(addr, len_aes_data) );
}
function LogAES_KEY(func_name:string, inout_title: string, addr:NativePointer): void 
{
    Logger.DUMP(func_name, inout_title + ' AES_KEY (invole addresses of ctx and encrpt func) len=' + len_aes_key, dumpHex(addr, len_aes_key) );
}
function hook_create_custom_aes_data(base_addr: NativePointer):void 
{
    // .text:A10660A0 ; AesCustomData *__cdecl create_custom_aes_data(AES_CONTEXT *a1, int fnHash)
    let addr = null;
    let i ;
    let loaded_libc = 0 ;
    let func_name = '2.create_custom_aes_data';
    let offset = 0XA10660A0 - 0x9EC40000;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            if (Maybe_Create_Headers_is_called)
            {
                // (_BYTE *a1, int a2, AES_CONTEXT *a3)
                this.a1 = args[0];
                Logger.DUMP(func_name, 'Input a1 len=' + this.lenAesContext, dumpHex(this.a1, len_aes_key) );
            }
        }, 
        onLeave: function(retval) {
            if (Maybe_Create_Headers_is_called)
            {
                Logger.DEBUG(func_name, 'Output ret =' + retval);
                Logger.DUMP(func_name, 'Output a1 len=' + this.lenAesContext, dumpHex(this.a1, len_aes_key) );
                Logger.DUMP(func_name, 'Output ret(cutom)', dumpHex(retval, len_aes_data) );
            }          
        }
    })       
}

function hook_aes_hash_with_random(base_addr: NativePointer): void
{
    // .text:A1064CAE ; unsigned __int32 __cdecl aes_hash_with_random(AesCustomData *a1, _BYTE *randomData, unsigned int len)
    let addr = null;
    let i ;
    let loaded_libc = 0 ;
    let func_name = '3.aes_hash_with_random';
    let offset = 0xA1064CAE - 0x9EC40000;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            if (Maybe_Create_Headers_is_called)
            {
                // (_BYTE *a1, int a2, AES_CONTEXT *a3)
                this.pAesData = args[0];
                this.pRand = args[1];
                this.nRand = args[2].toInt32();
                
                let ctx_addr = this.pAesData.add(0x174).readPointer();
                
                Logger.DUMP(func_name, 'Input pCutom', dumpHex(this.pAesData, len_aes_data) );
                Logger.DUMP(func_name, 'Input pRand len=' + this.nRand, dumpHex(this.pRand, this.nRand) );
                Logger.DUMP(func_name, 'Input ctx len=' + len_aes_key, dumpHex(ctx_addr, len_aes_key) );
            }
        }, 
        onLeave: function(retval) {
            if (Maybe_Create_Headers_is_called)
            {
                Logger.DEBUG(func_name, 'Output ret =' + retval);
                Logger.DUMP(func_name, 'Output pCutom', dumpHex(this.pAesData, len_aes_data) );
                Logger.DUMP(func_name, 'Output pRand len=' + this.nRand, dumpHex(this.pRand, this.nRand) );
                let ctx_addr = this.pAesData.add(0x174).readPointer();
                Logger.DUMP(func_name, 'Output ctx len=' + len_aes_key, dumpHex(ctx_addr, len_aes_key) );
            }          
        }
    })     
}

function hook_aes_do_body(base_addr: NativePointer): void
{
    // .text:A1065277 ; signed int __cdecl aes_do_body(AesCustomData *a1, _BYTE *strCompressedBody, _BYTE *a3, int a4)
    let addr = null;
    let i ;
    let loaded_libc = 0 ;
    let func_name = '4.aes_do_body';
    let offset = 0xA1065277 - 0x9EC40000;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            if (Maybe_Create_Headers_is_called)
            {
                // (_BYTE *a1, int a2, AES_CONTEXT *a3)
                this.pAesData = args[0];
                this.pBody = args[1];
                this.pBuff = args[2];
                this.nBuff = args[3].toInt32();
                let ctx_addr:NativePointer = this.pAesData.add(0x174).readPointer();
                LogAES_DATA(func_name, 'input', this.pAesData);
                LogAES_KEY(func_name, 'input', ctx_addr);
                Logger.DUMP(func_name, 'Input pBody len=' + this.nBuff, dumpHex(this.pBody, this.nBuff) );
                Logger.DUMP(func_name, 'Input pBuff len=' + this.nBuff, dumpHex(this.pBuff, this.nBuff) );
            }
        }, 
        onLeave: function(retval) {
            if (Maybe_Create_Headers_is_called)
            {
                let ctx_addr:NativePointer = this.pAesData.add(0x174).readPointer();
                Logger.DEBUG(func_name, 'Output ret =' + retval);
                LogAES_DATA(func_name, 'Output', this.pAesData);
                LogAES_KEY(func_name, 'Output', ctx_addr);
                Logger.DUMP(func_name, 'Output pBody len=' + this.nBuff, dumpHex(this.pBody, this.nBuff) );
                Logger.DUMP(func_name, 'Output pBuff len=' + this.nBuff, dumpHex(this.pBuff, this.nBuff) );
            }          
        }
    })        
}

function hook_aes_fnhash(base_addr: NativePointer): void 
{
    // .text:A1065277 ; signed int __cdecl aes_do_body(AesCustomData *a1, _BYTE *strCompressedBody, _BYTE *a3, int a4)
    let addr = null;
    let i ;
    let loaded_libc = 0 ;
    let func_name = 'aes_fnhash';
    let offset = 0x02432026;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            if (Maybe_Create_Headers_is_called)
            {
                this.p1 = args[0];
                this.p2 = args[1];
                this.pCtx = args[2];

                Logger.DUMP(func_name, 'Input p1', dumpHex(this.p1, 288) );
                Logger.DUMP(func_name, 'Input p2' , dumpHex(this.p2, 288) );
                Logger.DUMP(func_name, 'Input pCtx', dumpHex(this.pCtx, len_aes_key) );
            }
        }, 
        onLeave: function(retval) {
            if (Maybe_Create_Headers_is_called)
            {
                Logger.DEBUG(func_name, 'Output ret =' + retval);
                Logger.DUMP(func_name, 'Output p1', dumpHex(this.p1, 288) );
                Logger.DUMP(func_name, 'Output p2' , dumpHex(this.p2, 288) );
                Logger.DUMP(func_name, 'Output pCtx', dumpHex(this.pCtx, len_aes_key) );
            }          
        }
    })        
}
function dump_AesTable(base_addr: NativePointer): void 
{
    return ;
    // let addr = null;
    // let i ;
    // let loaded_libc = 0 ;
    // let func_name = 'aes_set_table';
    // let offset;

    // func_name = 'aes_Table'
    // offset = 0x02A0A4F8;
    // Logger.DUMP(func_name, 'T1(tb1=T1+3)', dumpHex(base_addr.add(offset), 1030));
    // offset = 0x02A0A8F8;
    // Logger.DUMP(func_name, 'T2(tb2=T2+3)', dumpHex(base_addr.add(offset), 1030));
    // offset = 0x02A0ACF8;
    // Logger.DUMP(func_name, 'T3(tb3=T3+1)', dumpHex(base_addr.add(offset), 1030));
    // offset = 0x02A0B0F8;
    // Logger.DUMP(func_name, 'T4', dumpHex(base_addr.add(offset), 1030));
}
function hook_aes_set_data(base_addr: NativePointer): void 
{
    // .text:02424863 ; unsigned int __cdecl aes_set_data(AesCustomData *s, AES_CONTEXT *a2, int fnHash)
    let addr = null;
    let i ;
    let loaded_libc = 0 ;
    let func_name = 'aes_set_data';
    let offset = 0x2424863;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            if (Maybe_Create_Headers_is_called)
            {
                this.pAesData = args[0];
                this.pCtx = args[1];

                dump_AesTable(base_addr);
                Logger.DUMP(func_name, 'Input pCustom', dumpHex(this.pAesData, len_aes_data) );
                Logger.DUMP(func_name, 'Input pCtx', dumpHex(this.pCtx, len_aes_key) );
            }
        }, 
        onLeave: function(retval) {
            if (Maybe_Create_Headers_is_called)
            {
                dump_AesTable(base_addr);
                Logger.DUMP(func_name, 'Output pCustom', dumpHex(this.pAesData, len_aes_data) );
                Logger.DUMP(func_name, 'Output pCtx', dumpHex(this.pCtx, len_aes_key) );
            }          
        }
    })        
}

function hook_aes_sub_hash2(base_addr: NativePointer): void 
{
    // .text:02424863 ; unsigned int __cdecl aes_set_data(AesCustomData *s, AES_CONTEXT *a2, int fnHash)
    let addr = null;
    let i ;
    let loaded_libc = 0 ;
    let func_name = 'aes_sub_hash2';
    let offset = 0x024250A3;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            //if (Maybe_Create_Headers_is_called)
            {
                Logger.DEBUG(func_name, 'params', {p0:args[0], p1:args[1], p2:args[2], p3:args[3]});
                if ( 'edx' in this.context )
                { 
                    this.pAesData1 = this.context.edx ; // param1
                    this.pAesData2 = this.context.ecx ; // param2
                    this.pBuff = args[0]; //this.context.ebp.add(0x08).readPointer(); // param3
                    this.nBuff = args[1].toUInt32(); //this.context.ebp.add(0x0C).readPointer().readU32(); // param4
                    
                    if ( this.nBuff > 0x500 ) 
                    {
                        Logger.DEBUG(func_name, 'buffer size(' + this.nBuff + ') is larger than 0x10000');
                        this.nBuff = 0x20;
                    }
                    Logger.DUMP(func_name, 'Input pCustom1', dumpHex(this.pAesData1, len_aes_data) );
                    Logger.DUMP(func_name, 'Input pCustom2', dumpHex(this.pAesData2, len_aes_data) );
                    Logger.DUMP(func_name, 'Input EBP' , dumpHex(this.context.ebp, 0x10) );
                    Logger.DUMP(func_name, 'Input EBP+0x08' , dumpHex(this.context.ebp.add(0x08).readPointer(), 0x10) );
                    Logger.DUMP(func_name, 'Input EBP+0x0C' , dumpHex(this.context.ebp.add(0x0C).readPointer(), 0x10) );
                    Logger.DUMP(func_name, 'Input pBuff = ' + this.nBuff, dumpHex(this.pBuff, this.nBuff) );
                }
            }
        }, 
        onLeave: function(retval) {
            //if (Maybe_Create_Headers_is_called)
            if ( 'pBuff' in this)
            {
                Logger.DEBUG(func_name, 'Output ret = ' + retval );
                Logger.DUMP(func_name, 'Output pCustom1', dumpHex(this.pAesData1, len_aes_data ) );
                Logger.DUMP(func_name, 'Output pCustom2', dumpHex(this.pAesData2, len_aes_data ) );
                Logger.DUMP(func_name, 'Output pBuff = ' + this.nBuff, dumpHex(this.pBuff, this.nBuff) );
            }          
        }
    }) 
}
function hook_aes_sub_hash1(base_addr: NativePointer): void 
{
    // .text:02424863 ; unsigned int __cdecl aes_set_data(AesCustomData *s, AES_CONTEXT *a2, int fnHash)
    let i ;
    let func_name = 'aes_sub_hash1';
    let offset = 0x02424E15;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            if (Maybe_Create_Headers_is_called && 'ecx' in this.context)
            {
                this.pAesData1 = this.context.ecx ; // param1
                this.pAesData2 = this.context.edx ; // param2
                
                Logger.DEBUG(func_name, 'param ', this.context);
                Logger.DUMP(func_name, 'Input pCustom1 p1=' + this.pAesData1, dumpHex(this.pAesData1, len_aes_data) );
                Logger.DUMP(func_name, 'Input pCustom2 p2=' + this.pAesData2, dumpHex(this.pAesData2, len_aes_data) );
            }
        }, 
        onLeave: function(retval) {
            if (Maybe_Create_Headers_is_called)
            {
                Logger.DEBUG(func_name, 'Output ret = ' + retval );
                Logger.DUMP(func_name, 'Output pCustom1 p1=' + this.pAesData1, dumpHex(this.pAesData1, len_aes_data ) );
                Logger.DUMP(func_name, 'Output pCustom2 p2=' + this.pAesData2, dumpHex(this.pAesData2, len_aes_data ) );
            }
        }
    }) 
}

function hook_xmm(base_addr: NativePointer): void
{
    // signed int __cdecl aes_xmm(__m128i *a1, int a2, unsigned int a3)
    let addr = null;
    let i ;
    let loaded_libc = 0 ;
    let func_name = 'aes_xmm';
    let offset = 0x02425EEF;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            if (Maybe_Create_Headers_is_called)
            {
                // (_BYTE *a1, int a2, AES_CONTEXT *a3)
                this.pData = args[0];
                this.pBuff = args[1];
                this.nBuff = args[2].toUInt32();

                LogAES_DATA(func_name, 'input', this.pData);
                Logger.DUMP(func_name, 'Input pBuff len=' + this.nBuff, dumpHex(this.pBuff, this.nBuff) );
            }
        }, 
        onLeave: function(retval) {
            if (Maybe_Create_Headers_is_called)
            {
                Logger.DEBUG(func_name, 'Output ret =' + retval);
                LogAES_DATA(func_name, 'Output', this.pData);
                Logger.DUMP(func_name, 'Output pBuff len=' + this.nBuff, dumpHex(this.pBuff, this.nBuff) );
            }          
        }
    })        
}
function dump_myString(base_addr: NativePointer, func_name:string, inout_title:string ): void 
{
    let b1 = base_addr.readU8();
    let capa = 0;
    let len = 0 ;
    let addr: NativePointer ;
    // base addr :  0xA46E8318
    // A46E8310  F8 85 3C 8F 40 86 3C 8F  41 01 00 00 0B 01 00 00  ..<.@.<.A.......
    // A46E8320  80 DA 84 94 F0 01 52 99  45 50 C5 A8 0A 8A CF A1  .ڄ .....EPŨ ..ϡ 
    // A46E8330  28 00 00 00 00 85 6E A4  E8 84 6E A4 18 85 6E A4  (.....n.......n.
    // A46E8340  00 85 6E A4 F8 55 82 A2  68 85 6E A4 31 1E B9 9F  ..n..U..h.n.1...
    // A46E8350  C0 84 6E A4 30 85 6E A4  18 85 6E A4 78 83 6E A4  ..n.0.n...n.x.n.
    // A46E8360  15 00 00 00 F0 00 00 00  2C 01 00 00 C8 98 49 99  ........,...Ș I.
    // A46E8370  84 C8 79 BD 40 00 D4 C7  31 00 00 00 23 00 00 00  ....@...1...#...
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

    Logger.DUMP(func_name, 'string dump', dumpHex(base_addr, 0x10));
    Logger.DEBUG(func_name, 'len = ' + len + ' / capa = ' + capa );
    Logger.DUMP(func_name, inout_title + ' len=' + len, dumpHex(addr, len));
}

function hook_compress_body_1D6E942(base_addr: NativePointer): void
{
    // int __cdecl sub_1D6E942(int a1, unsigned int a2, _DWORD *a3)
    let addr = null;
    let i ;
    let loaded_libc = 0 ;
    let func_name = 'zip_compress';
    let offset = 0x01D6E942;
    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.pBuff = args[0];
            this.nBuff = args[1].toUInt32();
            this.OutObject = args[2];

            Logger.DUMP(func_name, 'Input pBuff len=' + this.nBuff, dumpHex(this.pBuff, this.nBuff) );
            
            let trace = Thread.backtrace(this.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress) ;
            Logger.TRACE( func_name, 'call stack', trace);                    
        }, 
        onLeave: function(retval) {
            let length = 0;
            let compressed_body_addr = this.OutObject.readPointer();
            let compressed_1 = this.OutObject.add(0x04).readU32();
            let compressed_2 = this.OutObject.add(0x08).readU32();

            Logger.DEBUG(func_name, 'Output ret =' + retval);
        }
    })        
}
function hook_compress_body_1D6EBE3(base_addr: NativePointer): void
{
    // int __cdecl sub_1D6EBE3(int a1, signed int a2, int *a3, signed int a4)
    let addr = null;
    let i ;
    let loaded_libc = 0 ;
    let func_name = 'zip_1D6EBE3';
    let offset = 0x01D6EBE3;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p1 = args[0];
            this.p2 = args[1];
            this.p3 = args[2];
            this.p4 = args[3];
            Logger.DEBUG(func_name, 'zip', {p1: this.p1, p2: this.p2, p3: this.p3, p4: this.p4});
        }, 
        onLeave: function(retval) {
            Logger.DEBUG(func_name, 'Output ret =' + retval);
            Logger.DEBUG(func_name, 'zip', {p1: this.p1, p2: this.p2, p3: this.p3, p4: this.p4});
        }
    })        
}
function hook_compress_body_01D6EF14(base_addr: NativePointer): void
{
    // char __cdecl sub_1D6EF14(int a1, unsigned int a2, int *a3)
    let addr = null;
    let i ;
    let loaded_libc = 0 ;
    let func_name = 'zip_uncompress';
    let offset = 0x01D6EF14;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p1 = args[0];
            this.p2 = args[1].toUInt32();
            this.p3 = args[2];
            Logger.DEBUG(func_name, 'zip', {p1: this.p1, p2: this.p2, p3: this.p3});
        }, 
        onLeave: function(retval) {
            let addr = this.p3.readPointer();
            let len_decompress = this.p3.add(4).readU32();
            Logger.DEBUG(func_name, 'Output ret =' + retval);
            //Logger.DUMP(func_name, 'out p1', dumpHex(this.p1, this.p2));
            Logger.DUMP(func_name, 'out p3', dumpHex(addr, len_decompress));
        }
    })        
}
function hook_compress_body_1F04C36(base_addr: NativePointer): void
{
    // unsigned int __cdecl sub_1F04C36(int a1, char a2, char a3, int a4)
    let addr = null;
    let i ;
    let loaded_libc = 0 ;
    let func_name = 'zip_1F04C36';
    let offset = 0x1F04C36;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p1 = args[0];
            this.p2 = args[1];
            this.p3 = args[2];
            this.p4 = args[3];
            Logger.DEBUG(func_name, 'zip', {p1: this.p1, p2: this.p2, p3: this.p3, p4: this.p4});
        }, 
        onLeave: function(retval) {
            Logger.DEBUG(func_name, 'Output ret =' + retval);
            Logger.DEBUG(func_name, 'zip', {p1: this.p1, p2: this.p2, p3: this.p3, p4: this.p4});
        }
    })        
}
function hook_compress_body_1F05C5E(base_addr: NativePointer): void
{
    // unsigned int __cdecl sub_1F05C5E(int a1)
    let addr = null;
    let i ;
    let loaded_libc = 0 ;
    let func_name = 'zip_1F05C5E';
    let offset = 0x1F05C5E;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p1 = args[0];
            Logger.DEBUG(func_name, 'zip', {p1: this.p1});
        }, 
        onLeave: function(retval) {
            Logger.DEBUG(func_name, 'Output ret =' + retval);
            Logger.DEBUG(func_name, 'zip', {p1: this.p1});
        }
    })        
}
function hook_compress_body_23B2FEC(base_addr: NativePointer): void
{
    // int __cdecl sub_23B2FEC(char *a1, int a2, int a3, int a4, int a5, int (__cdecl *a6)(int *, size_t), int a7)
    let addr = null;
    let i ;
    let loaded_libc = 0 ;
    let func_name = 'zip_23B2FEC';
    let offset = 0x23B2FEC;
    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p1 = args[0];
            this.p2 = args[1];
            this.p3 = args[2];
            this.p4 = args[3];
            this.p5 = args[4];
            this.p6 = args[5];
            this.p7 = args[6];
            Logger.DEBUG(func_name, 'zip', {p1: this.p1, p2: this.p2, p3: this.p3, p4: this.p4, p5: this.p5, p6: this.p6, p7: this.p7});
        }, 
        onLeave: function(retval) {
            Logger.DEBUG(func_name, 'Output ret =' + retval);
            Logger.DEBUG(func_name, 'zip', {p1: this.p1, p2: this.p2, p3: this.p3, p4: this.p4, p5: this.p5, p6: this.p6, p7: this.p7});
        }
    })        
}
function hook_compress_body_23C614B(base_addr: NativePointer): void
{
    // signed int __cdecl sub_23C614B(int a1, _DWORD *a2, _DWORD *a3, int a4, int a5)
    let addr = null;
    let i ;
    let loaded_libc = 0 ;
    let func_name = 'zip_23C614B';
    let offset = 0x23C614B;
    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            // this.p1 = args[0];
            // this.p2 = args[1];
            // this.p3 = args[2];
            // this.p4 = args[2];
            // this.p5 = args[2];
            Logger.DEBUG(func_name, 'zip', {p1: this.p1, p2: this.p2, p3: this.p3, p4: this.p4, p5: this.p5});
            // Logger.DUMP(func_name, 'in - p1', dumpHex(this.p1, 0x20));
        }, 
        onLeave: function(retval) {
            Logger.DEBUG(func_name, 'Output ret =' + retval);
            // Logger.DUMP(func_name, 'out - p1', dumpHex(this.p1, 0x20));
        }
    })        
}
function hook_compress_body_23C864A(base_addr: NativePointer): void
{
    // int __cdecl sub_23C864A(int a1, int a2, int a3, int a4, int a5, int a6, int a7, char *s, int a9, int a10, int a11, int a12, int a13, int a14, int a15, int a16, int a17, int a18, int a19)
    let addr = null;
    let i ;
    let loaded_libc = 0 ;
    let func_name = 'zip_23C864A';
    let offset = 0x23C864A;
    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p1 = args[0];
            this.p2 = args[1];
            this.p3 = args[2];
            this.p4 = args[3];
            this.p5 = args[4];
            this.p6 = args[5];
            this.p7 = args[6];
            this.p8 = args[7];
            this.p9 = args[8];
            this.p10 = args[9];
            this.p11 = args[10];
            this.p12 = args[11];
            this.p13 = args[12];
            this.p14 = args[13];
            this.p15 = args[14];
            this.p16 = args[15];
            this.p17 = args[16];
            this.p18 = args[17];
            this.p19 = args[18];
            Logger.DEBUG(func_name, 'zip', {
                p1: this.p1, p2: this.p2, p3: this.p3, p4: this.p4, p5: this.p5,
                p6: this.p6, p7: this.p7, p8: this.p8, p9: this.p9, p10: this.p10,
                p11: this.p11, p12: this.p12, p13: this.p13, p14: this.p14, p15: this.p15,
                p16: this.p16, p17: this.p17, p18: this.p18, p19: this.p19
            });
        }, 
        onLeave: function(retval) {
            Logger.DEBUG(func_name, 'zip', {
                p1: this.p1, p2: this.p2, p3: this.p3, p4: this.p4, p5: this.p5,
                p6: this.p6, p7: this.p7, p8: this.p8, p9: this.p9, p10: this.p10,
                p11: this.p11, p12: this.p12, p13: this.p13, p14: this.p14, p15: this.p15,
                p16: this.p16, p17: this.p17, p18: this.p18, p19: this.p19
            });
        }
    })        
}
function hook_compress_body(base_addr: NativePointer): void
{
    hook_compress_body_1D6E942(base_addr); // sub_23BE5A8 (compress)
    hook_compress_body_1D6EBE3(base_addr); // sub_23BE5A8 (compress)
    hook_compress_body_01D6EF14(base_addr);// sub_23C0FEF (decompress)
    hook_compress_body_1F04C36(base_addr); // sub_23BE5A8 (compress)
    hook_compress_body_1F05C5E(base_addr); // sub_23C0FEF (decompress)
    hook_compress_body_23B2FEC(base_addr); // sub_23C10D8 (compress)
    //hook_compress_body_23C614B(base_addr); // sub_23C0FEF (decompress)
    hook_compress_body_23C864A(base_addr); // sub_23BE5A8 (compress)
}
function hook_jni_nativeHttpRequestOnHeaders(base_addr: NativePointer): void 
{
    // public static native boolean nativeHttpRequestOnHeaders(long j, int i, String[] strArr);
    let i ;
    let func_name = 'JNI_ReqHeader';
    let offset = 0x01F88C0E;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.JNIEnv = args[0];
            this.JObject = args[1];
            this.j = args[2];
            this.i = args[3];
            this.strArr = args[4];

            Logger.DEBUG(func_name, 'onEnter', {env:this.JNIEnv, obj:this.JObject, j:this.j, i:this.i, strArr:this.strArr});
        }, 
        onLeave: function(retval) {
        }
    })    

}
function hook_jni_nativeHttpRequestOnAppendContent(base_addr: NativePointer): void 
{
    // public static native void nativeHttpRequestOnAppendContent(long j, byte[] bArr, int i);
    let i ;
    let func_name = 'JNI_ReqContent';
    let offset = 0x01F8900C;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.JNIEnv = args[0];
            this.JObject = args[1];
            this.j = args[2];
            this.bArr = args[3];
            this.i = args[4];

            Logger.DEBUG(func_name, 'onEnter', {env:this.JNIEnv, obj:this.JObject, j:this.j, bArr:this.bArr, i:this.i});
        }, 
        onLeave: function(retval) {
        }
    })    

}
function hook_jni_nativeHttpRequestFinished(base_addr: NativePointer): void 
{
    // public static native void nativeHttpRequestFinished(long j, int i, String str);
    let i ;
    let func_name = 'JNI_ReqFinish';
    let offset = 0x01F8934A;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.JNIEnv = args[0];
            this.JObject = args[1];
            this.j = args[2];
            this.i = args[3];
            this.str = args[4];

            Logger.DEBUG(func_name, 'onEnter', {env:this.JNIEnv, obj:this.JObject, j:this.j, i:this.i, str:this.str});
        }, 
        onLeave: function(retval) {
        }
    })    
}
function sub_73BD16(base_addr:NativePointer): void 
{
    // sub_73BD16
    let i ;
    let func_name = 'sub_73BD16';
    let offset = 0x73BD16;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p1 = args[0];
            this.p2 = args[1];
            this.p3 = args[2];
            Logger.DEBUG(func_name, 'onEnter p1', dumpHex(this.p1, 0x20));
            Logger.DEBUG(func_name, 'onEnter p2', dumpHex(this.p2, 0x20));
            Logger.DEBUG(func_name, 'onEnter p2', dumpHex(this.p3, 0x20));
        }, 
        onLeave: function(retval) {
            Logger.DEBUG(func_name, 'onLeave p1', dumpHex(this.p1, 0x20));
            Logger.DEBUG(func_name, 'onLeave p2', dumpHex(this.p2, 0x20));
            Logger.DEBUG(func_name, 'onLeave p2', dumpHex(this.p3, 0x20));
        }
    })      
}
function sub_1413F12(base_addr:NativePointer): void 
{
    // sub_73BD16
    let i ;
    let func_name = 'sub_1413F12';
    let offset = 0x1413F12;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p1 = args[0];
            this.p2 = args[1];
            Logger.DEBUG(func_name, 'onEnter p1', dumpHex(this.p1, 0x20));
            Logger.DEBUG(func_name, 'onEnter p2', dumpHex(this.p2, 0x20));
        }, 
        onLeave: function(retval) {
            Logger.DEBUG(func_name, 'onLeave p1', dumpHex(this.p1, 0x20));
            Logger.DEBUG(func_name, 'onLeave p2', dumpHex(this.p2, 0x20));
        }
    })      
}
function sub_20566D7(base_addr:NativePointer): void 
{   
    let i ;
    let func_name = 'sub_20566D7';
    let offset = 0x1413F12;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p1 = args[0];
            this.p2 = args[1];
            this.p3 = args[2];
            Logger.DEBUG(func_name, 'onEnter p1', dumpHex(this.p1, 0x20));
            Logger.DEBUG(func_name, 'onEnter p2', dumpHex(this.p2, 0x20));
            Logger.DEBUG(func_name, 'onEnter p2', dumpHex(this.p3, 0x20));
        }, 
        onLeave: function(retval) {
            Logger.DEBUG(func_name, 'onLeave p1', dumpHex(this.p1, 0x20));
            Logger.DEBUG(func_name, 'onLeave p2', dumpHex(this.p2, 0x20));
            Logger.DEBUG(func_name, 'onLeave p2', dumpHex(this.p3, 0x20));
        }
    })  

    func_name = 'sub_49A346';
    offset = 0x49A346;
    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p1 = args[0];
            this.p2 = args[1];
            this.p3 = args[2];
            for ( let i = 0 ; i < 5 ; i ++ )
                Logger.DUMP(func_name, 'onEnter p' + i , args[ i  ]);
        }, 
        onLeave: function(retval) {
            // Logger.DEBUG(func_name, 'onLeave p1', dumpHex(this.p1, 0x20));
            // Logger.DEBUG(func_name, 'onLeave p2', dumpHex(this.p2, 0x20));
            // Logger.DEBUG(func_name, 'onLeave p2', dumpHex(this.p3, 0x20));
        }
    })  

}

function EncodeJsonBody(base_addr:NativePointer): void 
{
// .text:01413F12 Maybe_generate_body proc near           ; CODE XREF: sub_44AECC+2CE8↑p
// .text:01413F12                                         ; sub_4F96FC+232↑p ...
    let i ;
    let func_name = 'EncodeJsonBody';
    let offset = 0x01413F12;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p1 = args[0];
            this.p2 = args[1];
            //Logger.DUMP(func_name, 'onEnter p1', dumpHex(this.p1, 0x20));
            Logger.DUMP(func_name, 'onEnter p2', dumpHex(this.p2, 0x20));
            Logger.DUMP(func_name, '*p2', dumpHex(this.p2.readPointer(), 0x20));
        }, 
        onLeave: function(retval) {
            Logger.DEBUG(func_name, 'Output ret =' + retval);

            //Logger.DUMP(func_name, 'onLeave p1', dumpHex(this.p1, 0x20));
            Logger.DUMP(func_name, 'onLeave p2', dumpHex(this.p2, 0x20));
            Logger.DUMP(func_name, '*p2', dumpHex(this.p2.readPointer(), 0x20));
        }
    })  

}
function sub_1117870(base_addr:NativePointer): void 
{
    let i ;
    let func_name = 'sub_1117870';
    let offset = 0x1117870;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p0 = args[0];
            this.p1 = args[1];
            this.p2 = args[2];
            Logger.DEBUG(func_name, 'onEnter', {p0:args[0], p1:args[1], p2:args[2]});
            Logger.DUMP(func_name, 'onEnter', dumpHex(this.p0, 0x30));
            Logger.DUMP(func_name, 'onEnter', dumpHex(this.p0.readPointer(), 0x30));
        }, 
        onLeave: function(retval) {
            Logger.DEBUG(func_name, 'onLeave ret =' + retval);
            Logger.DUMP(func_name, 'onLeave', dumpHex(this.p0, 0x30));
            Logger.DUMP(func_name, 'onLeave', dumpHex(this.p0.readPointer(), 0x30));
        }
    })  
}
function sub_1A59DB6(base_addr:NativePointer): void 
{
    let i ;
    let func_name = 'sub_1A59DB6';
    let offset = 0x1A59DB6;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p0 = args[0];
            this.p1 = args[1];
            Logger.DEBUG(func_name, 'onEnter', {p0:args[0], p1:args[1]});
            Logger.DUMP(func_name, 'onEnter p0', dumpHex(this.p0, 0x60));
            Logger.DUMP(func_name, 'onEnter p1', dumpHex(this.p1, 0x60));
        }, 
        onLeave: function(retval) {
            Logger.DEBUG(func_name, 'onLeave ret =' + retval);
            Logger.DUMP(func_name, 'onLeave p0', dumpHex(this.p0, 0x60));
            Logger.DUMP(func_name, 'onLeave p1', dumpHex(this.p1, 0x60));
        }
    })  
}
function sub_1A5BB9E(base_addr:NativePointer): void 
{
    let i ;
    let func_name = 'sub_1A5BB9E';
    let offset = 0x1A5BB9E;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p0 = args[0];
            this.p1 = args[1];
            Logger.DEBUG(func_name, 'onEnter', {p0:args[0], p1:args[1]});
            Logger.DUMP(func_name, 'onEnter p0', dumpHex(this.p0, 0x60));
            Logger.DUMP(func_name, 'onEnter p1', dumpHex(this.p1, 0x60));
        }, 
        onLeave: function(retval) {
            Logger.DEBUG(func_name, 'onLeave ret =' + retval);
            Logger.DUMP(func_name, 'onLeave p0', dumpHex(this.p0, 0x60));
            Logger.DUMP(func_name, 'onLeave p1', dumpHex(this.p1, 0x60));
        }
    })  
}

function readXml_decode_xml(base_addr:NativePointer): void 
{
    let i ;
    let func_name = 'decodeXml';
    let offset = 0x01109CF7;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p0 = args[0];
            this.p1 = args[1].toUInt32();
            this.p2 = args[2];
            Logger.DEBUG(func_name, 'onEnter', {p0:args[0], p1:args[1], p2:args[2]});
            Logger.DUMP(func_name, 'onEnter FileData', dumpHex(this.p0.readPointer(), this.p1));
            //Logger.DUMP(func_name, 'onEnter p2', dumpHex(this.p2.readPointer(), 0x20));                 
        }, 
        onLeave: function(retval) {
            Logger.DEBUG(func_name, 'onLeave ret =' + retval);
            Logger.DUMP(func_name, 'onLeave FileData', dumpHex(this.p0.readPointer(), this.p1));
            //Logger.DUMP(func_name, 'onLeave p2', dumpHex(this.p2.readPointer(), 0x20));
        }
    })  
}
function generateHashTable_0x2d7(base_addr:NativePointer): void 
{
    let i ;
    let func_name = 'HashTbl0x2d7';
    let offset = 0x01109670;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p0 = args[0].readPointer();
            this.p1 = args[1];
            this.p2 = args[2];
            Logger.DEBUG(func_name, 'onEnter', {p0:args[0], p1:args[1], p2:args[2]});
        }, 
        onLeave: function(retval) {
            Logger.DEBUG(func_name, 'onLeave ret =' + retval);
        }
    })  
}
var hexArr: {[k: string]: any} = {};
function hook_decode_keyword(base_addr:NativePointer): void 
{
    // .text:020566D7 decode_keyword  proc near               ; CODE XREF: sub_2A6DF6+8C0↑p
    // .text:020566D7                                         ; sub_2A6DF6+8FB↑p ...    
    let i ;
    let func_name = 'decode_keyword';
    let offset = 0x020566D7;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p0 = args[0];
            this.p1 = args[1];
            this.p2 = args[2].toUInt32();
            let addr = '' + this.p1 + '';
            if ( addr in hexArr ){}
            else 
            {
                Logger.DEBUG(func_name, 'onEnter', {p0:this.p0, p1:this.p1, p2:this.p2});
            }
        }, 
        onLeave: function(retval) {
            let addr = '' + this.p1 + '';
            if ( addr in hexArr ){}
            else 
            {
                hexArr[addr] = 1;
                Logger.DEBUG(func_name, 'onLeave ret =' + retval);
                Logger.DUMP(func_name, 'text len=' + (this.p2), dumpMyString(this.p0));
                Logger.DUMP(func_name, 'hex len='+ (this.p2+1), dumpHex(this.p1, this.p2+1));
            }            
        }
    })  
}

function hook_readXml_Trace5_Package(base_addr:NativePointer): void 
{
    // .text:0111C29D readXml_Trace5_Package proc near        ; CODE XREF: sub_F8212A+5B↑p
    let i ;
    let func_name = 'readxml5';
    let offset = 0x0111C29D;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p0 = args[0];
            this.p1 = args[1];
            Logger.DEBUG(func_name, 'onEnter', {p0:this.p0, p1:this.p1});
            Logger.DUMP(func_name, 'onEnter p0', dumpMyString(this.p0));
        }, 
        onLeave: function(retval) {
            Logger.DEBUG(func_name, 'onLeave ret =' + retval);
            //Logger.DUMP(func_name, 'onLeave p0', dumpMyString(this.p0));
            let addr = this.p1.readPointer();
            let real_size = this.p1.add(4).readU32();
            let size = real_size > 0x30 ? 0x30 : real_size;
            Logger.DUMP(func_name, 'onLeave p1 len=' + real_size, dumpHex(addr, size));
        }
    })  
}
function hook_readXml_Trace4_Package(base_addr:NativePointer): void 
{
    // .text:002D17BB ; int *__userpurge readXml_Trace4_Package@<eax>(int *pOut, MyString *pfilename, int a3)
    let i ;
    let func_name = 'readxml4';
    let offset = 0x002D17BB;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p0 = args[0];
            this.p1 = args[1];
            this.p2 = args[2];
            Logger.DEBUG(func_name, 'onEnter', {p0:this.p0, p1:this.p1, p2:this.p2});
            Logger.DUMP(func_name, 'onEnter p0', dumpHex(this.p0, 0x20));
            Logger.DUMP(func_name, 'onEnter p1', dumpMyString(this.p1));
        }, 
        onLeave: function(retval) {
            Logger.DEBUG(func_name, 'onLeave ret =' + retval);
            Logger.DUMP(func_name, 'onLeave p0', dumpHex(this.p0, 0x20));
            let addr = this.p0.readPointer();
            let real_size = this.p0.add(4).readU32();
            let size = real_size > 0x30 ? 0x30 : real_size;
            Logger.DUMP(func_name, 'onLeave p0 ptr len=' + real_size, dumpHex(addr, size));            
            for ( let i = 0 ; i < real_size ; i += 4 )
            {
                let addr2 = addr.add(i).readPointer()
                Logger.DUMP(func_name, 'onLeave p0 ptr ptr', dumpHex(addr2, 0x20));            
            }
        }
    })  
}
function hook_readXml_Trace8_GlobalVars(base_addr:NativePointer): void 
{
    // .text:01E37A3D readXml_Trace8_GlobalVars proc near     ; CODE XREF: readXml_Trace9_GlobalVars+584↑p
    let i ;
    let func_name = 'global8';
    let offset = 0x01E37A3D;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p0 = args[0];
            this.p1 = args[1];
            this.p2 = args[2];
            Logger.DEBUG(func_name, 'onEnter', {p0:this.p0, p1:this.p1, p2:this.p2});
            Logger.DUMP(func_name, 'onEnter p0', dumpMyString(this.p0));
            Logger.DUMP(func_name, 'onEnter p1', dumpMyString(this.p1));
            Logger.DUMP(func_name, 'onEnter p2', dumpHex(this.p2.readPointer().readPointer(), 0x20));
        }, 
        onLeave: function(retval) {
            Logger.DEBUG(func_name, 'onLeave ret =' + retval);
            Logger.DUMP(func_name, 'onLeave p0', dumpHex(this.p0, 0x20));
            Logger.DUMP(func_name, 'onLeave p1', dumpMyString(this.p1));
            Logger.DUMP(func_name, 'onLeave p2', dumpHex(this.p2.readPointer().readPointer(), 0x20));

        }
    })  
}

function hook_readXml_Trace7_GlobalVars(base_addr:NativePointer): void 
{
    // .text:01E37AC6 readXml_Trace7_GlobalVars proc near     ; CODE XREF: readXml_Trace8_GlobalVars+47↑p
    let i ;
    let func_name = 'global7';
    let offset = 0x01E37AC6;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p0 = args[0];
            this.p1 = args[1];
            this.p2 = args[2];
            Logger.DEBUG(func_name, 'onEnter', {p0:this.p0, p1:this.p1, p2:this.p2});
            Logger.DUMP(func_name, 'onEnter p0', dumpMyString(this.p0));
            Logger.DUMP(func_name, 'onEnter p1', dumpMyString(this.p1));
            Logger.DUMP(func_name, 'onEnter p2', dumpHex(this.p2, 0x20));
        }, 
        onLeave: function(retval) {
            Logger.DEBUG(func_name, 'onLeave ret =' + retval);
            Logger.DUMP(func_name, 'onLeave p0', dumpHex(this.p0, 0x20));
            Logger.DUMP(func_name, 'onLeave p1', dumpMyString(this.p1));
            Logger.DUMP(func_name, 'onLeave p2', dumpHex(this.p2, 0x20));

        }
    })  
}

function hook_readXml_Trace6_GlobalVars(base_addr:NativePointer): void 
{
    // .text:02071CFC readXml_Trace6_GlobalVars proc near     ; CODE XREF: readXml_Trace7_GlobalVars+F2↑p
    let i ;
    let func_name = 'global6';
    let offset = 0x02071CFC;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p0 = args[0];
            Logger.DEBUG(func_name, 'onEnter', {p0:this.p0});
            //Logger.DUMP(func_name, 'onEnter p0', dumpHex(this.p0, 0x2880));
            Logger.DUMP(func_name, 'onEnter p0', dumpHex(this.p0, 0x20));

            Logger.DUMP(func_name, 'onEnter *(_DWORD *)a1 = &off_285C847;', dumpHex(this.p0.add(0).readPointer(), 0x20));
            Logger.DUMP(func_name, 'onEnter *((_DWORD *)a1 + 1)', dumpHex(this.p0.add(4).readPointer(), 0x20));
            Logger.DUMP(func_name, 'onEnter ', dumpHex(this.p0.add(8).readPointer(), 0x20));
            Logger.DUMP(func_name, 'onEnter ', dumpHex(this.p0.add(0).readPointer(), 0x20));
            
        }, 
        onLeave: function(retval) {
            Logger.DEBUG(func_name, 'onLeave ret =' + retval);
            // Logger.DUMP(func_name, 'onEnter p0', dumpHex(this.p0, 0x2880));
            Logger.DUMP(func_name, 'onEnter p0', dumpHex(this.p0, 0x20));
        }
    })  
}

function hook_zlib_compress_check_data(base_addr:NativePointer): void 
{
    // .text:00440A93 zlib_compress_check_data proc near      ; CODE XREF: sub_4405FC+27B↑p
    let i ;
    let func_name = 'zlib_data';
    let offset = 0x00440A93;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p0 = args[0];
            this.p1 = args[1];
            this.p2 = args[2];
            this.p3 = args[3];

            Logger.DEBUG(func_name, 'onEnter', {p0:this.p0, p1:this.p1, p2:this.p2, p3:this.p3});

            Logger.DUMP(func_name, 'onEnter p0', dumpMyString(this.p0));
            Logger.DUMP(func_name, 'onEnter p1', dumpHex(this.p1.readPointer(), 0x20));

            let len = this.p2.readU32();
            let addr1 = this.p2.add(4).readPointer();
            let addr2 = this.p2.add(8).readPointer();
            Logger.DUMP(func_name, 'onEnter p2', dumpHex(this.p2, 0x20));
            Logger.DUMP(func_name, 'onEnter p2-addr1 len='+len, dumpHex(addr1, len));
            Logger.DUMP(func_name, 'onEnter p2-addr2len='+len, dumpHex(addr2, len));
            Logger.DUMP(func_name, 'onEnter p3', dumpMyString(this.p3 ));
        }, 
        onLeave: function(retval) {
            Logger.DEBUG(func_name, 'onLeave ret =' + retval);
            Logger.DUMP(func_name, 'onLeave p0', dumpMyString(this.p0));
            Logger.DUMP(func_name, 'onLeave p1', dumpHex(this.p1.readPointer(), 0x20));
            let len = this.p2.readU32();
            let addr1 = this.p2.add(4).readPointer();
            let addr2 = this.p2.add(8).readPointer();
            Logger.DUMP(func_name, 'onEnter p2', dumpHex(this.p2, 0x20));
            Logger.DUMP(func_name, 'onEnter p2-addr1 len='+len, dumpHex(addr1, len));
            Logger.DUMP(func_name, 'onEnter p2-addr2len='+len, dumpHex(addr2, len));
            Logger.DUMP(func_name, 'onLeave p3', dumpMyString(this.p3 ));
        }
    })  
}

function hook_xml_xor(base_addr:NativePointer):void
{
    //.text:01F081F2 ; int __cdecl readXml_read(int, void *ptr, size_t n, int)    
    let i ;
    let func_name = 'xml_xor';
    let offset = 0x01F0474E;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p0 = args[0];
            this.p1 = args[1].toUInt32(); // flag
            this.p2 = args[2].toUInt32(); // offset
            this.p3 = args[3];
            this.p4 = args[4].toUInt32(); // length

            Logger.DEBUG(func_name, 'onEnter param', {p0:this.p0, p1:this.p1, p2:this.p2, p3:this.p3, p4:this.p4});
            Logger.DUMP(func_name, 'onEnter p0', dumpHex(this.p0, 0x30));
            Logger.DUMP(func_name, 'onEnter p3(xml)', dumpHex(this.p3, 0x30));
            Logger.DUMP(func_name, 'onEnter p0+4(key)', dumpHex(this.p0.add(4).readPointer(), 0x40));
        }, 
        onLeave: function(retval) {
            Logger.DEBUG(func_name, 'onLeave param', {p0:this.p0, p1:this.p1, p2:this.p2, p3:this.p3, p4:this.p4});
            Logger.DUMP(func_name, 'onLeave p0', dumpHex(this.p0, 0x30));
            Logger.DUMP(func_name, 'onLeave p3(xml)', dumpHex(this.p3, 0x30));
        }
    })  
}

function hook_decode_0x79(base_addr:NativePointer):void
{
    // .text:01109ACA xml_decode_0x79
    let i ;
    let func_name = 'decode_0x79';
    let offset = 0x01109ACA;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p0 = args[0];
            this.p1 = args[1];

            let p1_len=this.p1.readU32();
            // 00e0d591
            // fc080000
            // fc080000
            let p0_a = this.p0.add(4).readU32();
            let p0_b = this.p0.add(8).readU32();
            Logger.DEBUG(func_name, 'onEnter param', {p0:this.p0, p1:p1_len});
            Logger.DUMP(func_name, 'onEnter p0 a='+p0_a + ' / b='+p0_b, dumpHex(this.p0.readPointer(), p0_a));
        }, 
        onLeave: function(retval) {
            let p0_a = this.p0.add(4).readU32();
            let p0_b = this.p0.add(8).readU32();
            Logger.DUMP(func_name, 'onLeave p0 a='+p0_a + ' / b='+p0_b, dumpHex(this.p0.readPointer(), p0_a));
        }
    })  
}
function hook_fetch_city1(base_addr:NativePointer): void 
{
    let i ;
    let func_name = 'fetch_city1';
    let offset = 0x004B2F5C;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p0 = args[0];
            this.p1 = args[1];
            this.p2 = args[2];

            Logger.DEBUG(func_name, 'onEnter param', {p0:this.p0, p1:this.p1, p2:this.p2});
            Logger.DUMP(func_name, 'onEnter p0 ', dumpHex(this.p0, 0x20));
            Logger.DUMP(func_name, 'onEnter p1 ', dumpHex(this.p1, 0x20));
            Logger.DUMP(func_name, 'onEnter p2 ', dumpHex(this.p2, 0x20));

            let trace = Thread.backtrace(this.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress) ;
            Logger.TRACE( func_name, 'onEnter', trace);                      
        }, 
        onLeave: function(retval) {
            Logger.DUMP(func_name, 'onLeave p0 ', dumpHex(this.p0, 0x20));
            Logger.DUMP(func_name, 'onLeave p1 ', dumpHex(this.p1, 0x20));
            Logger.DUMP(func_name, 'onLeave p2 ', dumpHex(this.p2, 0x20));
        }
    })      
}
function hook_fetch_city2(base_addr:NativePointer): void
{
    let i ;
    let func_name = 'fetch_city2';
    let offset = 0x0049A346;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p0 = args[0];
            this.p1 = args[1];

            Logger.DEBUG(func_name, 'onEnter param', {p0:this.p0, p1:this.p1});
            Logger.DUMP(func_name, 'onEnter p0 ', dumpHex(this.p0, 0x20));
            Logger.DUMP(func_name, 'onEnter p1 ', dumpHex(this.p1, 0x20));

            let trace = Thread.backtrace(this.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress) ;
            Logger.TRACE( func_name, 'onEnter', trace);             
        }, 
        onLeave: function(retval) {
            Logger.DUMP(func_name, 'onLeave p0 ', dumpHex(this.p0, 0x20));
            Logger.DUMP(func_name, 'onLeave p1 ', dumpHex(this.p1, 0x20));
        }
    })          
}
function hook_libgame() : void 
{
    let func_name = 'libgame.so';
    let base_addr:NativePointer | null = Module.findBaseAddress('libgame.so');
    Logger.INFO(func_name, 'base address', {addr : base_addr});

    if ( !base_addr )
    {
        Logger.ERROR(func_name, 'Failed to find base address of libgame.so');
        return;
    }
    else
    {
        hook_proc_status(base_addr);
        hook_check_rooting(base_addr);
        hook_check_emulator(base_addr);
        // hook_sub_0x2D0052(base_addr);
        // hook_proc_maps(base_addr);
        // hook_sub_1F18268(base_addr);
        // hook_sub_816C84(base_addr);
        //hook_header_value(base_addr);
        //hook_decode_http_header_key(base_addr);
        //hook_sub_9F082662(base_addr);
        // hook_Maybe_Concat(base_addr);
        
        //////////////////////////////////////////////////////////////
        // When analysis Body
        hook_Maybe_Create_Headers(base_addr);
        hook_encode_string_aes(base_addr);
        hook_decode_string_aes(base_addr);
        hook_compress_body(base_addr);
        // When analysis Body
        //////////////////////////////////////////////////////////////
        
        // hook_aes_setup(base_addr);
        // hook_create_custom_aes_data(base_addr);
        // hook_aes_hash_with_random(base_addr);
        // //hook_aes_fnhash(base_addr);
        // hook_aes_set_data(base_addr);

        //hook_aes_do_body(base_addr);

        // hash_1
        // hash_2
        // hook_aes_sub_hash1(base_addr);
        // hook_aes_sub_hash2(base_addr);
        // hook_xmm(base_addr);
        

        // hook_jni_nativeHttpRequestOnHeaders(base_addr);
        // hook_jni_nativeHttpRequestOnAppendContent(base_addr);
        // hook_jni_nativeHttpRequestFinished(base_addr);

        // maybe.. decode httpResponse ?
        // sub_73BD16(base_addr);
        // sub_1413F12(base_addr);
        // sub_20566D7(base_addr);
        // sub_1117870(base_addr);
        // EncodeJsonBody(base_addr);
        // sub_1A59DB6(base_addr);
        // sub_1A5BB9E(base_addr);
        // readXml_decode_xml(base_addr);
        // generateHashTable_0x2d7(base_addr);
        //hook_decode_keyword(base_addr);
        
        // sniffing Http Request and Response Data
        // 
        // hook_readXml_Trace4_Package(base_addr);
        // hook_readXml_Trace5_Package(base_addr);

        // hook_readXml_Trace8_GlobalVars(base_addr);
        // hook_readXml_Trace7_GlobalVars(base_addr);
        // hook_readXml_Trace6_GlobalVars(base_addr);
        // hook_zlib_compress_check_data(base_addr);

        // hook_xml_fread(base_addr);
        // hook_xml_xor(base_addr);

        // hook_decode_0x79(base_addr);

        // hook_fetch_city2(base_addr);
        // hook_fetch_city1(base_addr);
    }
}

export default hook_libgame;