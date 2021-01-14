(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
"use strict";

var e = this && this.__importDefault || function(e) {
  return e && e.__esModule ? e : {
    default: e
  };
};

Object.defineProperty(exports, "__esModule", {
  value: !0
});

const t = e(require("../logger"));

let a = "hook_java";

function r() {
  Java.use("com.playrix.lib.HttpManager").createHttpRequest.overload("com.playrix.lib.HttpManager$HttpRequest").implementation = function(e) {
    let a, r = [], o = "", n = e.content.value;
    for (n && (o = Array.from(n, (function(e) {
      return ("0" + (255 & e).toString(16)).slice(-2);
    })).join("")), a = 0; a < e.headers.value.length; a += 2) r.push(e.headers.value[a] + ":" + e.headers.value[a + 1]);
    return t.default.INFO("createHttpRequest", "createHttpRequest", {
      method: e.method.value,
      url: e.url.value,
      body: o,
      body_len: n.length,
      contentType: e.contentType.value,
      headers: r
    }), this.createHttpRequest(e);
  };
}

function o() {
  var e = Java.use("java.io.InputStream");
  e.read.overload().implementation = function() {
    let a = e.read.overload().call(this);
    return t.default.DEBUG("inputstream", "is.read()", {
      ret: a
    }), a;
  }, e.read.overload("[B").implementation = function(a) {
    let r = e.read.overload("[B").call(this, a), o = [];
    for (let e = 0; e < r && e < 5; ++e) o.push(a[e]);
    return t.default.DEBUG("inputstream", "is.read(byte[] bArr)", {
      ret: r,
      result: o
    }), r;
  };
}

function n() {
  Java.use("com.playrix.lib.HttpManager").createHttpResponse.overload("okhttp3.Response").implementation = function(e) {
    let a, r = this.createHttpResponse(e), o = [];
    for (a = 0; a < r.headers.value.length; a += 2) o.push(r.headers.value[a] + ":" + r.headers.value[a + 1]);
    return t.default.INFO("createHttpResponse", "createHttpResponse", {
      code: r.code.value,
      message: r.message.value,
      headers: o,
      body: e.body.value
    }), r;
  };
}

function l() {
  let e = "hookHttpReq";
  Java.use("com.playrix.lib.HttpManager").httpRequestSync.overload("long", "com.playrix.lib.HttpManager$HttpRequest").implementation = function(a, r) {
    t.default.INFO(e, "httpRequestSync", {
      allowRedirects: r.allowRedirects.value,
      headers: r.headers.value,
      method: r.method.value,
      openTimeout: r.openTimeout.value,
      readTimeout: r.readTimeout.value,
      url: r.url.value
    });
    let o = Thread.backtrace(this.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress);
    return t.default.TRACE(e, "httpRequestSync", o), this.httpRequestSync(a, r);
  };
}

function u() {
  let e = "hookHttpReq";
  Java.use("com.playrix.lib.HttpManager").httpRequestAsync.overload("long", "com.playrix.lib.HttpManager$HttpRequest").implementation = function(a, r) {
    t.default.INFO(e, "httpRequestAsync", {
      allowRedirects: r.allowRedirects.value,
      headers: r.headers.value,
      method: r.method.value,
      openTimeout: r.openTimeout.value,
      readTimeout: r.readTimeout.value,
      url: r.url.value
    });
    let o = Thread.backtrace(this.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress);
    return t.default.TRACE(e, "httpRequestAsync", o), this.httpRequestAsync(a, r);
  };
}

function s(e, t, a) {
  let r = [];
  for (let e = 0; e < a.length; e++) r.push("arg_" + e);
  var o = "result = this.__FUNCNAME__(__SEPARATED_ARG_NAMES__);\nlogmessage = '__CLASSNAME__.__FUNCNAME__(' + __SEPARATED_ARG_NAMES__ + ') => ' + result;\nconsole.log(logmessage);\nreturn result;";
  o = (o = (o = (o = o.replace(/__FUNCNAME__/g, t)).replace(/__SEPARATED_ARG_NAMES__/g, r.join(", "))).replace(/__CLASSNAME__/g, e)).replace(/\+  \+/g, "+"), 
  r.push(o), console.log(r);
}

function c() {
  var e = Java.vm.getEnv().handle.readPointer();
  console.log("\t[*] env handle: " + e);
  var r = e.add(1352).readPointer();
  console.log("\t[*] GetStringUTFChars addr: " + r), Interceptor.attach(r, {
    onEnter: function(e) {
      try {
        var r = Java.use("java.lang.String"), o = Java.cast(e[1], r);
        if ("township.playrix.com" == o.toString()) {
          let e = Thread.backtrace(this.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress);
          t.default.TRACE(a, "httpRequestAsync", e);
        }
        console.log("\t\t[*] GetStringUTFChars: " + o);
      } catch (e) {}
    }
  });
}

function i() {
  var e = Java.vm.getEnv().handle.readPointer();
  console.log("\t[*] env handle: " + e);
  var t = e.add(1336).readPointer();
  console.log("\t[*] NewStringUTF addr: " + t), Interceptor.attach(t, {
    onEnter: function(e) {
      try {
        var t = Java.use("java.lang.String"), a = Java.cast(e[1], t);
        console.log("\t\t[*] NewStringUTF: " + a);
      } catch (e) {}
    }
  });
}

function d() {
  r(), n();
}

exports.default = d;

},{"../logger":6}],2:[function(require,module,exports){
"use strict";

var t = this && this.__importDefault || function(t) {
  return t && t.__esModule ? t : {
    default: t
  };
};

Object.defineProperty(exports, "__esModule", {
  value: !0
}), exports.end_hook_fread = exports.start_hook_fread = exports.hook_libc = void 0;

const e = t(require("../logger")), o = !1;

function n(t, e) {
  const o = Java.use("java.io.File"), n = Java.use("java.io.FileInputStream"), a = Java.use("java.io.FileOutputStream"), i = Java.use("java.io.BufferedInputStream"), r = Java.use("java.io.BufferedOutputStream");
  var l = o.$new.overload("java.lang.String").call(o, e);
  if (l.exists()) return !0;
  var f = o.$new.overload("java.lang.String").call(o, t);
  if (f.exists() && f.canRead()) {
    for (var d, s = n.$new.overload("java.io.File").call(n, f), c = i.$new.overload("java.io.InputStream").call(i, s), u = 0, h = ""; -1 != (u = c.read()); ) h += String.fromCharCode(u);
    var p = h.split("\n"), m = !1;
    for (d = 0; d < p.length; d++) if (-1 !== p[d].indexOf("State:")) ; else if (-1 !== p[d].indexOf("TracerPid:")) {
      if (console.log("chagne " + p[d] + ' to "TracerPid:      0"'), "TracerPid:      0" == p[d]) continue;
      p[d] = "TracerPid:      0", m = !0;
    } else -1 === p[d].indexOf("frida") && -1 === p[d].indexOf("Frida") || (p[d] = "");
    if (!1 === m) return !1;
    h = p.join("\n"), l.createNewFile();
    var v = a.$new.overload("java.io.File").call(a, l), E = r.$new.overload("java.io.OutputStream").call(r, v);
    for (d = 0; d < h.length; d++) E.write(h.charCodeAt(d));
    return c.close(), s.close(), E.close(), v.close(), !0;
  }
  console.log("Error : File cannot read.");
}

function a(t) {
  if (t && -1 !== t.indexOf("/proc")) {
    if (-1 !== t.indexOf("/status")) return !0;
    if (-1 !== t.indexOf("/maps")) return !0;
  }
  return !1;
}

var i = {};

function r() {
  let t = "hook_open", o = null;
  o = Module.findExportByName("libc.so", "open"), o ? Interceptor.attach(o, {
    onEnter: function(o) {
      let i = o[0].readCString();
      if (this.path = i, i && a(i)) {
        let a = "/sdcard/Android/data/com.playrix.township/files/status_" + this.threadId + "_" + i.replaceAll("/", "_");
        Java.perform((function() {
          n(i, a) ? (o[0] = Memory.allocUtf8String(a), e.default.DEBUG(t, "open", {
            path: i,
            mode: o[1],
            new_path: a
          })) : e.default.DEBUG(t, "open", {
            path: i,
            mode: o[1]
          });
        }));
      }
    },
    onLeave: function(t) {
      i[t.toInt32()] = this.path;
    }
  }) : e.default.ERROR(t, "Failed to find open in libc.so");
}

var l = null;

function f() {
  let t = "hook_fopen", o = "fopen", i = null;
  i = Module.findExportByName("libc.so", o), i ? Interceptor.attach(i, {
    onEnter: function(o) {
      this.path = o[0].readCString(), this.mode = o[1].readCString();
      let i = this.path;
      if (this.path && a(this.path)) {
        let a = "/sdcard/Android/data/com.playrix.township/files/status_" + this.threadId + "_" + this.path.replaceAll("/", "_");
        Java.perform((function() {
          n(i, a) ? (o[0] = Memory.allocUtf8String(a), e.default.DEBUG(t, "fopen", {
            path: i,
            mode: o[1].readCString(),
            new_path: a
          })) : e.default.DEBUG(t, "fopen", {
            path: i,
            mode: o[1].readCString()
          });
        }));
      }
    },
    onLeave: function(t) {}
  }) : e.default.ERROR(t, "Failed to find open in libc.so");
}

var d = 0;

function s() {
  d += 1;
}

function c() {
  d -= 1;
}

function u() {
  let t = "hook_fread", o = null;
  o = Module.findExportByName("libc.so", "fread"), o ? Interceptor.attach(o, {
    onEnter: function(t) {
      this.destBuff = t[0], this.elementSize = t[1], this.count = t[2], this.fp = t[3];
    },
    onLeave: function(o) {
      (d > 0 || this.fp.toUInt32() == l) && (l = this.fp.toUInt32(), e.default.DEBUG(t, "fread", {
        destBuff: this.destBuff,
        elementSize: this.elementSize,
        count: this.count,
        fp: this.fp,
        ret: o
      }), e.default.DUMP(t, "fread", hexdump(this.destBuff, {
        offset: 0,
        length: Math.min(16, this.count.toUInt32()),
        header: !0,
        ansi: !1
      })));
    }
  }) : e.default.ERROR(t, "Failed to find open in libc.so");
}

function h() {
  let t = "hook_fwrite", o = "fwrite", n = null;
  n = Module.findExportByName("libc.so", o), n ? Interceptor.attach(n, {
    onEnter: function(t) {
      this.destBuff = t[0], this.elementSize = t[1], this.count = t[2], this.fp = t[3];
    },
    onLeave: function(n) {
      if (this.fp.toUInt32() == l) {
        e.default.DEBUG(t, o, {
          destBuff: this.destBuff,
          elementSize: this.elementSize,
          count: this.count,
          fp: this.fp,
          ret: n
        }), e.default.DUMP(t, o, hexdump(this.destBuff, {
          offset: 0,
          length: this.count.toUInt32(),
          header: !0,
          ansi: !1
        }));
        let a = Thread.backtrace(this.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress);
        e.default.TRACE(t, o, a);
      }
    }
  }) : e.default.ERROR(t, "Failed to find open in libc.so");
}

function p() {
  let t = "hook_fclose", o = "fclose", n = null;
  n = Module.findExportByName("libc.so", o), n ? Interceptor.attach(n, {
    onEnter: function(n) {
      if (this.fp = n[0], this.fp.toUInt32() == l) {
        l = null;
        let n = Thread.backtrace(this.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress);
        e.default.TRACE(t, o, n);
      }
    },
    onLeave: function(t) {}
  }) : e.default.ERROR(t, "Failed to find open in libc.so");
}

function m() {
  let t = "hook_fstat", o = "fstat", n = null;
  n = Module.findExportByName("libc.so", o), n ? Interceptor.attach(n, {
    onEnter: function(n) {
      let r = n[0].toInt32(), l = "" + r;
      r in i && (l = i[r]), l && a(l) && e.default.DEBUG(t, o, {
        path: l,
        arg1: n[1]
      });
    },
    onLeave: function(t) {}
  }) : e.default.ERROR(t, "Failed to find open in libc.so");
}

function v() {
  let t = "hook_lstat", o = "lstat", n = null;
  n = Module.findExportByName("libc.so", o), n ? Interceptor.attach(n, {
    onEnter: function(n) {
      let i = n[0].readCString();
      i && a(i) && e.default.DEBUG(t, o, {
        path: i,
        mode: n[1]
      });
    },
    onLeave: function(t) {}
  }) : e.default.ERROR(t, "Failed to find open in libc.so");
}

function E() {
  let t = "hook_stat", o = "stat", n = null;
  n = Module.findExportByName("libc.so", o), n ? Interceptor.attach(n, {
    onEnter: function(n) {
      let i = n[0].readCString();
      i && a(i) && e.default.DEBUG(t, o, {
        path: i,
        mode: n[1]
      });
    },
    onLeave: function(t) {}
  }) : e.default.ERROR(t, "Failed to find open in libc.so");
}

function _() {
  Process.getModuleByName("libc.so").enumerateExports().filter((t => "function" === t.type && [ "connect", "recv", "send", "read", "write" ].some((e => 0 === t.name.indexOf(e))))).forEach((t => {
    Interceptor.attach(t.address, {
      onEnter: function(o) {
        var n = o[0].toInt32();
        if ("tcp" === Socket.type(n)) {
          var a = Socket.peerAddress(n);
          null !== a && e.default.DEBUG("hook_socket", t.name, JSON.stringify(a));
        }
      }
    });
  }));
}

function x() {
  r(), f(), u(), _();
}

exports.start_hook_fread = s, exports.end_hook_fread = c, exports.hook_libc = x;

},{"../logger":6}],3:[function(require,module,exports){
"use strict";

var t = this && this.__importDefault || function(t) {
  return t && t.__esModule ? t : {
    default: t
  };
};

Object.defineProperty(exports, "__esModule", {
  value: !0
}), exports.hook_libgame = void 0;

const e = t(require("../logger"));

function a(t, e) {
  return hexdump(t, {
    offset: 0,
    length: e,
    header: !0,
    ansi: !1
  });
}

function n(t) {
  let a = "proc_status", n = 34677964;
  e.default.INFO(a, "start to hook", {
    base_addr: t,
    offset: n
  }), Interceptor.attach(t.add(n), {
    onEnter: function(t) {
      e.default.INFO(a, "called");
    },
    onLeave: function(t) {
      e.default.DEBUG(a, "return new value(0x0)", {
        old_ret: t
      }), t.replace(ptr("0x0"));
    }
  });
}

function o(t) {
  let a = "check_rooting", n = 34682599;
  e.default.INFO(a, "start to hook", {
    base_addr: t,
    offset: n
  }), Interceptor.attach(t.add(n), {
    onEnter: function(t) {
      e.default.INFO(a, "called");
    },
    onLeave: function(t) {
      e.default.DEBUG(a, "return new value(0x0)", {
        old_ret: t
      }), t.replace(ptr("0x0"));
    }
  });
}

function i(t) {
  let a = "check_emulator", n = 34693901;
  e.default.INFO(a, "start to hook", {
    base_addr: t,
    offset: n
  }), Interceptor.attach(t.add(n), {
    onEnter: function(t) {
      e.default.INFO(a, "called");
    },
    onLeave: function(t) {
      e.default.DEBUG(a, "return new value(0x0)", {
        old_ret: t
      }), t.replace(ptr("0x0"));
    }
  });
}

var p = !1;

function r(t) {
  let n = "GlobalHex", o = 26635948;
  e.default.INFO(n, "start to hook", {
    base_addr: t,
    offset: o
  }), Interceptor.attach(t.add(o), {
    onEnter: function(t) {
      if (this.p0 = t[0], this.p1 = t[1], this.p2 = t[2], this.p3 = t[3], p) {
        e.default.DEBUG(n, "onEnter", {
          p0: this.p0,
          p1: this.p1,
          p2: this.p2,
          p3: this.p3
        }), e.default.DumpMyString(n, "onEnter p0", this.p0), e.default.DUMP(n, "onEnter p1", a(this.p1, 16)), 
        e.default.DumpMyString(n, "onEnter p2", this.p2), e.default.DumpMyString(n, "onEnter p3", this.p3);
        let t = Thread.backtrace(this.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress);
        e.default.TRACE(n, "call stack", t);
      }
    },
    onLeave: function(t) {
      p && (e.default.DEBUG(n, "onLeave", {
        ret: t
      }), e.default.DUMP(n, "onEnter p1", a(this.p1, 16)), e.default.DumpMyString(n, "onLeave p0", this.p0));
    }
  });
}

function s(t) {
  let n = "hexhash", o = 26912482;
  e.default.INFO(n, "start to hook", {
    base_addr: t,
    offset: o
  }), Interceptor.attach(t.add(o), {
    onEnter: function(t) {
      this.p0 = t[0], this.p1 = t[1], this.p2 = t[2], p && (e.default.DEBUG(n, "onEnter", {
        p0: this.p0,
        p1: this.p1,
        p2: this.p2
      }), e.default.DumpMyString(n, "onEnter p0", this.p0), e.default.DUMP(n, "onEnter p1", a(this.p1, 16)), 
      e.default.DUMP(n, "onEnter p2", a(this.p2, 16)));
    },
    onLeave: function(t) {
      p && (e.default.DEBUG(n, "onLeave", {
        ret: t
      }), e.default.DumpMyString(n, "onLeave p0", this.p0));
    }
  });
}

function d(t) {
  let a = "HexTwice", n = 26914014;
  e.default.INFO(a, "start to hook", {
    base_addr: t,
    offset: n
  }), Interceptor.attach(t.add(n), {
    onEnter: function(t) {
      this.p0 = t[0], this.p1 = t[1], this.p2 = t[2], e.default.DumpMyString(a, "onEnter p1", this.p1), 
      p = !0;
    },
    onLeave: function(t) {
      p = !1;
    }
  });
}

var f = !1;

function h(t) {
  let n = "xml_fread", o = 33188754;
  e.default.INFO(n, "start to hook", {
    base_addr: t,
    offset: o
  }), Interceptor.attach(t.add(o), {
    onEnter: function(t) {
      this.p0 = t[0], this.p1 = t[1], this.p2 = t[2].toUInt32(), this.p3 = t[3];
    },
    onLeave: function(t) {
      f && e.default.DUMP(n, "ptr len=" + this.p2, a(this.p1, Math.min(32, this.p2)));
    }
  });
}

function u(t) {
  let a = "decode_45584C50", n = 33158500;
  e.default.INFO(a, "start to hook", {
    base_addr: t,
    offset: n
  }), Interceptor.attach(t.add(n), {
    onEnter: function(t) {
      this.p0 = t[0], this.p1 = t[1], this.p2 = t[2], this.p3 = t[3], e.default.DEBUG(a, "onEnter", {
        p0: this.p0,
        p1: this.p1,
        p2: this.p2,
        p3: this.p3
      }), f = !0;
    },
    onLeave: function(t) {
      f = !1;
    }
  });
}

function l(t) {
  let n = "docodeCase7-1", o = 33179856;
  e.default.INFO(n, "start to hook", {
    base_addr: t,
    offset: o
  }), Interceptor.attach(t.add(o), {
    onEnter: function(t) {
      this.p0 = t[0], this.p1 = t[1], this.p2 = t[2], f && (e.default.DEBUG(n, "onEnter", {
        p0: this.p0,
        p1: this.p1,
        p2: this.p2
      }), e.default.DUMP(n, "onEnter a2", a(this.p1, 16)), e.default.DUMP(n, "onEnter a2[0]", a(this.p1.readPointer(), 16)), 
      e.default.DUMP(n, "onEnter a2[1]", a(this.p1.add(4).readPointer(), 16)), e.default.DUMP(n, "onEnter a3", a(this.p2, 16)));
    },
    onLeave: function(t) {
      e.default.DUMP(n, "onLeave v5", a(this.p1.readPointer(), 84));
    }
  });
}

function c(t) {
  let n = "docodeCase7-2", o = 33172202;
  e.default.INFO(n, "start to hook", {
    base_addr: t,
    offset: o
  }), Interceptor.attach(t.add(o), {
    onEnter: function(t) {
      this.p0 = t[0], this.p1 = t[1], this.p2 = t[2], f && (e.default.DEBUG(n, "onEnter", {
        p0: this.p0,
        p1: this.p1,
        p2: this.p2
      }), e.default.DUMP(n, "onEnter a2", a(this.p1, 16)), e.default.DUMP(n, "onEnter a2[0]", a(this.p1.readPointer(), 16)), 
      e.default.DUMP(n, "onEnter a3", a(this.p2, 16)));
    },
    onLeave: function(t) {
      e.default.DUMP(n, "onEnter a1", a(this.p1, 32)), e.default.DUMP(n, "onEnter *a1", a(this.p1.readPointer(), 16));
    }
  });
}

function E(t) {
  let n = "docodeCase7-3", o = 33171024;
  e.default.INFO(n, "start to hook", {
    base_addr: t,
    offset: o
  }), Interceptor.attach(t.add(o), {
    onEnter: function(t) {
      this.p0 = t[0], this.p1 = t[1], this.p2 = t[2], f && e.default.DEBUG(n, "onEnter", {
        p0: this.p0,
        p1: this.p1,
        p2: this.p2
      });
    },
    onLeave: function(t) {
      f && e.default.DUMP(n, "onLeave a1", a(this.p0.readPointer(), 727));
    }
  });
}

function D(t) {
  let n = "crypt_block", o = 33171192;
  e.default.INFO(n, "start to hook", {
    base_addr: t,
    offset: o
  }), Interceptor.attach(t.add(o), {
    onEnter: function(t) {
      this.p0 = t[0], this.p1 = t[1], this.p2 = t[2], this.p3 = t[3], this.p4 = t[4], 
      e.default.DEBUG(n, "onEnter", {
        p0: this.p0,
        p1: this.p1,
        p2: this.p2,
        p3: this.p3,
        p4: this.p4
      }), e.default.DUMP(n, "onEnter a1", a(this.p0, 32)), e.default.DUMP(n, "onEnter a1[0]", a(this.p0.readPointer(), 32)), 
      e.default.DUMP(n, "onEnter a4", a(this.p3, 32));
    },
    onLeave: function(t) {
      e.default.DUMP(n, "onLeave a1", a(this.p0, 32)), e.default.DUMP(n, "onLeave a1[0]", a(this.p0.readPointer(), 32)), 
      e.default.DUMP(n, "onLeave a4", a(this.p3, 32));
    }
  });
}

function U(t) {
  let n = "xml_decode", o = 33165038;
  e.default.INFO(n, "start to hook", {
    base_addr: t,
    offset: o
  }), Interceptor.attach(t.add(o), {
    onEnter: function(t) {
      this.p0 = t[0], this.p1 = t[1], this.p2 = t[2], this.p3 = t[3], e.default.DEBUG(n, "onEnter", {
        p0: this.p0,
        p1: this.p1,
        p2: this.p2,
        p3: this.p3
      });
    },
    onLeave: function(t) {
      e.default.DUMP(n, "onLeave ret", {
        ret: t
      }), e.default.DUMP(n, "onLeave p1", a(this.p1, this.p2.toUInt32()));
      let o = Thread.backtrace(this.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress);
      e.default.TRACE(n, "call stack", o);
    }
  });
}

function M() {
  let t = "libgame.so", a = Module.findBaseAddress("libgame.so");
  e.default.INFO(t, "base address", {
    addr: a
  }), a ? (n(a), o(a), i(a)) : e.default.ERROR(t, "Failed to find base address of libgame.so");
}

exports.hook_libgame = M;

},{"../logger":6}],4:[function(require,module,exports){
"use strict";

var e = this && this.__importDefault || function(e) {
  return e && e.__esModule ? e : {
    default: e
  };
};

Object.defineProperty(exports, "__esModule", {
  value: !0
});

const t = e(require("./../logger"));

function o(e, o) {
  let n = "hook_module", l = null, d = 0;
  l = Module.findExportByName(null, "android_dlopen_ext"), l ? (t.default.INFO(n, "Found android_dlopen_ext", {
    addr: l
  }), Interceptor.attach(l, {
    onEnter: function(o) {
      try {
        let l = o[0].readCString();
        l && l.indexOf("libgame.so") >= 0 && (t.default.INFO(n, "onEnter libgame.so"), d = 1, 
        e(this, o));
      } catch (e) {
        console.log(e);
      }
    },
    onLeave: function(e) {
      d && (d = 0, t.default.INFO(n, "onLeave libgame.so"), o(this, e));
    }
  })) : t.default.ERROR(n, "Failed to find android_dlopen_ext", {
    addr: l
  });
}

function n(e, o) {
  let n = "hook_module", l = null, d = 0;
  l = Module.findExportByName(null, "dlopen"), l ? (t.default.INFO(n, "Found dlopen", {
    addr: l
  }), Interceptor.attach(l, {
    onEnter: function(o) {
      try {
        let l = o[0].readCString();
        l && l.indexOf("libc.so") >= 0 && (t.default.INFO(n, "onEnter libc.so"), d = 1, 
        e(this, o));
      } catch (e) {
        console.log(e);
      }
    },
    onLeave: function(e) {
      d && (d = 0, t.default.INFO(n, "onLeave libc.so"), o(this, e));
    }
  })) : t.default.ERROR(n, "Failed to find dlopen", {
    addr: l
  });
}

const l = {
  libgame: o,
  libc: n
};

exports.default = l;

},{"./../logger":6}],5:[function(require,module,exports){
"use strict";

function e() {
  let e = Java.use("javax.net.ssl.X509TrustManager"), t = Java.use("javax.net.ssl.SSLContext"), a = [ Java.registerClass({
    name: "com.sensepost.test.TrustManager",
    implements: [ e ],
    methods: {
      checkClientTrusted: function(e, t) {},
      checkServerTrusted: function(e, t) {},
      getAcceptedIssuers: function() {
        return [];
      }
    }
  }).$new() ], n = t.init.overload("[Ljavax.net.ssl.KeyManager;", "[Ljavax.net.ssl.TrustManager;", "java.security.SecureRandom");
  n.implementation = function(e, t, r) {
    n.call(this, e, a, r);
  };
  try {
    Java.use("okhttp3.CertificatePinner").check.overload("java.lang.String", "java.util.List").implementation = function() {};
  } catch (e) {
    if (0 === e.message.indexOf("ClassNotFoundException")) throw new Error(e);
  }
  try {
    Java.use("appcelerator.https.PinningTrustManager").checkServerTrusted.implementation = function() {};
  } catch (e) {
    if (0 === e.message.indexOf("ClassNotFoundException")) throw new Error(e);
  }
  try {
    Java.use("com.android.org.conscrypt.TrustManagerImpl").verifyChain.implementation = function(e, t, a, n, r, s) {
      return e;
    };
  } catch (e) {
    if (0 === e.message.indexOf("ClassNotFoundException")) throw new Error(e);
  }
  try {
    Java.use("com.android.org.conscrypt.TrustManagerImpl").checkTrustedRecursive.implementation = function(e, t, a, n, r, s) {
      return Java.use("java.util.ArrayList").$new();
    };
  } catch (e) {
    if (0 === e.message.indexOf("ClassNotFoundException")) throw new Error(e);
  }
  try {
    Java.use("nl.xservices.plugins.SSLCertificateChecker").execute.overload("java.lang.String", "org.json.JSONArray", "org.apache.cordova.CallbackContext").implementation = function(e, t, a) {
      return a.success("CONNECTION_SECURE"), !0;
    };
  } catch (e) {
    if (0 === e.message.indexOf("ClassNotFoundException")) throw new Error(e);
  }
}

Object.defineProperty(exports, "__esModule", {
  value: !0
}), exports.default = e;

},{}],6:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: !0
});

