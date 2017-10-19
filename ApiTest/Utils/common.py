import random
import string

import time

from Utils.config import jvmArg, jvmPath, private_key, encrypt_key
from Utils.exception import ParamsError
import jpype
'''
生成随机字符串 指定长度 一般用于接口相关单号生成，如标的号
'''
def gen_random_string(str_len):
    return ''.join(
        random.choice(string.ascii_letters + string.digits) for _ in range(str_len))
'''
得到当前请求时间，默认YYMMDDHHMMSS模式，一般用于生成接口请求时间和订单号 长度从0至14
'''
def get_now_time(str_len = 14):
    if isinstance(str_len, int) and 0 < str_len < 15:
        return time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))[0:str_len]
    raise ParamsError("timestamp length can only between 0 and 14.")

'''
延时设置
'''
def sleep(sleep_second = 0):
    time.sleep(sleep_second)

'''
列表转字符串
'''
def list_to_dict(exp_list):
    change_dict = {}
    if exp_list is None:
        raise ParamsError("%s is must hava values!" % exp_list)
    else:
        for value in exp_list:
            for key, data in value.items():
                change_dict.setdefault(key, data)
    return change_dict


'''
返回加签机密后接口请求报文
'''
def get_request_msg(case_data):
    sign_string = list_to_dict(case_data.get("basic_data"))
    sign_string.update(list_to_dict(case_data.get("unique_data")))

    encrypt_data = {}
    if "encrypt_data"in case_data.keys():
        encrypt_data = list_to_dict(case_data.get("encrypt_data"))

    if encrypt_data is not None:
        encrypt_data = encrypt_rsa(encrypt_data)
        for key, value in encrypt_data.items():
            sign_string[key] = value  # 添加加密后的key-value
            encrypt_data[key] = encode(value)  # encode

    sign_type = sign_string.pop('sign_type')
    sign_version = sign_string.pop('sign_version')

    list_string = sorted(sign_string)#排序

    input_string = ''
    for key in list_string:
        key_value = key+'='+sign_string.get(key) + '&'
        input_string = input_string + key_value
    input_string = input_string[0:len(input_string)-1]#去掉最后一个&
    sign = get_sign_rsa(input_string)#得到sign rsa
    sign = encode(sign)

    sign_string['sign_type'] = sign_type
    sign_string['sign_version'] = sign_version

    if encrypt_data is not None:  # 加密字段不为空
        for key, value in encrypt_data.items():
            sign_string[key] = value


    #其他需要encode的参数
    try:
        notify_url = encode(sign_string['notify_url'])
        return_url = encode(sign_string['return_url'])
        sign_string['notify_url'] = notify_url
        sign_string['return_url'] = return_url
    except ParamsError():
        pass

    sign_string['sign'] = sign
    return sign_string




'''RSA加签'''
def get_sign_rsa(input_string):
    if not jpype.isJVMStarted():
        jpype.startJVM(jvmPath, jvmArg)
    RSAUtil = jpype.JClass('com.common.RSAUtil')
    rsa = RSAUtil()
    rsa.setPrivateKey(private_key);
    sign = rsa.sign(input_string)
    return sign

'''明文信息加密'''
def encrypt_rsa(dict):
    if not jpype.isJVMStarted():
        jpype.startJVM(jvmPath, jvmArg)
    RSAUtil = jpype.JClass('com.common.RSAUtil')
    rsa = RSAUtil()
    encrypt_dict = {}
    for key,value in dict.items():
        encrypt_dict.setdefault(key, rsa.encrypt(value, encrypt_key))
    return encrypt_dict

'''解码'''
def decode(text):
    if not jpype.isJVMStarted():
        jpype.startJVM(jvmPath, jvmArg)
    text = jpype.java.net.URLDecoder.decode(text, "UTF-8");
    return text
'''编码'''
def encode(text):
    if not jpype.isJVMStarted():
        jpype.startJVM(jvmPath, jvmArg)
    text = jpype.java.net.URLEncoder.encode(text, "UTF-8");
    return text

