# township - cpp

 - LDPlayer + Frida를 이용하여 구동 후 IDA tool을 이용하여 attach.
 - libgame.so 파일 분석하여 주요 함수에 대한 in/out 구현 및 확인.
 
## Analysis
- hash 함수들의 validation 체크 목적.

### Data Format (xml, json)
- xml - rapidxml
- json - jsoncpp

### Encrypt
- AES 128bit + IV (random; ts-id)
- 공개된 소스로 테스트시 결과가 상이하여 모두 구현.

### Compress
- gzip

### Hash
- 데이터의 첫 N byte에 따라 hash 방식이 상이함.
- network으로 데이터를 주고 받는 데이터 혹은 저장된 xml 파일들 역시 동일한 방식.
- Header 종류 : 0x54, 0x53, 0x78, 0x79, 0x64, 0x66, 0x6f, 0x1f8b(gzip), 0x45584c50, .....

