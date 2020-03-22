# -*- coding:utf-8 -*-

from pkg_resources import resource_stream

import numpy as np
from moviepy.editor import *

from PIL import Image, ImageFont, ImageDraw


class CharsConverter:
    def __init__(self, path, fps, pixels, filetype, font_size, chars_width, t_start=0, t_end=None):
        """
        :param path: 字符串, 视频文件的路径
        :param fps: 生成的视频的帧率
        :param pixels:用于充当像素的字符，因为颜色已经用rgb控制了，这里的pixels其实可以随意排
        :param chars_width: 字符的宽度（以像素记），会影响最终视频的分辨率。
        :param t_start, t_end: 视频的开始时间和结束时间，只处理指定时间段的视频。
        """
        # 像素形状，因为颜色已经用rgb控制了，这里的pixels其实可以随意排
        self.pixels = pixels if pixels else \
            r"⣿⢿⡿⣽⣻⢿⣾⣵⡷⢻⡟⣛⣧⢻⣙⣥⣦⠻⣴⣌⣖⡋⣇⠶⠹⢋⣡⢸⢃⡌⠦⠸⡅⠙⣠⠒⠃⡄⢠⠄⢀ "
        # "$#@&%ZYXWVUTSRQPONMLKJIHGFEDCBA098765432?][}{/)(><zyxwvutsrqponmlkjihgfedcba*+1-. "
        
        self.chars_width = chars_width
        self.filetype = filetype

        # 字体相关
        font_fp = resource_stream("cvc", "arial.ttf")
        self.font = ImageFont.truetype(font_fp, size=font_size)  # 使用等宽字体
        self.font_width = sum(self.font.getsize(self.pixels)) // len(self.pixels)  # 为了保证像素宽高一致，均取宽高的平均值
        
        if self.filetype in ('.mp4', '.mkv', '.avi', '.wmv', '.iso'):
            # 加载视频,并截取
            try:
                video_clip = VideoFileClip(path).subclip(t_start, t_end)
            except OSError as e:
                raise OSError(e)

            self.fps = fps
            self.chars_height = int(chars_width / video_clip.aspect_ratio)

            # resize 一下
            self.video_clip: VideoClip = video_clip.resize((self.chars_width, self.chars_height))

        elif self.filetype in ('.jpg', '.jpeg', '.ico', '.png', '.bmp'):
            # 加载图片
            try:
                self.image = Image.open(path)
            except FileNotFoundError as e:
                raise FileNotFoundError(e)
            
            self.chars_height = int(self.chars_width * (self.image.size[1] / self.image.size[0]))  # 现高=现宽x纵横比
            
            # resize 一下
            self.image = self.image.resize((self.chars_width, self.chars_height))
        
        else:
            self.instruct()
        
        # 产生的视频/图片的宽高（以像素记）
        self.size = int(self.chars_width * self.font_width), int(self.chars_height * self.font_width)

    def get_char_by_gray(self, gray):
        """通过灰度值从 pixels 中挑选字符，充当字符动画中的‘像素’"""
        percent = gray / 255  # 转换到 0-1 之间
        index = int(percent * (len(self.pixels) - 1))  # 拿到index
        return self.pixels[index]
    
    def instruct(self):
        print('FileTypeError: You input a wrong format of file.')
        os.system('cls')
        exit()
    
    def get_chars_frame(self, temp):
        """将图片转换为字符画"""
        # 获取到图像
        img = Image.fromarray(self.video_clip.get_frame(temp), 'RGB') if self.filetype in ('.mp4', '.mkv', '.avi', '.wmv', '.iso') else temp
        img_gray = img.convert(mode="L")

        # 新建画布
        img_chars = Image.new("RGB", self.size, color="white")
        brush = ImageDraw.Draw(img_chars)  # 画笔

        for y in range(self.chars_height):
            for x in range(self.chars_width):
                rgb = img.getpixel((x,y))
                gray = img_gray.getpixel((x, y))
                char = self.get_char_by_gray(gray)
                
                position = x * self.font_width, y * self.font_width  # x 横坐标（宽），y纵坐标（高，而且向下为正）
                brush.text(position, char, fill=rgb, font=self.font)

        return np.array(img_chars)

    def generate_chars_video(self):
        """生成字符视频对象"""
        clip = VideoClip(self.get_chars_frame, duration=self.video_clip.duration)

        return (clip.set_fps(self.fps)
                .set_audio(self.video_clip.audio))
    
    def generate_chars_image(self):
        """生成字符图片对象"""
        img = Image.fromarray(self.get_chars_frame(self.image), 'RGB')
        return img

