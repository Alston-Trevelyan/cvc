# CVC

Convert video to character art animation.

[中文说明](/doc/README-zh-cn.md)

## Install


Install cvc:
```
pip install cvc
```

This tool relies on `imageio-ffmpeg`, but only the binary version of `imageio-ffmpeg` contains the `ffmpeg` binary.
if pip choose the source version, problem will occurs.

## Usage

```
cvc --chars_width 120 --t_end 10 path/of/video_file
```
The command shows that the specified video will be converted to an ascii art animation with the width of 120, and only convert the first 10 seconds.
you'll see a file named `output.mp4` in your current directory when completes, have fun ~

>p.s. it's a bit slow, turn down the width and fps, to speed up the conversion.

Check `cvc --help` for more information.
