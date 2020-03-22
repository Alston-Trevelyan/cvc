# -*- coding:utf-8 -*-

import click
import os

from cvc.converter import CharsConverter


@click.command()
@click.option("--chars_width", default=100, help='The width of the generated video, in characters, default to 80. Bigger is clearer but file size is also bigger')
@click.option("--fps", default=8, help='frames per second, default to 10')
@click.option("--pixels", default=None, type=str, help='the chars sequence used to generate character animation')
@click.option("--t_start", default=0, help="the start time that the video needs to be converted(in seconds)")
@click.option("--t_end", default=None, type=int, help="the end time that the video needs to be converted(in seconds)")
@click.option("--output", default="output.mp4", help='output to a file with this name, default to "output.mp4"')
@click.option("--font_size", default=14, type=int, help="font size, default to 14. Smaller is lighter and file size is smaller.")
@click.argument("filename")
def convert(filename, chars_width, font_size, fps, pixels, output, t_start, t_end):
    filetype = os.path.splitext(filename)[-1]
    converter = CharsConverter(path=filename,
                            fps=fps,
                            chars_width=chars_width,
                            filetype=filetype,
                            font_size=font_size,
                            t_start=t_start,
                            t_end=t_end,
                            pixels=pixels)
    
    
    if filetype in ('.mp4', '.mkv', '.avi', '.wmv', '.iso'):
        clip = converter.generate_chars_video()
        output = os.path.splitext(output)[0] + filetype if output not in ('.mp4', '.mkv', '.avi', '.wmv', '.iso') else output
        clip.write_videofile(os.path.abspath(output))
        
    elif filetype in ('.jpg', '.jpeg', '.ico', '.png', '.bmp'):
        img = converter.generate_chars_image()
        output = os.path.splitext(output)[0] + filetype if output not in ('.jpg', '.jpeg', '.ico', '.png', '.bmp') else output
        img.save(os.path.abspath(output))
