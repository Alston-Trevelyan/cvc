# 视频、图片转字符动画

这是一个能将视频文件转换成字符动画的命令行工具，使用 pillow + moviepy 实现

## 安装

直接使用 pip 安装 cvc:
```
pip install cvc
```
本工具依赖 `imageio-ffmpeg`，但只有二进制版本的该依赖内嵌 ffmpeg，如果你从源码安装，很可能会出问题。

## 用法

```
cvc --chars_width 120 --t_end 10 path/of/video_file
```
上面的命令表示，将指定路径的视频，转换成宽度为120字符的视频，只转换前十秒。
命令运行完毕后，会在当前目录下生成一个名为 `output.mp4` 的字符视频。

使用 `cvc --help` 命令，获取更多信息。

>p.s. 注意性能。默认参数 chars_width=120 fps=8。实在是慢的话，可以尝试调低一下这两个参数。