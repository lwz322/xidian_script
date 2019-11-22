FROM ubuntu:latest
MAINTAINER lwz322@qq.com
# 拷贝本地文件到镜像中 efee.sh *.py
COPY ./* /root/
# 在build这个镜像时执行的操作：中文支持
ENV LANG C.UTF-8

# 修改软件源以及安装倚赖和必要的软件
RUN sed -i 's/archive.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list \
&& apt-get update && mkdir ~/.pip && touch ~/.pip/pip.conf \
&& apt-get install -y python3-pip vim tesseract-ocr chromium-chromedriver screen cron ssh gawk

RUN echo "[global] \nindex-url = https://mirrors.ustc.edu.cn/pypi/web/simple \nformat = columns" > ~/.pip/pip.conf \
&& pip3 install pytesseract lxml prettytable cssselect selenium requests

# 添加cron计划任务
RUN echo "*/30 * * * * /root/efee.sh 2>&1" >> /var/spool/cron/crontabs/root \
&& echo "tessedit_char_whitelist 0123456789QWERTYUIOPASDFGHJKLZXCVBNM" > /usr/share/tesseract-ocr/*/tessdata/configs/DIGIT_CAPS