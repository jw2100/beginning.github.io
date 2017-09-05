# 一些注意事项 #
- 如果机器是64位，需要使用64位元的方法进行编译安装 

>  CFLAGS="-O3 -fPIC" ./configure

- 需要x264进行视频转码
	
	1. Git clone http://git.videolan.org/git/x264.git
	2.  sudo ./configure --enable-shared --disable-asm
	3. 	sudo make && make install
	4. 	重新安装ffmpeg 
	5. 	sudo  ./configure --enable-shared --disable-yasm --enable-libx264  --enable-gpl  --prefix=/usr/local/ffmpeg
	6. 	sudo make && make install
	

----------


- 加载库  把ffmpeg的lib库加载到系统，不然会出错 echo '/usr/local/ffmpeg/lib'      >> /etc/ld.so.conf  && ldconfig

- export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH  && ldconfig

- PATH=$PATH:/usr/local/ffmpeg2/bin

- ln -s /usr/local/lib/libx264.so.142 /usr/lib/libx264.so.142


# 使用 #

- 截取（指定时间长度[duration] 指定分辨率 1080*1902  指定使用线程数 -threads）

> {$ffmpegBin} -y -ss 00:00:00 -i {$sourceFile} -s 1080x1902 -c:a copy -t {$duration} -threads 2 {$destFile}


- 加水印(指定图片位置movie，调整图片分辨率 scale=1080:1902，转高清 -q 0， 转编码 -vcodec h264)

> "{$ffmpegBin} -y -i {$sourceFile} -vf  \"movie={$imgPath},scale={$resolution[0]}:{$resolution[1]}[watermask]; [in] [watermask] overlay=0:0 [out]\" -q 0 -vcodec h264 -threads 2 $destFile 2>&1"