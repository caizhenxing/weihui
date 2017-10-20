import os

import jpype

project_path = os.path.abspath('..')

jvmPath = jpype.getDefaultJVMPath()

rsa_jar_path = project_path + os.path.sep +'Lib' + os.path.sep + 'RsaUtil.jar'
jvmArg = '-Djava.class.path=' + rsa_jar_path

dbopt_jar_path = project_path + os.path.sep +'Lib' + os.path.sep + 'DBOpt.jar'
db_jvm_arg = '-Djava.class.path=' + dbopt_jar_path

'''加签私钥'''
private_key = 'MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAO/6rPCvyCC+IMalLzTy3cVBz/+wamCFNiq9qKEilEBDTttP7Rd/GAS51lsfCrsISbg5td/w25+wulDfuMbjjlW9Afh0p7Jscmbo1skqIOIUPYfVQEL687B0EmJufMlljfu52b2efVAyWZF9QBG1vx/AJz1EVyfskMaYVqPiTesZAgMBAAECgYEAtVnkk0bjoArOTg/KquLWQRlJDFrPKP3CP25wHsU4749t6kJuU5FSH1Ao81d0Dn9m5neGQCOOdRFi23cV9gdFKYMhwPE6+nTAloxI3vb8K9NNMe0zcFksva9c9bUaMGH2p40szMoOpO6TrSHO9Hx4GJ6UfsUUqkFFlN76XprwE+ECQQD9rXwfbr9GKh9QMNvnwo9xxyVl4kI88iq0X6G4qVXo1Tv6/DBDJNkX1mbXKFYL5NOW1waZzR+Z/XcKWAmUT8J9AkEA8i0WT/ieNsF3IuFvrIYG4WUadbUqObcYP4Y7Vt836zggRbu0qvYiqAv92Leruaq3ZN1khxp6gZKl/OJHXc5xzQJACqr1AU1i9cxnrLOhS8m+xoYdaH9vUajNavBqmJ1mY3g0IYXhcbFm/72gbYPgundQ/pLkUCt0HMGv89tn67i+8QJBALV6UgkVnsIbkkKCOyRGv2syT3S7kOv1J+eamGcOGSJcSdrXwZiHoArcCZrYcIhOxOWB/m47ymfE1Dw/+QjzxlUCQCmnGFUO9zN862mKYjEkjDN65n1IUB9Fmc1msHkIZAQaQknmxmCIOHC75u4W0PGRyVzq8KkxpNBq62ICl7xmsPM='
'''加密公钥'''
encrypt_key = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDv0rdsn5FYPn0EjsCPqDyIsYRawNWGJDRHJBcdCldodjM5bpve+XYb4Rgm36F6iDjxDbEQbp/HhVPj0XgGlCRKpbluyJJt8ga5qkqIhWoOd/Cma1fCtviMUep21hIlg1ZFcWKgHQoGoNX7xMT8/0bEsldaKdwxOlv3qGxWfqNV5QIDAQAB'



'''
测试环境host
'''
# 10.65.209.181 pay.shbank.com
# 10.65.1.16 funcpay.sina.com.cn
# 222.73.39.37 func2pay.sina.com.cn func2pay.sina.com.cn
# 22.73.39.40 static.pay.sina.com.cn
# 10.65.1.19 merchant.pay.sina.com.cn www.weicaifu.com pay.sina.com.cn fcw.pay.sina.com.cn js.weibopay.com css.weibopay.com i1.weibopay.com i3.weibopay.com i4.weibopay.com www.wexmoney.com m.weibopay.com pay.xlubank.com mpay.xlubank.com
# 10.65.1.19 pay.weibopay.com mpay.sina.com.cn


