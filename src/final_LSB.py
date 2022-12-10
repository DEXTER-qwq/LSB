#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import datetime
import cv2
import numpy as np
from PIL import Image
import gmpy2
from gmpy2 import mpz
import binascii


# LSB
def to_asc(strr):
    # 转二进制
    return int(strr, 2)


# str1为所要提取的信息的长度（根据需要修改），str2为加密载体图片的路径，str3为提取文件的保存路径
def decode(str1, str2, str3):
    b = ""
    im = Image.open(str2)
    lenth = int(str1) * 8
    width, height = im.size[0], im.size[1]
    count = 0
    for h in range(height):
        for w in range(width):
            # 获得(w,h)点像素的值
            pixel = im.getpixel((w, h))
            # 此处mod3，依次从R、G、B三个颜色通道获得最低位的隐藏信息
            if count % 3 == 0:
                count += 1
                b = b + str((mod(int(pixel[0]), 2)))
                if count == lenth:
                    break
            if count % 3 == 1:
                count += 1
                b = b + str((mod(int(pixel[1]), 2)))
                if count == lenth:
                    break
            if count % 3 == 2:
                count += 1
                b = b + str((mod(int(pixel[2]), 2)))
                if count == lenth:
                    break
        if count == lenth:
            break

    with open(str3, "w", encoding='utf-8') as f:
        for i in range(0, len(b), 8):
            # 以每8位为一组二进制，转换为十进制
            stra = to_asc(b[i:i + 8])
            # 将转换后的十进制数视为ascii码，再转换为字符串写入到文件中
            # print((stra))
            f.write(chr(stra))
    print("sussess")


def plus(string):
    # Python zfill() 方法返回指定长度的字符串，原字符串右对齐，前面填充0。
    # 填充为8位二进制
    return string.zfill(8)


def get_key(strr):
    # 获取要隐藏的文件内容
    with open(strr, "rb") as f:
        s = f.read().decode("utf-8")
        return s


def mod(x, y):
    return x % y


# str1为载体图片路径，str2为隐写字符串，str3为加密图片保存的路径
def encode(str1, key, str3):
    im = Image.open(str1)
    # 获取图片的宽和高
    width, height = im.size[0], im.size[1]
    print("width:" + str(width))
    print("height:" + str(height))
    count = 0
    # 获取需要隐藏的信息
    keylen = len(key)
    for h in range(height):
        for w in range(width):
            pixel = im.getpixel((w, h))
            a = pixel[0]
            b = pixel[1]
            c = pixel[2]
            if count == keylen:
                break
            # 下面的操作是将信息隐藏进去
            # 分别将每个像素点的RGB值mod2，这样可以去掉最低位的值
            # 再从需要隐藏的信息中取出一位，转换为整型
            # 两值相加，就把信息隐藏起来了
            a = a - mod(a, 2) + int(key[count])
            count += 1
            if count == keylen:
                im.putpixel((w, h), (a, b, c))
                break
            b = b - mod(b, 2) + int(key[count])
            count += 1
            if count == keylen:
                im.putpixel((w, h), (a, b, c))
                break
            c = c - mod(c, 2) + int(key[count])
            count += 1
            if count == keylen:
                im.putpixel((w, h), (a, b, c))
                break
            if count % 3 == 0:
                im.putpixel((w, h), (a, b, c))
    im.save(str3)
    return width, height


# 混乱

'''
加密:
    -key: 密钥
    -imgpath: 待加密图像路径
    -start: 将生成的混沌序列，从第start个之后开始作为加密用序列
'''


