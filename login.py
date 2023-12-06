import hashlib
import requests
import time
import uuid
import urllib.parse

class xyw:
    @staticmethod
    def get_username():
        username = "  " #填入宽带账号
        return username

    @staticmethod
    def get_psw():
        psw = "  "  # 填入密码
        return psw


    @staticmethod
    def get_ip_address():
        # 把你自己的校园网获取到的url替换下面的url
        url = "http://125.XXX.XXX.XXX:10001/qs/main_gz.jsp?wlanacip=192.168.1.1&wlanuserip=192.168.1.1"  
        # 解析URL
        parsed_url = urllib.parse.urlparse(url)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        # 提取参数值
        wlanuserip = query_params.get('wlanuserip')[0]
        wlanacip = query_params.get('wlanacip')[0]
        return (wlanuserip,wlanacip)

    @staticmethod
    def post_json(url, data):
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return [response.status_code, response.json()]

    @staticmethod
    def get_mac_address():
        mac_address = uuid.getnode()
        # 格式化为标准MAC地址格式（XX:XX:XX:XX:XX:XX）
        mac_address = ':'.join(("%012X" % mac_address)[i:i+2] for i in range(0, 12, 2))
        return mac_address


    @staticmethod
    def get_verify_code(username, wlanuserip, wlanacip, mac):
        secret = "Eshore!@#"
        current_time = str(int(time.time()))
        version = "214"
        authenticator = version + wlanuserip + wlanacip + mac + current_time + secret
        authenticator = hashlib.md5(authenticator.encode()).hexdigest().upper()

        post_data = {
            'version': version,
            'username': username,
            'clientip': wlanuserip,
            'nasip': wlanacip,
            'mac': mac,
            'timestamp': current_time,
            'authenticator': authenticator,
            'iswifi': "4060"
        }

        url = "http://enet.10000.gd.cn:10001/client/vchallenge"
        verify_code = xyw.post_json(url, post_data)[1]

        if verify_code['rescode'] == "0":
            return verify_code['challenge']
        else:
            raise Exception("获取验证码出错！！！")

    @staticmethod
    def login(username, password, wlanuserip, wlanacip, mac, verificationcode):
        secret = "Eshore!@#"
        current_time = str(int(time.time()))
        authenticator = wlanuserip + wlanacip + mac + current_time + verificationcode + secret
        authenticator = hashlib.md5(authenticator.encode()).hexdigest().upper()

        post_data = {
            'username': username,
            'password': password,
            'clientip': wlanuserip,
            'nasip': wlanacip,
            'mac': mac,
            'timestamp': current_time,
            'authenticator': authenticator,
            'iswifi': "1050",
            'verificationcode': verificationcode
        }

        url = "http://125.88.59.131:10001/client/login"
        response = xyw.post_json(url, post_data)
        return response[1]

if __name__ == '__main__':
    app = xyw()
    username = app.get_username()
    password = app.get_psw()
    result = app.get_ip_address()
    wlanuserip = result[0]
    wlanacip = result[1]
    mac = app.get_mac_address()

    # 获取验证码
    verifycode = app.get_verify_code(username, wlanuserip, wlanacip, mac)

    # 登录账号
    result = app.login(username, password, wlanuserip, wlanacip, mac, verifycode)

    # 输出结果
    print(result)
