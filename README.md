# pi_ssd1306_sysinfo
树莓派使用SSD1306 OLED显示系统信息

## 添加为开启自启动服务
复制 oled-system-info.py 文件到 /usr/bin/

复制 oled-system-info.service 文件到 /lib/systemd/system/

sudo systemctrl enable oled-system-info.service

sudo reboot

就能看到启动后的信息了!

![WechatIMG533](https://user-images.githubusercontent.com/469091/111262587-72bdf980-865f-11eb-81e5-191413a630b4.jpeg)