def encryption(key, imgpath, start=500, x0=0.1):
    if key > 4 or key < 3.57:
        print('[Error]: Key must between <3.57-4>...')
        return None
    if x0 >= 1 or x0 <= 0:
        print('[Error]: x0 must between <0-1>...')
        return None
    img = Image.open(imgpath)
    img_en = Image.new(mode=img.mode, size=img.size)
    width, height = img.size
    chaos_seq = np.zeros(width * height)
    for _ in range(start):
        x = key * x0 * (1 - x0)
        x0 = x
    for i in range(width * height):
        x = key * x0 * (1 - x0)
        x0 = x
        chaos_seq[i] = x
    idxs_en = np.argsort(chaos_seq)
    i, j = 0, 0
    for idx in idxs_en:
        col = int(idx % width)
        row = int(idx // width)
        img_en.putpixel((i, j), img.getpixel((col, row)))
        i += 1
        if i >= width:
            j += 1
            i = 0
    img_en.save('encryption.%s' % imgpath.split('.')[-1], quality=100)


'''
解密:
    -key: 密钥
    -imgpath: 待解密图像路径
    -start: 将生成的混沌序列，从第start个之后开始作为解密用序列
'''


def decryption(key, imgpath, start=500, x0=0.1):
    if key > 4 or key < 3.57:
        print('[Error]: Key must between <3.57-4>...')
        return None
    if x0 >= 1 or x0 <= 0:
        print('[Error]: x0 must between <0-1>...')
        return None
    img = Image.open(imgpath)
    img_de = Image.new(img.mode, img.size)
    width, height = img.size
    chaos_seq = np.zeros(width * height)
    for _ in range(start):
        x = key * x0 * (1 - x0)
        x0 = x
    for i in range(width * height):
        x = key * x0 * (1 - x0)
        x0 = x
        chaos_seq[i] = x
    idxs_de = np.argsort(chaos_seq)
    i, j = 0, 0
    for idx in idxs_de:
        col = int(idx % width)
        row = int(idx // width)
        img_de.putpixel((col, row), img.getpixel((i, j)))
        i += 1
        if i >= width:
            j += 1
            i = 0
    img_de.save('decryption.%s' % imgpath.split('.')[-1], quality=100)


# RSA

def gen_prime(rs):
    # 生成二进制位数为1024的随机素数
    p = gmpy2.mpz_urandomb(rs, 1024)
    # print(p)
    while not gmpy2.is_prime(p):
        p = p + 1
    return p


def gen_key():
    # 生成密钥
    rs = gmpy2.random_state(datetime.datetime.now().microsecond)
    p = gen_prime(rs)
    q = gen_prime(rs)
    return p, q


def encrypt(e, n, message):
    # 将输入消息转换成16进制数字并加密，支持utf-8字符串
    M = mpz(binascii.hexlify(message.encode('utf-8')), 16)
    C = gmpy2.powmod(M, e, n)
    return C


def decrypt(d, n, C):
    # 对输入的密文进行解密并解码
    M = gmpy2.powmod(C, d, n)
    return binascii.unhexlify(format(M, 'x')).decode('utf-8')


def rsa_init():
    p, q = gen_key()
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = gmpy2.invert(e, phi)
    return e, d, n


def show_lsb(input_img, input_msg, key):
    img = cv2.imread(input_img, 1)  # 读取原始图像
    cv2.imshow("img", img)  # 显示原图

    encryption(key, input_img)  # 保存混乱加密
    img = cv2.imread("encryption.bmp", 1)
    cv2.imshow("EncryptionImg", img)  # 显示

    msg = get_key(input_msg)
    e, d, n = rsa_init()
    C = encrypt(e, n, msg)
    # 字符串转换为相应的二进制串
    string = ""
    for i in range(len(C.__str__())):
        string = string + "" + plus(bin(ord(C.__str__()[i])).replace('0b', ''))
    # LSB隐写
    width, height = encode("encryption.bmp", string, "lenaLsb.bmp")
    img = cv2.imread("lenaLsb.bmp", 1)  # 读取加密图像
    cv2.imshow("lsbEncryption ", img)  # 显示

    decryption(key, "lenaLsb.bmp")  # 保存混乱解密
    img = cv2.imread("decryption.bmp", 1)
    cv2.imshow("DecryptionImg ", img)  # 显示
    img1 = cv2.imread("Lenna.bmp", 1)  # 读取原始图像
    img2 = cv2.imread("decryption.bmp", 1)  # 读取lsb混乱图像
    sub = img1 - img2
    cv2.imshow("subtracted ", sub)  # 显示

    cv2.waitKey(0)
    return e, d, n, C


def decode_show(input_img, key):
    img = cv2.imread(input_img, 1)  # 读取解密图像
    cv2.imshow("decryption", img)  # 显示原图

    encryption(key, input_img)  # 保存混乱加密
    img = cv2.imread("encryption.bmp", 1)
    cv2.imshow("en_decryption", img)  # 显示

    im = Image.open("encryption.bmp")
    width, height = im.size[0], im.size[1]
    decode(width * height, "encryption.bmp", "output.txt")  # 读取隐藏信息
    cv2.waitKey(0)
    with open('output.txt', 'r') as f:
        line = f.readline()
    return line


if __name__ == "__main__":
    # show_lsb("Lenna.bmp", "flag.txt", 3.58)
    # e, d, n, C = encode_show("Lenna.bmp", "flag.txt", 3.58)
    # decode_show("lenaLsb.bmp","Lenna.bmp", d, n, C, 3.58)  # 保存混乱解密
    e, d, n, C = show_lsb("D:/python/LSB/Lenna.bmp", "flag.txt", 3.58)
    # e, d, n, C = show_lsb("D:/python/LSB/Lenna.bmp", "flag.txt", 3.59)
    line = decode_show("decryption.bmp", 3.58)
    # print(decrypt(d, n, C))
    # print(C)
    # print(line)
