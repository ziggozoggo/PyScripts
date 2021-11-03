# Для теста плейера; Берём готовый файл с N потоками и бацаем на него текст
# https://study-video.severstal.com/Vprod/flussonic.asp?stream=SEDO/MB/kiberbezopasnost_test/kiberbezopasnost_test_720p_full.mp4

import subprocess
import sys, os

# Файл для экспериментов
file_name = "C:\\_myProgs\\PyScripts\\out\\out_2_VSlow_New.mp4"
# Путь до ffmpeg; PATH прописать админы не дают же
ffmpeg_exe = "C:\\Progs\\ffmpeg-4.4-full_build\\bin\\ffmpeg.exe"
# Результат эксперимента
file_output = "C:\\_myProgs\\PyScripts\\out\\out_2_VSlow_New_marked.mp4"

# Параметры ffmpeg; маппим видео каналы 

map_input = ['-map', '0:0', '-map', '0:1', '-map', '0:2', '-map', '0:3', '-map', '0:4']

# Text mark

text_mark_720p = ['-filter:v:0', 'drawtext="text=\'720P\':x=100:y=50:fontsize=120:fontcolor=yellow:box=1:boxcolor=red"']
text_mark_480p = ['-filter:v:1', 'drawtext="text=\'480P\':x=100:y=50:fontsize=120:fontcolor=yellow:box=1:boxcolor=red"']
text_mark_360p = ['-filter:v:2', 'drawtext="text=\'360P\':x=100:y=50:fontsize=120:fontcolor=yellow:box=1:boxcolor=red"']
text_mark_240p = ['-filter:v:3', 'drawtext="text=\'240P\':x=100:y=50:fontsize=120:fontcolor=yellow:box=1:boxcolor=red"']

# Запуск ffmpeg
command = [ffmpeg_exe, '-i', file_name,'-preset','veryslow']
out = [file_output]

final_list = command + map_input + text_mark_720p + text_mark_480p + text_mark_360p + text_mark_240p + out
#final_list = command + map_input2 + target_stream_720p + target_stream_480p + out
launch_str = ' '.join(final_list)


subprocess.run(launch_str, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

print(launch_str)

