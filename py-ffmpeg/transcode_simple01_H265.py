import subprocess
import sys, os

# Файл для экспериментов
file_name = "C:\\_myProgs\\PyScripts\\source\\kiberbezopasnost_test_720p.mp4"
# Путь до ffmpeg; PATH прописать админы не дают же
ffmpeg_exe = "C:\\Progs\\ffmpeg-4.4-full_build\\bin\\ffmpeg.exe"
# Результат эксперимента
file_output = "C:\\_myProgs\\PyScripts\\out\\out_2_H265.mp4"

# Параметры ffmpeg; маппим видео канал (трек) 4 раза, по числу требуемых потоков
# в целевом файле.
# -map 0:1 - это аудио поток; он один
map_input = ['-map', '0:0', '-map', '0:0', '-map', '0:0', '-map', '0:0', '-map', '0:1']
map_input2 = ['-map', '0:0', '-map', '0:0', '-map', '0:1']
map_input_tst = ['-map', '0:0', '-map', '0:1']

# Целевые видео треки/потоки (track/stream); исходим из того, что все файлы макс. в 720p
# с первым потоком ничего не делаем.

target_stream_720p = ['-c:v:0', 'libx265', '-crf:0', '28', '-x265-params:0', 'vbv-maxrate=1700:vbv-bufsize=3400','-filter:v:0', 
                      'scale=1280:720']
target_stream_480p = ['-c:v:1', 'libx265', '-crf:1', '28', '-x265-params:1', 'vbv-maxrate=800:vbv-bufsize=1600','-filter:v:1', 
                      'scale=854:480']
target_stream_360p = ['-c:v:2', 'libx265', '-crf:2', '28', '-x265-params:2', 'vbv-maxrate=600:vbv-bufsize=1200','-filter:v:1', 
                      'scale=640:360']
target_stream_240p = ['-c:v:3', 'libx265', '-crf:3', '28', '-x265-params:3', 'vbv-maxrate=500:vbv-bufsize=1000','-filter:v:3', 
                      'scale=426:240']


test_stream = ['-c:v:0', 'libx264', '-crf:0', '23', '-maxrate:0', '1700K', '-bufsize:0', '3400K', '-vf:0', 
                      'scale=-1:720']
test_stream2 = ['-c:v:0', 'libx264']


# Запуск ffmpeg
command = [ffmpeg_exe, '-i', file_name,'-preset','slow']
out = [file_output]

final_list = command + map_input + target_stream_720p + target_stream_480p + target_stream_360p + target_stream_240p + out
#final_list = command + map_input2 + target_stream_720p + target_stream_480p + out
launch_str = ' '.join(final_list)
print(launch_str)

subprocess.run(launch_str, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

