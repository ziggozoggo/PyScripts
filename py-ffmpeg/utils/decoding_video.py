import subprocess
import sys, os

def decoding_file(file_name, ffmpeg_exe, file_output):
    ''' На вход - файл высокого качества
        На выходе - мультибитрейд
    '''
    #file_output = file_name + '_new.mp4'
    command = [ffmpeg_exe, '-i', file_name, '-map', '0:0', '-map', '0:0', '-map', '0:0', '-map', '0:0',
               '-map', '0:1', 
               '-c:v:0', 'libx264', '-b:v:0', '2500k', '-metadata:s:v:0', 'language=eng',
               '-c:v:1', 'libx264', '-b:v:1', '1200k', '-s:v:1', '854x480', '-metadata:s:v:1', 'language=eng',
               '-c:v:2', 'libx264', '-b:v:2', '800k', '-s:v:2', '640x360', '-metadata:s:v:2', 'language=eng',
               '-c:v:3', 'libx264', '-b:v:3', '400k', '-s:v:3', '426x240', '-metadata:s:v:3', 'language=eng',
               file_output
    ]
    my_str = ' '.join(command)
    print(my_str)
    subprocess.run(my_str, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

my_file = "C:\\_myProgs\\PyScripts\\source\\kiberbezopasnost_test_720p.mp4"
my_ffpmeg = "C:\\Progs\\ffmpeg-4.4-full_build\\bin\\ffmpeg.exe"
my_out = "C:\\_myProgs\\PyScripts\\out\\out_2.mp4"

decoding_file(my_file,my_ffpmeg,my_out)

