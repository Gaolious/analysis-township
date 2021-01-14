import Logger from "../logger";
import {start_hook_fread, end_hook_fread} from "./libc"

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

/**
 * Access to /proc/[pid]/status 
 *           /proc/self/status 
 *           /proc/../task/[pid]/status
 *           /proc/../task/self/status
 */
function hook_proc_status(base_addr: NativePointer): void
{
    let func_name = 'proc_status';
    //let offset = 0x20738D8 ;
    let offset = 0x21124CC;  // 7.9.5

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
    // let offset = 0x2074AF3 ;
    let offset = 0x21136E7; // 7.9.5

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
    // let offset = 0x2077719;
    let offset = 0x211630D;  // 7.9.5

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


var isStartHexTwiceFunction = false;
/**
 * <root>
 *      <global>
 *          <hex>32길이의 hex string</hex>   <----
 *          <hex2>32길이의 hex string</hex2> <----
 *      </global>
 * </root
 * @param base_addr base address of libgame.so
 */
function hook_global_hex_value(base_addr: NativePointer): void 
{
    let func_name = 'GlobalHex';
    let offset = 0x01966EAC;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p0 = args[0];
            this.p1 = args[1];
            this.p2 = args[2];
            this.p3 = args[3];
            if (isStartHexTwiceFunction)
            {
                Logger.DEBUG(func_name, 'onEnter', {p0:this.p0, p1:this.p1, p2:this.p2, p3:this.p3});
                Logger.DumpMyString(func_name, 'onEnter p0', this.p0);
                Logger.DUMP(func_name, 'onEnter p1', dumpHex(this.p1, 0x10));
                Logger.DumpMyString(func_name, 'onEnter p2', this.p2);
                Logger.DumpMyString(func_name, 'onEnter p3', this.p3);
                let trace = Thread.backtrace(this.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress) ;
                Logger.TRACE( func_name, 'call stack', trace);                    
            }
        }, 
        onLeave: function(retval) {
            if ( isStartHexTwiceFunction)
            {
                Logger.DEBUG(func_name, 'onLeave', {ret:retval});
                Logger.DUMP(func_name, 'onEnter p1', dumpHex(this.p1, 0x10));
                Logger.DumpMyString(func_name, 'onLeave p0', this.p0);
            }
        }
    })      
}

function hook_hex_hash(base_addr: NativePointer): void 
{
    let func_name = 'hexhash';
    let offset = 0x019AA6E2;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p0 = args[0];
            this.p1 = args[1];
            this.p2 = args[2];
            if (isStartHexTwiceFunction)
            {
                Logger.DEBUG(func_name, 'onEnter', {p0:this.p0, p1:this.p1, p2:this.p2});
                Logger.DumpMyString(func_name, 'onEnter p0', this.p0);
                Logger.DUMP(func_name, 'onEnter p1', dumpHex(this.p1, 0x10));
                Logger.DUMP(func_name, 'onEnter p2', dumpHex(this.p2, 0x10));
            }
        }, 
        onLeave: function(retval) {
            if ( isStartHexTwiceFunction)
            {
                Logger.DEBUG(func_name, 'onLeave', {ret:retval});
                Logger.DumpMyString(func_name, 'onLeave p0', this.p0);
            }
        }
    })      
}
function hook_global_hex2_value(base_addr: NativePointer): void 
{
    let func_name = 'HexTwice';
    let offset = 0x019AACDE;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p0 = args[0];
            this.p1 = args[1];
            this.p2 = args[2];
            Logger.DumpMyString(func_name, 'onEnter p1', this.p1);
            isStartHexTwiceFunction = true;
        }, 
        onLeave: function(retval) {
            isStartHexTwiceFunction = false;
        }
    })      
}


var enter_decode_45584C50 = false ;

