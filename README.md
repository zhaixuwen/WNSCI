# WNSCI
利用woniusales系统做的CI的demo,梳理持续集成各个环节的相关知识。

## 涉及的点
1. svn获取最新代码
2. ant打包
3. 停止相关服务(tomcat/mysql等)再替换为最新包
4. 重启服务
5. 运行test下自动测试脚本
6. 将测试结果生成测试报告
7. 最后将测试报告email给指定人员
## 完善
1. svn路径/tomcat路径等参数通过configparser配置文件方式实现，方便维护使用
