import os, time
import socket


# 往csv文件中写入测试结果
def write_report(case, result):
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    with open(r'../report/report.csv', mode='a+', encoding='utf-8') as file:
        file.write('%s,%s,%s\n' % (now, case, result))

# 连接服务端口判断服务有没有开启
def check_port(ip, port):
    s = socket.socket()
    try:
        s.connect((ip, port))
        return True
    except:
        return False
    finally:
        s.close()


if __name__ == '__main__':
    check_port('127.0.0.1', 3306)
