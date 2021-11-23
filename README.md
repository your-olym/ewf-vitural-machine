# ewf-vitural-machine
forensics - make virtual machine with E01[ewf] files on OSX ———— 电子取证 MAC OS平台仿真


浏览了很多网站,基于OSX平台上的**电子取证** 工具很少,仿真实验室又不支持虚拟机,于是决定自己找办法,在OSX上直接仿真。主要百度,必应还有那个啥都找了,没有资料🤨
# 1挂载
自己是catalina(10.15)
Darwin XXX.local 19.6.0 Darwin Kernel Version 19.6.0: Thu Sep 16 20:58:47 PDT 2021; root:xnu-6153.141.40.1~1/RELEASE_X86_64 x86_64


首先我们来看一下挂载命令都有哪些

```shell
mount
diskutil mount
hdiutil mount
```
这些挂载命令在对linux文件系统执行时也会有较大的差异,平时也需要注意
等会需要用到 diskutil,这是一个系统自带的工具,比磁盘管理用处稍大



 ## 库安装
环境搭建到现在我好像安了挺多东西了,我会尽可能的列出来,还有没有的命令大家可以自己github一下或着评论留言
### osxfuse
这是为libewf库做的基础
要注意不是 MacFuse 这两者也是存在区别的
[https://github.com/osxfuse/osxfuse/releases/download/osxfuse-3.10.0/osxfuse-3.10.0.dmg](https://github.com/osxfuse/osxfuse/releases/download/osxfuse-3.10.0/osxfuse-3.10.0.dmg)

### libewf
毫无疑问这是我迄今为止装的最久的库了,让我想到了在自带的python2下安装pwntools

建议大家下载旧一点点的libewf,我安装实验版还有最新的稳定版都存在错误
首先安装mac port  官网
[https://www.macports.org/install.php](https://www.macports.org/install.php)
不同系统版本对应不同软件版本的像我Catalina是 
[https://github.com/macports/macports-base/releases/download/v2.7.1/MacPorts-2.7.1-10.15-Catalina.pkg](https://github.com/macports/macports-base/releases/download/v2.7.1/MacPorts-2.7.1-10.15-Catalina.pkg)
然后借用mac port安装一些能自动安装的环境
```shell
sudo port install git autoconf automake gettext libtool pkgconfig flex byacc
```
下载libewf工具
[https://github.com/libyal/libewf-legacy/releases/download/20140811/libewf-20140811.tar.gz](https://github.com/libyal/libewf-legacy/releases/download/20140811/libewf-20140811.tar.gz)
解压后cd 进入目录然后输入三个命令进行安装
```shell
# dsa @ '(^-^)' in ~ [23:26:10] C:127
$ cd /Users/dsa/Downloads/libewf-20140811

# dsa @ '(^-^)' in ~/Downloads/libewf-20140811 [23:37:16]
$ ./configure --prefix=/usr/local --enable-python --with-pyprefix

checking for a BSD-compatible install... /usr/bin/install -c
checking whether build environment is sane... yes
checking for a thread-safe mkdir -p... ./install-sh -c -d
...
...
...
Features:
   Multi-threading support:                  pthread
   Wide character type support:              no
   Write support:                            yes
   ewftools are build as static executables: no
   Python (pyewf) support:                   3.7
   Verbose output:                           no
   Debug output:                             no
   Version 1 API compatibility:              no


# dsa @ '(^-^)' in ~/Downloads/libewf-20140811 [23:39:29]
$ make

...
...
...
Making all in msvscpp
make[1]: Nothing to be done for `all'.
make[1]: Nothing to be done for `all-am'.

# dsa @ '(^-^)' in ~/Downloads/libewf-20140811 [23:42:19]
$ make install DESTDIR=/
```


然后就可以使用libewf库了

![在这里插入图片描述](https://img-blog.csdnimg.cn/f851d29152954dab95b0f6b27f3db9a2.png?x-oss-process=image/watermark,type_ZHJvaWRzYW5zZmFsbGJhY2s,shadow_50,text_Q1NETiBA6L6b6L6b5a2m5ruT,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)



# 2 虚拟机存储文件
我自己尝试过很多命令,试图直接实现windows下那样FTK Imager挂载后直接通过虚拟机访问磁盘来实现仿真,但是mac下好像挂载时没有办法挂载成物理磁盘,会被PD检测报错,VM就直接不报错了,直接输出帮助内容

## qemu 
于是我决定用挂载出的raw文件创建一个虚拟磁盘 
这就用到了qemu-img
这是一个很强大的虚拟磁盘管理工具大家可以参考下面这篇文章来了解
[https://blog.csdn.net/u012324798/article/details/109705017](https://blog.csdn.net/u012324798/article/details/109705017)


我尝试过 PD VM自己的创建虚拟磁盘的方法,当然这些都是挂载物理磁盘时读取做虚拟机系统的

/Applications/Parallels\ Desktop.app/Contents/MacOS/prl_disk_tool create -p --hdd ~/10.hdd --ext-disk-path /dev/disk2

/Applications/VMware\ Fusion.app/Contents/Library/vmware-rawdiskCreator creat /dev/disk2 "fullDevice" /Users/dsa/Parallels/CentOS\ Linux.pvm\ssk  "ide"

大家有兴趣可以深入研究,在需要挂载多个磁盘时也能够提供参考
# 3 开始实验&&虚拟机导入

这一部分需要图片辅助,我们也就从这里开始实际操作吧
```shell
# dsa @ '(^-^)' in ~ [12:08:51]
$ diskutil list                  
                                该命令只用做查看系统挂载镜像,可以不做
/dev/disk0 (internal, physical):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:      GUID_partition_scheme                        *1.0 TB     disk0
   1:                        EFI EFI                     314.6 MB   disk0s1
   2:                 Apple_APFS Container disk1         899.0 GB   disk0s2
   3:       Microsoft Basic Data BOOTCAMP                100.6 GB   disk0s3
   4:           Windows Recovery                         610.3 MB   disk0s4

/dev/disk1 (synthesized):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:      APFS Container Scheme -                      +899.0 GB   disk1
                                 Physical Store disk0s2
   1:                APFS Volume Macintosh HD            11.4 GB    disk1s1
   2:                APFS Volume Macintosh HD - Data     699.4 GB   disk1s2
   3:                APFS Volume Preboot                 83.6 MB    disk1s3
   4:                APFS Volume Recovery                529.0 MB   disk1s4
   5:                APFS Volume VM                      3.2 GB     disk1s5


# dsa @ '(^-^)' in ~ [12:09:06]
$ mkdir ~/tmp/mpoint

# dsa @ '(^-^)' in ~ [12:11:48]    //挂载E01文件到挂载点
$ ewfmount -X volicon=/Library/Filesystems/osxfuse.fs/Contents/Resources/Volume.icns  /Users/dsa/Downloads/检材4.E01 ~/tmp/mpoint
ewfmount 20140811


# dsa @ '(^-^)' in ~ [12:13:34]
$ diskutil list
/dev/disk0 (internal, physical):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:      GUID_partition_scheme                        *1.0 TB     disk0
   1:                        EFI EFI                     314.6 MB   disk0s1
   2:                 Apple_APFS Container disk1         899.0 GB   disk0s2
   3:       Microsoft Basic Data BOOTCAMP                100.6 GB   disk0s3
   4:           Windows Recovery                         610.3 MB   disk0s4

/dev/disk1 (synthesized):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:      APFS Container Scheme -                      +899.0 GB   disk1
                                 Physical Store disk0s2
   1:                APFS Volume Macintosh HD            11.4 GB    disk1s1
   2:                APFS Volume Macintosh HD - Data     699.4 GB   disk1s2
   3:                APFS Volume Preboot                 83.6 MB    disk1s3
   4:                APFS Volume Recovery                529.0 MB   disk1s4
   5:                APFS Volume VM                      3.2 GB     disk1s5


# dsa @ '(^-^)' in ~ [12:14:13]    上一步可以看到还没有检测出来,还需要下一步挂载到系统
$ hdiutil attach -imagekey diskimage-class=CRawDiskImage -nomount ~/tmp/mpoint/ewf1
/dev/disk2          	FDisk_partition_scheme
/dev/disk2s1        	Linux
/dev/disk2s2        	Linux_LVM

# dsa @ '(^-^)' in ~ [12:14:42]
$ diskutil list
/dev/disk0 (internal, physical):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:      GUID_partition_scheme                        *1.0 TB     disk0
   1:                        EFI EFI                     314.6 MB   disk0s1
   2:                 Apple_APFS Container disk1         899.0 GB   disk0s2
   3:       Microsoft Basic Data BOOTCAMP                100.6 GB   disk0s3
   4:           Windows Recovery                         610.3 MB   disk0s4

/dev/disk1 (synthesized):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:      APFS Container Scheme -                      +899.0 GB   disk1
                                 Physical Store disk0s2
   1:                APFS Volume Macintosh HD            11.4 GB    disk1s1
   2:                APFS Volume Macintosh HD - Data     699.4 GB   disk1s2
   3:                APFS Volume Preboot                 83.6 MB    disk1s3
   4:                APFS Volume Recovery                529.0 MB   disk1s4
   5:                APFS Volume VM                      3.2 GB     disk1s5

/dev/disk2 (disk image):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:     FDisk_partition_scheme                        +21.5 GB    disk2
   1:                      Linux                         1.1 GB     disk2s1
   2:                  Linux_LVM                         20.4 GB    disk2s2

挂载完毕后使用下条命令制作vmdk虚拟磁盘 路径不能省略,不能用 sudo
# dsa @ '(^-^)' in ~ [12:14:44]
$ /usr/local/Cellar/qemu/6.1.0_1/bin/qemu-img convert -O vmdk ~/tmp/mpoint/ewf1 /Users/dsa/Virtual\ Machines.localized/mpoint.vmwarevm/检材.vmdk

```
到这里我们就成功建立vmdk文件了,然后可以开始启动虚拟机了,像这里我是创建在了已有的文件夹里,导入然后更改启动项就好了![在这里插入图片描述](https://img-blog.csdnimg.cn/a5fade4241d14b1aabc3c7f3b578bc71.png?x-oss-process=image/watermark,type_ZHJvaWRzYW5zZmFsbGJhY2s,shadow_50,text_Q1NETiBA6L6b6L6b5a2m5ruT,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)


![在这里插入图片描述](https://img-blog.csdnimg.cn/a2d42199fa8f49b399672d62060f0ca8.png?x-oss-process=image/watermark,type_ZHJvaWRzYW5zZmFsbGJhY2s,shadow_50,text_Q1NETiBA6L6b6L6b5a2m5ruT,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)
也可以创建在外面,然后新建虚拟机,注意固件选项需要是BIOS启动的,然后选中磁盘后VM会自动复制到新建虚拟机上(如果导入时为共享磁盘的话,需要文件在虚拟机目录下才能启动)




git了一周,好累😌转载记得说明哈
