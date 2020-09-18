# __author__ = "zok" 362416272@qq.com
# Date: 2020/7/24 Python:3.7

import pyDes
import base64


class TripleDesUtils:

    def encryption(self, data: str, key, iv) -> str:
        """3des 加密
        """
        _encryption_result = pyDes.triple_des(key, pyDes.CBC, iv, None, pyDes.PAD_PKCS5).encrypt(data)
        _encryption_result = self._base64encode(_encryption_result).decode()
        return _encryption_result

    def decrypt(self, data: str, key, iv) -> str:
        """3des 解密
        """
        data = self._base64decode(data)
        _decrypt_result = pyDes.triple_des(key, pyDes.CBC, iv, None, pyDes.PAD_PKCS5).decrypt(data).decode('utf-8')
        return _decrypt_result

    @staticmethod
    def _base64encode(data):
        try:
            _b64encode_result = base64.b64encode(data)
        except Exception as e:
            raise Exception(f"base64 encode error:{e}")
        return _b64encode_result

    @staticmethod
    def _base64decode(data):
        try:
            _b64decode_result = base64.b64decode(data)
        except Exception as e:
            raise Exception(f"base64 decode error:{e}")
        return _b64decode_result


des3 = TripleDesUtils()


if __name__ == "__main__":
    _test_data = '1595553133358'
    _key = 'fmgKRc4aLmgTbXzcm9PNziI8'
    _iv = '20200724'
    result = des3.encryption(_test_data, _key, _iv)
    print(f"加密结果: {result}")

    _test_data = 'i3yR3q4MM2QlrgJFeLLl/3ZCQaHyaqoj+zTmV4hJ1Aj8Z5xeSNHNb/QI7OkcxoKr/g6jPqcG94BonJ2viz6MUqhheutFlzRYNPx/YhNwvNuMmEjRn8C8uOwUvbgMzqLWcJK8v12xhIqNW2gMrZdQep1o8OhYnA2xvS0VCLiYh4sJwBaSWgNoihDqWTwf6WS/PdCjCYiRy1OKpV1aglLe9zHlLt1aycQrldWJngnsAVCuhS8kQ9bDYdKMskDKd6TOWDRnQlKIqwu8kyJzUYMqQcp50eXFiOlIT6UwgKsj5a1JgLh3Q2aisEVuPXN+e5CDbeUFG9IQtLCLAFJXGmn8i3Ec1AgThc1UFJwRkG0F0GIfqyEZG+g0imiTZL/M0ddPzmfkzBD2jCCi1l8Xlw5r14cyrTFzaZNq1UHOMATYQlydgQ5EoBvf8JDkXFmH2hKTeFmYjY92MDPcYnfK9mFnPNWdesfk2k9D27E8U8X/chxz5UT1G0X0QQ=='
    _key = 'hsL5n2Xgk7aVR8F5DcAk4MCk'
    _iv = '20200825'
    result2 = des3.decrypt(_test_data, _key, _iv)
    print(f"解密结果: {result2}")

