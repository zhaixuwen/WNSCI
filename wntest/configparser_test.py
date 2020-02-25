import configparser

config = configparser.ConfigParser()
filename = '../config/config.ini'
config.read(filename, encoding='utf-8')
sections = config.sections()
print(sections)
items = config.items('svn')
print(items)
vpn_path = config.get('svn', 'svn_path')
print(vpn_path)