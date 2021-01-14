# township

playrix사 의 [township](https://www.playrix.com/township/) 분석

## Analysis
- 초기 서버로부터 game data를 요청 다운 받음.
- 주기적으로 thread로 돌면서 로컬 데이터를 서버로 전송 함.
   - 이때 간헐적 freezing 현상이 생김.

- 자체 게임엔진을 사용하는 것으로 보이며, C++, Boost, RapidXML 라이브러리를 사용함.


## Tools

Android (Emulator) Tools
- [LDPlayer](https://kr.ldplayer.net/)
- [APK Download](https://www.apkmirror.com/apk/playrix/township/township-7-8-6-release/#downloads)


Reverse Tools
- [IDA pro 7.0 (Hex-Rays)](https://www.hex-rays.com/products/ida/)
- [Frida](https://frida.re/)


Develop Tools
- [Visual Studio Code](https://code.visualstudio.com/)
- [Ubuntu 18.04](https://releases.ubuntu.com/18.04/) / g++ 7.5.0

## Logic

### Game data Logic
 - [Encoding/Decoding (Test 용도) ](parsing_encoded_xml/)
 - [frida-src (분석용)](frida/)
 - [cpp-src (분석용)](township/)
 - [python-src (web viewer)](py_township/)

----

TBA