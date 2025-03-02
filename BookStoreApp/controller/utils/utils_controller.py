import json
import os
import random
import smtplib

from BookStoreApp import app


# Đọc dữ liệu từ file json
def get_data_json_file(filename):
    if filename:
        with open(os.path.join(app.root_path, 'data/{}'.format(filename)),
                  encoding='utf-8') as f:
            return json.load(f)


# Ghi dữ liệu xuống file json
def set_data_json_file(filename, data):
    if filename:
        with open(os.path.join(app.root_path, 'data/{}'.format(filename)), 'w',
                  encoding='utf-8') as f:
            return json.dump(data, f, ensure_ascii=True, indent=4)


# Mã hóa bằng thuật toán vigenere
def encode_vigenere(plain_text):
    # Lấy số nhỏ nhất và lớn nhất có 10 chữ số
    beg_num = '1'
    end_num = ''
    for x in range(1, 11):
        if len(beg_num) < 10:
            beg_num += '0'
        end_num += '9'

    # Chuyển đổi số đầu vào thành 1 số khác
    secret_number = random.randint(int(beg_num) - plain_text, int(end_num) - plain_text)
    secret_data = str(plain_text + secret_number)

    # data source
    data_source = []
    for dt in range(65, 91):
        data_source.append(chr(dt))
        data_source.append(chr(dt + 32))

    # tạo key
    first_key = ''
    second_key = ''
    key_index = random.randint(0, len(data_source) - 10)
    key_source = [x for x in data_source[key_index:key_index + 10]]
    random.shuffle(key_source)
    for key in key_source:
        first_key += str(key)
    random.shuffle(key_source)
    for key in key_source:
        second_key += str(key)

    # Tạo map pivot
    map_pivot = [x for x in first_key]
    for dt in data_source:
        if not map_pivot.__contains__(dt):
            map_pivot.append(dt)

    # Tạo bảng ánh xạ
    map_table = []
    map_pivot_temp = [x for x in map_pivot]
    for r in range(0, len(data_source)):
        map_table.append([map_pivot_temp[c] for c in range(0, len(data_source))])
        map_pivot_temp.append(map_pivot_temp.pop(0))

    # Ánh xạ và tiến hành mã hóa
    pivot = 0
    cipher_data = ''
    for sd in secret_data:
        sd = chr(ord(sd) + (17 if pivot % 2 == 0 else 49))
        row_idx = map_pivot.index(second_key[pivot % len(second_key)])
        col_idx = map_pivot.index(sd)
        cipher_data += str(map_table[row_idx][col_idx])
        pivot += 1

    # chuyển đổi secret number
    secret_number_convert = ''
    secret_number = str(secret_number)
    for sn in secret_number:
        secret_number_convert += chr(ord(sn) + (17 if secret_number.index(sn) % 2 == 0 else 49))

    return '{first_key}{cipher_data}{second_key}{secret_number}' \
        .format(first_key=first_key,
                cipher_data=cipher_data,
                second_key=second_key,
                secret_number=secret_number_convert)


# Giải mã bằng thuật toán Vigenere
def decode_vigenere(cipher_text):
    # Tách dữ liệu mã hóa
    first_key = cipher_text[:10]
    cipher_data = cipher_text[10:20]
    second_key = cipher_text[20:30]
    secret_number = cipher_text[30:]

    # chuyển đổi secret number
    secret_number_convert = ''
    for sn in secret_number:
        secret_number_convert += chr(ord(sn) - (17 if secret_number.index(sn) % 2 == 0 else 49))
    secret_number = int(secret_number_convert)

    # data source
    data_source = []
    for dt in range(65, 91):
        data_source.append(chr(dt))
        data_source.append(chr(dt + 32))

    # Tạo map pivot
    map_pivot = [x for x in first_key]
    for dt in data_source:
        if not map_pivot.__contains__(dt):
            map_pivot.append(dt)

    # Tạo bảng ánh xạ
    map_table = []
    map_pivot_temp = [x for x in map_pivot]
    for r in range(0, len(data_source)):
        map_table.append([map_pivot_temp[c] for c in range(0, len(data_source))])
        map_pivot_temp.append(map_pivot_temp.pop(0))

    # Ánh xạ và giải mã
    secret_data = ''
    pivot = 0
    for c in cipher_data:
        row_idx = map_pivot.index(second_key[pivot % len(second_key)])
        sd = map_pivot[map_table[row_idx].index(c)]
        secret_data += chr(ord(sd) - (17 if pivot % 2 == 0 else 49))
        pivot += 1

    plain_text = int(secret_data) - secret_number

    return plain_text


