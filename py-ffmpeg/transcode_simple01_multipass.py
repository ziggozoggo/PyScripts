# !!!!!!! НЕ РАБОТАЕТ !!!!!! Не складывает все потоки в один файл.
# Для теста плейера; добавляем на каждый поток текст

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

# Text mark

text_mark_720p = ['-vf', '"drawtext="text=\'720P\':x=100:y=50:fontsize=120:fontcolor=yellow:box=1:boxcolor=red"']
text_mark_480p = ['-filter:v:1', '"drawtext="text=\'480P\':x=100:y=50:fontsize=120:fontcolor=yellow:box=1:boxcolor=red" ']
text_mark_360p = ['-filter:v:2', '"drawtext="text=\'360P\':x=100:y=50:fontsize=120:fontcolor=yellow:box=1:boxcolor=red" ']
text_mark_240p = ['-filter:v:3', '"drawtext="text=\'360P\':x=100:y=50:fontsize=120:fontcolor=yellow:box=1:boxcolor=red" ']

# Целевые видео треки/потоки (track/stream); исходим из того, что все файлы макс. в 720p
# с первым потоком ничего не делаем.

target_stream_720p = ['-c:v:0', 'libx264', '-crf', '23', '-maxrate', '1700K', '-bufsize', '3400K', '-vf', 
                      'scale=1280:720']
target_stream_480p = ['-c:v:1', 'libx264', '-crf', '23', '-maxrate', '800K', '-bufsize', '1600K', '-vf', 
                      'scale=854:480']
target_stream_360p = ['-c:v:2', 'libx264', '-crf', '23', '-maxrate', '600K', '-bufsize', '1200K', '-vf', 
                      'scale=640:360']
target_stream_240p = ['-c:v:3', 'libx264', '-crf', '23', '-maxrate', '500K', '-bufsize', '1000K', '-vf', 
                      'scale=426:240']



# Запуск ffmpeg
command = [ffmpeg_exe, '-i', file_name,'-preset','slow']
multi_pass1 = ['-pass','1', '-f null NUL']
multi_pass2 = ['-pass','2', '-f null NUL']
multi_pass3 = ['-pass','3', '-f null NUL']
out = [file_output]

final_list1 = command + target_stream_720p + multi_pass1
final_list2 = command + target_stream_480p + multi_pass2
final_list3 = command + target_stream_360p + multi_pass3
final_list4 = command + target_stream_240p + out

#final_list = command + map_input + target_stream_720p + text_mark_720p +  target_stream_480p +  target_stream_360p +  target_stream_240p + out
#final_list = command + map_input2 + target_stream_720p + target_stream_480p + out
launch_str1 = ' '.join(final_list1)
launch_str2 = ' '.join(final_list2)
launch_str3 = ' '.join(final_list3)
launch_str4 = ' '.join(final_list4)

subprocess.run(launch_str1, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
subprocess.run(launch_str2, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
subprocess.run(launch_str3, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
subprocess.run(launch_str4, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

