import io
import os

from django.conf import settings

from app_root.contents.utils import load_all_products_xml, create_township_version, load_all_material_xml, \
    load_all_building_xml
from app_root.gameinfos.models import Account
from app_root.keywords.models import Keyword
from app_root.keywords.utils import decode_keyword
from core.utils import hash10
from modules.ts_file import ts_decode_file

"""
    7.9.0
    Program Headers:
        Type           Offset       VirtAddr    PhysAddr    FileSiz     MemSiz      Flg     Align
        PHDR           0x000034     0x00000034  0x00000034  0x00100     0x00100     R       0x4
        LOAD           0x000000     0x00000000  0x00000000  0x2f9cf68   0x2f9cf68   R E     0x1000
        GNU_EH_FRAME   0x2ec19d4    0x02ec19d4  0x02ec19d4  0xdb594     0xdb594     R       0x4
        LOAD           0x2f9dda0    0x02f9eda0  0x02f9eda0  0x150540    0x191788    RW      0x1000
        DYNAMIC        0x30e6c4c    0x030e7c4c  0x030e7c4c  0x00140     0x00140     RW      0x4
        NOTE           0x000134     0x00000134  0x00000134  0x000bc     0x000bc     R       0x4
        GNU_STACK      0x000000     0x00000000  0x00000000  0x00000     0x00000     RW      0x10
        GNU_RELRO      0x2f9dda0    0x02f9eda0  0x02f9eda0  0x14b260    0x14b260    RW      0x8
    7.9.5    
        Type           Offset       VirtAddr    PhysAddr    FileSiz     MemSiz      Flg     Align
        PHDR           0x000034     0x00000034  0x00000034  0x00100     0x00100     R       0x4
        LOAD           0x000000     0x00000000  0x00000000  0x3063d2c   0x3063d2c   R E     0x1000
        LOAD           0x3064660    0x03065660  0x03065660  0x155c60    0x197108    RW      0x1000
        DYNAMIC        0x31b2c7c    0x031b3c7c  0x031b3c7c  0x00138     0x00138     RW      0x4
        NOTE           0x000134     0x00000134  0x00000134  0x000bc     0x000bc     R       0x4
        GNU_EH_FRAME   0x2f85d08    0x02f85d08  0x02f85d08  0xde024     0xde024     R       0x4
        GNU_STACK      0x000000     0x00000000  0x00000000  0x00000     0x00000     RW      0x10
        GNU_RELRO      0x3064660    0x03065660  0x03065660  0x1509a0    0x1509a0    RW      0x8

"""
mapping_7_9_0 = [
    (0x2f9dda0, 0x02f9eda0, 0x150540),
    (0x30e6c4c, 0x030e7c4c, 0x00140),
]
mapping_7_9_5 = [
    (0x3064660, 0x03065660, 0x155c60),
    (0x31b2c7c, 0x031b3c7c, 0x00138),
]
mapping = mapping_7_9_5


def generate_predefined_keywords():
    from app_root.keywords.offset_info import offsets_7_9_5 as offsets

    path = settings.EXTERNAL_DIR / "lib" / settings.TS_APP_VERSION / "libgame.so"

    bulk_list = []
    with open(path, "rb") as fin :
        for (offset, length) in offsets:

            adjust_offset = offset
            for (o, v, s) in mapping:
                if v <= offset <= v + s:
                    adjust_offset -= v-o
                    break

            fin.seek(adjust_offset, io.SEEK_SET)
            data = fin.read(length + 1)

            keyword = decode_keyword(data)

            hex_string = data.hex()

            if not Keyword.objects.with_encoded_keyword(hex_string).exists():
                # print("data : {} / keyword : {}".format(data, keyword))

                bulk_list.append(
                    Keyword(
                        address=adjust_offset,
                        encoded_hex_string=hex_string,
                        encoded_hash=hash10(hex_string),
                        decoded_string=keyword,
                        decoded_hash=hash10(keyword)
                    )
                )

    if bulk_list:
        Keyword.objects.bulk_create(
            bulk_list
        )


