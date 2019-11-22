# xidian_script
查询校园网流量以及电费余额的Python脚本

因为最近找到了各种**不需要验证码**的接口，做了一次大更新，之前的仓库太乱就删了，但是依然保留了之前处理识别验证码的成果在dev分支，如果想用到更多的校园内的爬虫脚本可以参考：

[xdlinux/xidian-scripts](https://github.com/xdlinux/xidian-scripts)

写法更规范（中断了7年的项目后又有人维护了）

## 使用方法
安装完需要的包之后，在脚本内填写账号信息，如果不想安装太多的倚赖的话可以考虑用*_log文件，输出也会简单一些

在校园网环境下直接运行即可使用，详情可见于博客(代码可能在dev分支)：
- https://lwz322.github.io/2018/11/30/Flow.html
- https://lwz322.github.io/2019/3/30/Efee.html

注：因为代码本身结构很简单，报错部分写的比较简略...实在有问题联系作者吧

## 文件
master分支方便clone
- xidian_flow.py，查询校园网流量
- xidian_me.py，查询宿舍电费的余额，电费账号可以在
- *_log文件则是简化倚赖，适配平台和定制输出，满足简单的使用和记录
- *_sh文件用于执行计划任务，处理查询结果并输出到文档，可以放到路由器之类的设备中，用于记录


dev分支：
- 包括了中间查看验证码的处理等调试需要的注释（信息量多一点，可能有些乱）
- 一些实验性的代码（瞎写的）
  - xidian_flow_captcha.py，验证码识别，可以借助标注提高准确率
  - xidian_me_selenium.py，之前写的处理和识别带彩色噪点的验证码，因为没搞定Requests登陆，用的selenium模拟
  - Dockerfile 考虑到上面的倚赖比较多且运行的环境相对复杂，为了省时省力就放到Docker中运行
- ar.traineddata，Tesseract识别验证码的标注数据