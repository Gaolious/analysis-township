import Logger from "../logger";

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

function hook_decode_keyword(base_addr: NativePointer): void 
{
    let addr = null;
    let i ;
    let loaded_libc = 0 ;
    let func_name = 'Keyword';
    let offset = 0x20F5585;  // 7.9.6

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            Logger.INFO(func_name, 'called');
            this.p0 = args[0]; // buffer
            this.p1 = args[1]; // target
            this.p2 = args[2].toUInt32();
            Logger.DUMP(func_name, 'buff : ', {addr: args[1].sub(base_addr), len:this.p2});
        }, 
        onLeave: function(retval) {
            Logger.DumpMyString(func_name, 'output string', this.p0 );
        }
    })      
}

function hook_banned_from_server(base_addr: NativePointer): void 
{
    let addr = null;
    let i ;
    let loaded_libc = 0 ;
    let func_name = 'Banned';
    let offset = 0x01133906;  // 7.9.6

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            Logger.DEBUG(func_name, 'onEnter');
        }, 
        onLeave: function(retval) {
            Logger.DEBUG(func_name, 'onLeave', {retval:retval});
        }
    })      
}

function hook_banned_from_server2(base_addr: NativePointer): void 
{
    let func_name = 'Banned2';
    let offset = 0x01E1D900;  // 7.9.6

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            Logger.DEBUG(func_name, 'onEnter');
        }, 
        onLeave: function(retval) {
            Logger.DEBUG(func_name, 'onLeave', {retval:retval});
        }
    })      
}
function hook_banned_from_server3(base_addr: NativePointer): void 
{
    let func_name = 'Banned3';
    let offset = 0x01D4B404;  // 7.9.6

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            Logger.DEBUG(func_name, 'onEnter');
        }, 
        onLeave: function(retval) {
            Logger.DEBUG(func_name, 'onLeave', {retval:retval});
        }
    })      
}
function hook_banned_from_server4(base_addr: NativePointer): void 
{
    let func_name = 'Banned4';
    let offset = 0x01D491B0;  // 7.9.6

    Logger.INFO(func_name, 'start to hook', {base_addr:base_addr, offset:offset});
    Interceptor.attach( base_addr.add(offset), {
        onEnter: function(args) {
            Logger.DEBUG(func_name, 'onEnter');
        }, 
        onLeave: function(retval) {
            Logger.DEBUG(func_name, 'onLeave', {retval:retval});
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
        hook_decode_keyword(base_addr);

        hook_banned_from_server(base_addr);
        hook_banned_from_server2(base_addr);
        hook_banned_from_server3(base_addr);
        hook_banned_from_server4(base_addr);
    }
}
