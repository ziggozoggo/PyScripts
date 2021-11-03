import subprocess
import sys, os

# Файл для экспериментов
file_name = "C:\\_myProgs\\PyScripts\\source\\kiberbezopasnost_test_720p.mp4"
# Путь до ffmpeg; PATH прописать админы не дают же
ffmpeg_exe = "C:\\Progs\\ffmpeg-4.4-full_build\\bin\\ffmpeg.exe"
# Результат эксперимента
file_output = "C:\\_myProgs\\PyScripts\\out\\out_3_slower_moveFlags.mp4"

# Параметры ffmpeg; маппим видео канал (трек) 4 раза, по числу требуемых потоков
# в целевом файле.
# -map 0:1 - это аудио поток; он один
map_input = ['-map', '0:0', '-map', '0:0', '-map', '0:0', '-map', '0:0', '-map', '0:1']
map_input2 = ['-map', '0:0', '-map', '0:0', '-map', '0:1']
map_input_tst = ['-map', '0:0', '-map', '0:1']

# Интересные параметры
profile = 'high'
movflags = '+faststart' # Перемещает часть информации в начало файла; хорошо для web

# Целевые видео треки/потоки (track/stream); исходим из того, что все файлы макс. в 720p
# с первым потоком ничего не делаем.
# Про maxrate и bufrate:
# maxrate - максимальная ширина канала, занимаемая видео-потоком (не забываем про аудио - 128 Кбит/с !)
# bufsize - размер буфера в Кбит; 1-2 секунды - gaming screencast; до 5 секунд - статичный контент

# Wi-FI - 5 Мбит/с
target_stream_720p = ['-c:v:0', 'libx264', '-crf:0', '18', '-maxrate:0', '3968K', '-bufsize:0', '7936K', '-filter:v:0', 
                      'scale=1280:720']
# Default 720p
target_stream_720p_def = ['-c:v:0', 'libx264']

# 4G(LTE) - 2 Мбит/с
target_stream_480p = ['-c:v:1', 'libx264', '-crf:1', '23', '-maxrate:1', '1511K', '-bufsize:v:1', '3022K', '-filter:v:1', 
                      'scale=trunc(oh*a/2)*2:480']
# 3G - 1 Мбит/с
target_stream_360p = ['-c:v:2', 'libx264', '-crf:2', '23', '-maxrate:2', '692K', '-bufsize:v:2', '1384K', '-filter:v:2', 
                      'scale=trunc(oh*a/2)*2:360']
# 3G/ADSL до 512 Кбит/с
target_stream_240p = ['-c:v:3', 'libx264', '-crf:3', '23', '-maxrate:3', '282K', '-bufsize:v:3', '564K', '-filter:v:3', 
                      'scale=trunc(oh*a/2)*2:240']
# EDGE/UMTS 3G до 384 Кбит/с; исключаем этот вариант.
target_stream_240p_Low = ['-c:v:4', 'libx264', '-crf:4', '30', '-maxrate:4', '180K', '-bufsize:v:4', '540K', '-filter:v:4', 
                      'scale=trunc(oh*a/2)*2:240']


test_stream = ['-c:v:0', 'libx264', '-crf:0', '23', '-maxrate:0', '1700K', '-bufsize:0', '3400K', '-vf:0', 
                      'scale=-1:720']
test_stream2 = ['-c:v:0', 'libx264']


# Запуск ffmpeg
command = [ffmpeg_exe, '-i', file_name,'-preset','slower', '-movflags', movflags]
out = [file_output]

final_list = command + map_input + target_stream_720p_def + target_stream_480p + target_stream_360p + target_stream_240p + out
#final_list = command + map_input2 + target_stream_720p + target_stream_480p + out
launch_str = ' '.join(final_list)
print(launch_str)

subprocess.run(launch_str, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