def generate_AES_data():

    in_path = settings.EXTERNAL_DIR / "lib" / settings.TS_APP_VERSION / "libgame.so"
    out_path = settings.EXTERNAL_DIR / "lib" / settings.TS_APP_VERSION / "aes_data.py"

    offset_info_7_9_0 = {
        'T' : {'offset': 0x02A0566C, 'size': 64},
        'T1': {'offset': 0x02A0A4F8, 'size': 1024},
        'Tb1': {'offset': 0x02A0A4FB, 'size': 1024},
        'T2': {'offset': 0x02A0A8F8, 'size': 1024},
        'Tb2': {'offset': 0x02A0A8FA, 'size': 1024},
        'T3': {'offset': 0x02A0ACF8, 'size': 1024},
        'Tb3': {'offset': 0x02A0ACF9, 'size': 1024},
        'T4': {'offset': 0x02A0B0F8, 'size': 1024},
        'Rc': {'offset': 0x02A0B4F8, 'size': 40},
    }

    offset_info_7_9_5 = {
        'T' : {'offset': 0x02ABB3B8, 'size': 64},
        'T1': {'offset': 0x02AC0248, 'size': 1024},
        'Tb1': {'offset': 0x02AC024B, 'size': 1024},
        'T2': {'offset': 0x02AC0648, 'size': 1024},
        'Tb2': {'offset': 0x02AC064A, 'size': 1024},
        'T3': {'offset': 0x02AC0A48, 'size': 1024},
        'Tb3': {'offset': 0x02AC0A49, 'size': 1024},
        'T4': {'offset': 0x02AC0E48, 'size': 1024},
        'Rc': {'offset': 0x02AC1248, 'size': 40},
    }
    offset_info = offset_info_7_9_5

    chunk_size = 116

    with open(in_path, "rb") as fin, open(out_path, "wt") as fout:
        fout.write("""from struct import unpack
from typing import List


def _(a: str) -> List[int]:
    barr = bytes.fromhex(''.join([_.strip() for _ in a if _.strip()]))
    return list(unpack('I' * (len(barr) // 4), barr))
""")
        for name in offset_info:
            offset = offset_info[name]['offset']
            size = offset_info[name]['size']

            for (o, v, s) in mapping:
                if v <= offset <= v + s:
                    offset -= v-o
                    break

            fin.seek(offset, io.SEEK_SET)
            data = fin.read(size)

            fout.write('\n\n# {0:s} / offset=0x{1:08x} ({1:d}) / length = 0x{2:08x} ({2:d})\n'.format(
                name, offset, size
            ))
            txt = ''.join(['{:02x}'.format(_) for _ in data ])
            fout.write('{0:s}: List[int] = _("""'.format(name))
            for i in range(0, size*2, chunk_size):
                fout.write('\n    ')
                fout.write(txt[i:i+chunk_size])
            fout.write('\n""")\n')


def _convert_contents(from_path, to_path):

    if not to_path.exists():
        to_path.mkdir(mode=0o755, parents=True, exist_ok=True)

    for file in from_path.glob('*'):
        out_file = to_path / file.name

        if file.is_dir():
            _convert_contents(from_path = file, to_path = out_file)
        else:
            if out_file.exists():
                continue

            try:
                ts_decode_file(file, out_file)
            except:
                out_file.write_bytes(
                    file.read_bytes()
                )

def load_contents():
    base_path = settings.WORK_DIR / "base" / settings.TS_APP_VERSION

    from_path = settings.EXTERNAL_DIR / "base" / settings.TS_APP_VERSION
    _convert_contents(from_path=from_path, to_path=base_path)

    version = create_township_version()

    load_all_products_xml(version=version, base_path=base_path)
    load_all_material_xml(version=version, base_path=base_path)
    load_all_building_xml(version=version, base_path=base_path)


def generate_account():
    for data in settings.ACCOUNTS:
        if not Account.objects.filter(city_id=data.get('city_id')).exists():
            Account.objects.create(**data)


def run():
    print("1. generate predefined keywords")
    generate_predefined_keywords()

    print("2. generate AES table")
    generate_AES_data()

    print("3. load township contents from package")
    load_contents()

    print("4. generate account info")
    generate_account()

    print("complete.")
