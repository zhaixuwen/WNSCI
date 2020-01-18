import os, time
from common import utility
from tests import login
import configparser


class WoniuSalesCI:
    def __init__(self):
        config = configparser.ConfigParser()
        filename = '../config/config.ini'
        config.read(filename, encoding='utf-8')
        # svn目录路径
        self.svn_path = config.get('svn', 'svn_path')
        # svn目录下ant打包文件路径
        self.svn_build_path = config.get('svn', 'svn_build_path')
        # svn服务器地址
        self.svn_service_address = config.get('svn', 'svn_service_address')
        # svn用户名
        self.svn_username = config.get('svn', 'svn_username')
        # svn密码
        self.svn_password = config.get('svn', 'svn_password')
        # tomcat服务器地址
        self.tomcat_address = config.get('tomcat', 'tomcat_address')
        # tomcat服务端口
        self.tomcat_port = config.getint('tomcat', 'tomcat_port')
        # tomcat startup.bat文件路径
        self.tomcat_startup_path = config.get('tomcat', 'tomcat_startup_path')
        # tomcat shutown.bat文件路径
        self.tomcat_shutdown_path = config.get('tomcat', 'tomcat_shutdown_path')
        # tomcat webapps目录路径
        self.tomcat_webapps_path = config.get('tomcat', 'tomcat_webapps_path')

    def svn(self):
        # 判断svn目录是否存在
        if os.path.exists(self.svn_path) and os.path.exists(self.svn_build_path):
            # 若代码库已存在update
            os.system('svn update %s' % self.svn_path)
            print('svn代码update成功。')
        else:
            # 代码库不存在则checkout
            os.system(f'svn checkout {self.svn_service_address} {self.svn_path} --username {self.svn_username} --password {self.svn_password}')
            print('svn代码checkout成功。')

    # 调用ant -f build.xml命令对当前项目进行构建，生成war包，用于tomcat部署
    def build(self):
        os.system('ant -f %s' % self.svn_build_path)
        print('ant打包成功。')
        time.sleep(5)

    # 部署到tomcat上，并启动tomcat运行
    def deploy(self):
        # 判断tomcat服务状态，如果没启动则启动
        if not utility.check_port(self.tomcat_address, self.tomcat_port):
            os.system(self.tomcat_startup_path)
        # 删除老的war包和目录，复制新war包到webapps下
        os.system('del /F /Q %s' % self.tomcat_webapps_path + '\woniusales.war')
        os.system('rd /S /Q %s' % self.tomcat_webapps_path + '\woniusales')
        os.system('copy %s %s' % (self.svn_path+"\woniusales.war", self.tomcat_webapps_path))
        print('替换war包成功。')
        time.sleep(10)

    # 修改服务器配置文件
    def config(self):
        content = 'db_url=jdbc:mysql://localhost:3306/woniusales?useUnicode=true&characterEncoding=utf8\n'
        content += 'db_username=root\n'
        content += 'db_password=\n'
        content += 'db_driver=com.mysql.jdbc.Driver'
        with open(f"{self.tomcat_webapps_path}+r'\woniusales\WEB-INF\classes\db.properties'", mode='w') as file:
            file.write(content)
        print('修改配置文件成功。')
        time.sleep(10)

    # 重启tomcat服务：tomcat启动时会打开另一个进程，当前脚本不会等待它启动完成
    def tomcat(self):
        if utility.check_port(self.tomcat_address, self.tomcat_port):
            os.system(self.tomcat_shutdown_path)
        time.sleep(10)
        # 检查mysql状态后再起tomcat服务
        # if not common.check_port('127.0.0.1', 3306):
        #     pass
        os.system(self.tomcat_startup_path)
        time.sleep(20)
        print('tomcat已启动完成.')

    # 运行测试脚本
    def test(self):
        login.test_login_gui()
        login.test_login_http()
        print('测试脚本运行完成。')

    # 右键发送测试报告
    def email(self):
        pass

    # 生成html报告
    def html(self):
        with open(r'../report/report.csv', mode='r') as file:
            result_list = file.readlines()
        content = "<html>\n<head>\n<meta charset='utf-8'>\n</head>\n"
        content += '<body>\n<table border="1px" align="center" >\n<tr>\n<td>测试时间</td>\n<td>测试名称</td>\n<td>测试结果</td>\n</tr>\n'
        for result in result_list:
            test_time = result.split(',')[0]
            test_name = result.split(',')[1]
            test_result = result.split(',')[2]
            content += f'<tr>\n<td>{test_time}</td>\n<td>{test_name}</td>\n<td>{test_result}</td>\n</tr>\n'
        content +='</table>\n</body>\n</html>'
        with open('../report/report.html', mode='w') as file:
            file.write(content)


if __name__ == '__main__':
    ci = WoniuSalesCI()
    ci.svn()
    ci.build()
    ci.deploy()
    ci.config()
    ci.tomcat()
    ci.test()
    ci.email()
    ci.html()