const t = 15;

function e(t, e) {
  return hexdump(t, {
    offset: 0,
    length: e,
    header: !0,
    ansi: !1
  });
}

class a {
  static _SEND(t, e, a, s) {
    let d = {
      thread_id: Process.getCurrentThreadId(),
      log_level: t,
      function: e && e.length > 15 ? e.substr(0, 15) : e,
      msg: a,
      data: s
    };
    send(d);
  }
  static DEBUG(t, e, s) {
    a._SEND("D", t, e, s);
  }
  static INFO(t, e, s) {
    a._SEND("I", t, e, s);
  }
  static ERROR(t, e, s) {
    a._SEND("E", t, e, s);
  }
  static TRACE(t, e, s) {
    a._SEND("T", t, e, s);
  }
  static DUMP(t, e, s) {
    a._SEND("P", t, e, s);
  }
  static DumpMyString(t, s, d) {
    let r, i = d.readU8(), n = 0, c = 0;
    1 & i ? (n = d.readU32() - 1, c = d.add(4).readU32(), r = d.add(8).readPointer()) : (n = 15, 
    c = i / 2, r = d.add(1)), a.DUMP(t, s + " len=" + c, e(r, c));
  }
}

exports.default = a;

},{}],7:[function(require,module,exports){
"use strict";

var e = this && this.__importDefault || function(e) {
  return e && e.__esModule ? e : {
    default: e
  };
};

Object.defineProperty(exports, "__esModule", {
  value: !0
});

const o = e(require("./logger")), r = e(require("./hooks/ssl")), t = e(require("./hooks/module")), u = require("./hooks/libgame_7.9.5"), l = require("./hooks/libc"), i = e(require("./hooks/java"));

function a(e, o) {}

function s(e, o) {}

function f(e, r) {
  u.hook_libgame();
  for (let e = 0; e < 30; e++) o.default.DEBUG("onload libgame.so", "sleep " + (e + 1) + " / 30"), 
  Thread.sleep(1);
}

o.default.INFO("MAIN", "start to hook"), Java.perform((function() {
  r.default(), i.default(), t.default.libgame(a, f), l.hook_libc();
}));

},{"./hooks/java":1,"./hooks/libc":2,"./hooks/libgame_7.9.5":3,"./hooks/module":4,"./hooks/ssl":5,"./logger":6}]},{},[7])
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIm5vZGVfbW9kdWxlcy9icm93c2VyLXBhY2svX3ByZWx1ZGUuanMiLCJzcmMvaG9va3MvamF2YS50cyIsInNyYy9ob29rcy9saWJjLnRzIiwic3JjL2hvb2tzL2xpYmdhbWVfNy45LjUudHMiLCJzcmMvaG9va3MvbW9kdWxlLnRzIiwic3JjL2hvb2tzL3NzbC50cyIsInNyYy9sb2dnZXIudHMiLCJzcmMvbWFpbi50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtBQ0FBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUM1SUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FDdk9BO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUNyU0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUNoRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOzs7Ozs7OztBQ3BEQSxNQUFNLElBQTRCOztBQUVsQyxTQUFTLEVBQVEsR0FBMEI7RUFXdkMsT0FUVSxRQUNOLEdBQ0E7SUFDSSxRQUFPO0lBQ1AsUUFBTztJQUNQLFNBQU87SUFDUCxPQUFLOzs7O0FBTWpCLE1BQU07RUFFRixhQUFhLEdBQWtCLEdBQWtCLEdBQVk7SUFFekQsSUFBSSxJQUFVO01BQ1YsV0FBVyxRQUFRO01BQ25CLFdBQVc7TUFDWCxVQUFVLEtBQWEsRUFBVSxTQXZCWCxLQXVCd0MsRUFBVSxPQUFPLEdBdkJ6RCxNQXVCK0U7TUFDckcsS0FBSztNQUNMLE1BQUs7O0lBRVQsS0FBSzs7RUFFVCxhQUFhLEdBQWtCLEdBQVk7SUFFdkMsRUFBTyxNQUFNLEtBQUssR0FBVyxHQUFLOztFQUV0QyxZQUFZLEdBQWtCLEdBQVk7SUFFdEMsRUFBTyxNQUFNLEtBQUssR0FBVyxHQUFLOztFQUV0QyxhQUFhLEdBQWtCLEdBQVk7SUFFdkMsRUFBTyxNQUFNLEtBQUssR0FBVyxHQUFLOztFQUV0QyxhQUFhLEdBQWtCLEdBQVk7SUFFdkMsRUFBTyxNQUFNLEtBQUssR0FBVyxHQUFLOztFQUV0QyxZQUFZLEdBQWtCLEdBQVk7SUFFdEMsRUFBTyxNQUFNLEtBQUssR0FBVyxHQUFLOztFQUd0QyxvQkFBb0IsR0FBa0IsR0FBWTtJQUU5QyxJQUdJLEdBSEEsSUFBSyxFQUFVLFVBQ2YsSUFBTyxHQUNQLElBQU07SUFFQSxJQUFMLEtBRUQsSUFBTyxFQUFVLFlBQVksR0FDN0IsSUFBTSxFQUFVLElBQUksR0FBTSxXQUMxQixJQUFPLEVBQVUsSUFBSSxHQUFNLGtCQUkzQixJQUFPO0lBQ1AsSUFBTSxJQUFLLEdBQ1gsSUFBTyxFQUFVLElBQUksS0FFekIsRUFBTyxLQUFLLEdBQVcsSUFBTSxVQUFVLEdBQUssRUFBUSxHQUFNOzs7O0FBSWxFLFFBQUEsVUFBZTs7Ozs7Ozs7Ozs7Ozs7O0FDekVmLE1BQUEsSUFBQSxFQUFBLFFBQUEsY0FDQSxJQUFBLEVBQUEsUUFBQSxpQkFDQSxJQUFBLEVBQUEsUUFBQSxvQkFDQSxJQUFBLFFBQUEsMEJBQ0EsSUFBQSxRQUFBLGlCQUNBLElBQUEsRUFBQSxRQUFBOztBQUlBLFNBQVMsRUFBWSxHQUF1Qjs7QUFDNUMsU0FBUyxFQUFjLEdBQXVCOztBQUU5QyxTQUFTLEVBQWdCLEdBQXVCO0VBRTVDLEVBQUE7RUFDQSxLQUFNLElBQUksSUFBSSxHQUFJLElBQUksSUFBSyxLQUV2QixFQUFBLFFBQU8sTUFBTSxxQkFBcUIsWUFBWSxJQUFFLEtBQUs7RUFDckQsT0FBTyxNQUFNOzs7QUFYckIsRUFBQSxRQUFPLEtBQUssUUFBUSxrQkFvQnBCLEtBQUssU0FBUTtFQUNULEVBQUEsV0FDQSxFQUFBLFdBQ0EsRUFBQSxRQUFZLFFBQVEsR0FBYSxJQUVqQyxFQUFBIiwiZmlsZSI6ImdlbmVyYXRlZC5qcyIsInNvdXJjZVJvb3QiOiIifQ==