function hook_xml_fread(base_addr: NativePointer): void 
{
    // .text:01FA6B92 ; size_t __cdecl xml_fread(XmlDecodeParentV4 *a1, void *ptr, size_t n, XmlStatus *a)
    let func_name = 'xml_fread';
    let offset = 0x01FA6B92;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p0 = args[0];
            this.p1 = args[1];
            this.p2 = args[2].toUInt32();
            this.p3 = args[3];
            if (enter_decode_45584C50)
            {
                //Logger.DEBUG(func_name, 'onEnter', {p0:this.p0, p1:this.p1, p2:this.p2, p3:this.p3});
            }
        }, 
        onLeave: function(retval) {
            if (enter_decode_45584C50)
            {
                Logger.DUMP(func_name, 'ptr len='+this.p2, dumpHex(this.p1, Math.min(0x20,this.p2)));
            }
        }
    })      
}
function hook_decode_45584C50(base_addr: NativePointer): void 
{
    // .text:01F9F564 ; _BOOL4 __cdecl decode_45584C50(XmlDeocdeA1 *a1, XmlDecodeParentV4 *a2, MyString *a3, XmlStatus *a4)
    let func_name = 'decode_45584C50';
    let offset = 0x1F9F564;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p0 = args[0];
            this.p1 = args[1];
            this.p2 = args[2];
            this.p3 = args[3];
            Logger.DEBUG(func_name, 'onEnter', {p0:this.p0, p1:this.p1, p2:this.p2, p3:this.p3});
            enter_decode_45584C50 = true ;
        }, 
        onLeave: function(retval) {
            enter_decode_45584C50 = false ;
        }
    })      
}
function hook_decode_4558_case7_1(base_addr: NativePointer): void 
{
    // .text:01FA48D0 ; _DWORD *__userpurge sub_1FA48D0@<eax>(XmlDecodeParentV4 *a1, int *a2, int *a3)
    let func_name = 'docodeCase7-1';
    let offset = 0x01FA48D0;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p0 = args[0];
            this.p1 = args[1];
            this.p2 = args[2];
            if (enter_decode_45584C50)
            {
                Logger.DEBUG(func_name, 'onEnter', {p0:this.p0, p1:this.p1, p2:this.p2});
                Logger.DUMP(func_name, 'onEnter a2', dumpHex(this.p1, 0x10));
                Logger.DUMP(func_name, 'onEnter a2[0]', dumpHex(this.p1.readPointer(), 0x10));
                Logger.DUMP(func_name, 'onEnter a2[1]', dumpHex(this.p1.add(4).readPointer(), 0x10));
                Logger.DUMP(func_name, 'onEnter a3', dumpHex(this.p2, 0x10));
            }
        }, 
        onLeave: function(retval) {
            Logger.DUMP(func_name, 'onLeave v5', dumpHex(this.p1.readPointer(), 0x54));
        }
    })      
}
function hook_decode_4558_case7_2(base_addr: NativePointer): void 
{
    // .text:01FA2AEA sub_1FA2AEA
    let func_name = 'docodeCase7-2';
    let offset = 0x01FA2AEA;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p0 = args[0];
            this.p1 = args[1];
            this.p2 = args[2];
            if (enter_decode_45584C50)
            {
                Logger.DEBUG(func_name, 'onEnter', {p0:this.p0, p1:this.p1, p2:this.p2});
                Logger.DUMP(func_name, 'onEnter a2', dumpHex(this.p1, 0x10));
                Logger.DUMP(func_name, 'onEnter a2[0]', dumpHex(this.p1.readPointer(), 0x10));
                Logger.DUMP(func_name, 'onEnter a3', dumpHex(this.p2, 0x10));
            }
        }, 
        onLeave: function(retval) {
            Logger.DUMP(func_name, 'onEnter a1', dumpHex(this.p1, 0x20));
            Logger.DUMP(func_name, 'onEnter *a1', dumpHex(this.p1.readPointer(), 0x10));
        }
    })      
}
function hook_decode_4558_case7_3(base_addr: NativePointer): void 
{
    // .text:01FA2650 sub_1FA2650
    let func_name = 'docodeCase7-3';
    let offset = 0x01FA2650;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p0 = args[0];
            this.p1 = args[1];
            this.p2 = args[2];
            if (enter_decode_45584C50)
            {
                Logger.DEBUG(func_name, 'onEnter', {p0:this.p0, p1:this.p1, p2:this.p2});
            }
        }, 
        onLeave: function(retval) {
            if (enter_decode_45584C50)
            {
                Logger.DUMP(func_name, 'onLeave a1', dumpHex(this.p0.readPointer(), 0x2d7));
            }

        }
    })      
}
function hook_xml_crypt_block(base_addr:NativePointer): void
{
    // .text:01FA26F8 ; unsigned int __cdecl xml_decode_crypt_block(_BYTE *pBuff, signed int a2, int a3, _BYTE *a4, unsigned int a5)
    let func_name = 'crypt_block';
    let offset = 0x01FA26F8;

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p0 = args[0];
            this.p1 = args[1];
            this.p2 = args[2];
            this.p3 = args[3];
            this.p4 = args[4];
            Logger.DEBUG(func_name, 'onEnter', {p0:this.p0, p1:this.p1, p2:this.p2, p3:this.p3, p4:this.p4});
            Logger.DUMP(func_name, 'onEnter a1', dumpHex(this.p0, 0x20));
            Logger.DUMP(func_name, 'onEnter a1[0]', dumpHex(this.p0.readPointer(), 0x20));
            Logger.DUMP(func_name, 'onEnter a4', dumpHex(this.p3, 0x20));
        }, 
        onLeave: function(retval) {
            Logger.DUMP(func_name, 'onLeave a1', dumpHex(this.p0, 0x20));
            Logger.DUMP(func_name, 'onLeave a1[0]', dumpHex(this.p0.readPointer(), 0x20));
            Logger.DUMP(func_name, 'onLeave a4', dumpHex(this.p3, 0x20));
        }
    })      

}
function hook_xml_decode(base_addr: NativePointer): void 
{
    let func_name = 'xml_decode';
    // let offset = 0x01F9E5BA;
    // let offset = 0x1fa0f19;
    let offset = 0x01FA0EEE;
    
    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            this.p0 = args[0];
            this.p1 = args[1];
            this.p2 = args[2];
            this.p3 = args[3];
            Logger.DEBUG(func_name, 'onEnter', {p0:this.p0, p1:this.p1, p2:this.p2, p3:this.p3});
        }, 
        onLeave: function(retval) {
            Logger.DUMP(func_name, 'onLeave ret', {ret: retval});
            Logger.DUMP(func_name, 'onLeave p1', dumpHex(this.p1, this.p2.toUInt32()));
            let trace = Thread.backtrace(this.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress) ;
            Logger.TRACE( func_name, 'call stack', trace);             
        }
    })      

}
export function hook_libgame() : void 
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

        //////////////////////////////////////////////////////////////////
        // <root><global> hex, hex2 </global></root>
        // hook_global_hex2_value(base_addr);
        // hook_global_hex_value(base_addr);
        // hook_hex_hash(base_addr);

        //////////////////////////////////////////////////////////////////
        // decode file
        // hook_decode_45584C50(base_addr);
        // hook_xml_fread(base_addr);
        // hook_decode_4558_case7_1(base_addr);
        // hook_decode_4558_case7_2(base_addr);
        // hook_decode_4558_case7_3(base_addr);
        // hook_xml_crypt_block(base_addr);

        // hook_xml_decode(base_addr);
    }
}
