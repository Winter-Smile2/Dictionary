"""
dict 客户端

功能: 发起请求,接收结果
"""

from socket import *
import sys
import getpass

# 服务器地址
ADDR = ('127.0.0.1',8888)

# 注册功能
def do_register(s):
    while True:
        name = input("User:")
        pwd = getpass.getpass("Pwd:")
        pwd1 = getpass.getpass("Again:")
        if pwd != pwd1:
            print("两次密码不一致！")
            continue
        if (' ' in name) or (' ' in pwd):
            print("用户名或密码不能含有空格")
            continue

        msg = "R %s %s"%(name,pwd)
        s.send(msg.encode()) # 发送请求
        data = s.recv(128).decode() # 反馈
        if data == 'OK':
            print("注册成功")
        else:
            print("注册失败")
        return

# 登录功能
def do_login(s):
    name = input("User:")
    pwd = getpass.getpass("Password")
    msg = "L " + name + " " + pwd
    s.send(msg.encode())
    data = s.recv(128).decode() # 得到反馈
    if data == 'OK':
        print("登陆成功")
        login(s,name)
    else:
        print("登录失败")


def do_query(s,name):
    while True:
        word = input("请输入查找的单词")
        if word == "##":
            break
        msg = "Q " + word + " " + name
        s.send(msg.encode())
        data = s.recv(1024).decode()
        print(data)


def do_history(s, name):
    msg = "H "+name
    s.send(msg.encode())
    while True:
        data = s.recv(1024).decode()
        if data == '##':
            break
        print(data)


def login(s,name):
    while True:
        print("""
        ==========%s Query ============
          1.查单词     2.历史记录     3.注销
        ===============================
        """%name)
        cmd = input("选项(1,2,3):")
        if cmd == '1':
            do_query(s,name)
        elif cmd == '2':
            do_history(s,name)
        elif cmd == '3':
            break
# 搭建网络
def main():
    s = socket()
    s.connect(ADDR)
    while True:
        print("""
        ========== Welcome ============
          1.注册     2.登录     3.退出
        ===============================
        """)
        cmd = input("选项(1,2,3):")
        if cmd == '1':
            do_register(s)
        elif cmd == '2':
            do_login(s)
        elif cmd == '3':
            s.send(b'E')
            sys.exit("谢谢使用")

if __name__ == '__main__':
    main()







