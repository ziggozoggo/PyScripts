import subprocess
import sys, os

# Файл для экспериментов
file_name = "C:\\_myProgs\\PyScripts\\source\\kiberbezopasnost_test_720p.mp4"
# Путь до ffmpeg; PATH прописать админы не дают же
ffmpeg_exe = "C:\\Progs\\ffmpeg-4.4-full_build\\bin\\ffmpeg.exe"
# Результат эксперимента
file_output = "C:\\_myProgs\\PyScripts\\out\\out_2.mp4"

# Параметры ffmpeg; маппим видео канал (трек) 4 раза, по числу требуемых потоков
# в целевом файле.
# -map 0:1 - это аудио поток; он один
map_input = ['-map', '0:0', '-map', '0:0', '-map', '0:0', '-map', '0:0', '-map', '0:1']
map_input2 = ['-map', '0:0', '-map', '0:0', '-map', '0:1']
map_input_tst = ['-map', '0:0', '-map', '0:1']

# Целевые видео треки/потоки (track/stream); исходим из того, что все файлы макс. в 720p
# с первым потоком ничего не делаем.

target_stream_720p = ['-c:v:0', 'libx264', '-crf:0', '23', '-maxrate:0', '1700K', '-bufsize:0', '3400K', '-filter:v:0', 
                      'scale=1280:720']
target_stream_480p = ['-c:v:1', 'libx264', '-crf:1', '23', '-maxrate:1', '800K', '-bufsize:v:1', '1600K', '-filter:v:1', 
                      'scale=854:480']
target_stream_360p = ['-c:v:2', 'libx264', '-crf:2', '23', '-maxrate:2', '600K', '-bufsize:v:2', '1200K', '-filter:v:2', 
                      'scale=640:360']
target_stream_240p = ['-c:v:3', 'libx264', '-crf:3', '23', '-maxrate:3', '500K', '-bufsize:v:3', '1000K', '-filter:v:3', 
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

