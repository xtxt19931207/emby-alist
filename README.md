# emby-alist
emby挂载alist媒体库  


一、前提  
配置好的Alist服务端和Emby服务端  
Emby的strm文件应用参考：https://emby.media/support/articles/Strm-Files.html  


二、总体思路  
我们需要获取Alist服务器上指定目录下的视频文件名称、路径、播放链接，然后在Emby媒体库路径下生成相同的路径、文件名（后缀改为strm，内容为播放链接）的文本文件，同时也可以把字幕文件一起复制过来。效果如下图：  
 ![image](https://github.com/xtxt19931207/emby-alist/blob/main/1.png)  
          Alist文件  
 ![image](https://github.com/xtxt19931207/emby-alist/blob/main/2.png)  
          本地文件（Emby媒体库） 

          
三、优势和效果  
这种方案最大的优势就是节省本地空间，而且比之前挂载的方法稳定，因为读取的就是本地文件，不会存在反复扫描的情况，设备重启后也不用担心掉盘或者需要重启Emby才能识别媒体库。
两千多个视频文件，空间占用只有几百KB：  
![image](https://github.com/xtxt19931207/emby-alist/blob/main/3.png)  


四、后续  
这种方法虽然简便，但是每次更新都需要在电脑上点下程序，后续的的想法是能做一个OpenWrt下的程序，或者打包成Docker镜像运行，有想法的朋友也可以帮忙做一下。
