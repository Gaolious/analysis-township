function hook_ssl_pinning()
{
    let func_name = 'ssl_pinning';
    let X509TrustManager = Java.use('javax.net.ssl.X509TrustManager');
    let SSLContext = Java.use('javax.net.ssl.SSLContext');

    let TrustManager = Java.registerClass({
        name: 'com.sensepost.test.TrustManager',
        implements: [X509TrustManager],
        methods: {
            checkClientTrusted: function (chain, authType) {},
            checkServerTrusted: function (chain, authType) {},
            getAcceptedIssuers: function () {
                return [];
            }
        }
    });

    let TrustManagers = [TrustManager.$new()];
    let SSLContext_init = SSLContext.init.overload(
        '[Ljavax.net.ssl.KeyManager;', '[Ljavax.net.ssl.TrustManager;', 'java.security.SecureRandom');

    SSLContext_init.implementation = function (keyManager:any, trustManager:any, secureRandom:any) {
        SSLContext_init.call(this, keyManager, TrustManagers, secureRandom);
    };

    try {
        var CertificatePinner = Java.use('okhttp3.CertificatePinner');
        CertificatePinner.check.overload('java.lang.String', 'java.util.List').implementation = function () {}
    } catch (err) {
        if (err.message.indexOf('ClassNotFoundException') === 0) {
            throw new Error(err);
        }
    }

    try {
        var PinningTrustManager = Java.use('appcelerator.https.PinningTrustManager');
        PinningTrustManager.checkServerTrusted.implementation = function () {}
    } catch (err) {
        if (err.message.indexOf('ClassNotFoundException') === 0) {
            throw new Error(err);
        }
    }

    try {
        var TrustManagerImpl = Java.use('com.android.org.conscrypt.TrustManagerImpl');
        TrustManagerImpl.verifyChain.implementation = function (untrustedChain:any, trustAnchorChain:any, host:any, clientAuth:any, ocspData:any, tlsSctData:any) {
            return untrustedChain;
        }
    } catch (err) {
        if (err.message.indexOf('ClassNotFoundException') === 0) {
            throw new Error(err);
        }
    }

    try {
        var TrustManagerImpl = Java.use('com.android.org.conscrypt.TrustManagerImpl');
        TrustManagerImpl.checkTrustedRecursive.implementation = function (certs:any, host:any, clientAuth:any, untrustedChain:any, trustAnchorChain:any, used:any) {
            let ArrayList = Java.use("java.util.ArrayList");
            return ArrayList.$new();
        }
    } catch (err) {
        if (err.message.indexOf('ClassNotFoundException') === 0) {
            throw new Error(err);
        }
    }  

    try {
        var SSLCertificateChecker  = Java.use('nl.xservices.plugins.SSLCertificateChecker');
        SSLCertificateChecker.execute.overload("java.lang.String", "org.json.JSONArray", "org.apache.cordova.CallbackContext").implementation = function (str:any, jsonArray:any, callBackContext:any) {
            callBackContext.success("CONNECTION_SECURE");
            return true;
        }
    } catch (err) {
        if (err.message.indexOf('ClassNotFoundException') === 0) {
            throw new Error(err);
        }
    }   
}

export default hook_ssl_pinning;