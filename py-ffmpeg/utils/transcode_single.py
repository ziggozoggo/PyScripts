import subprocess

# Файл для экспериментов
file_name = "C:\\_myProgs\\Flussonic\\Courses\\TEST2\\HR2274_NT\\mini.mp4"
# Путь до ffmpeg; PATH прописать админы не дают же
ffmpeg_exe = "C:\\Progs\\ffmpeg-4.4-full_build\\bin\\ffmpeg.exe"
# Результат эксперимента
file_output = "C:\\_myProgs\\Flussonic\\Courses\\TEST2\\HR2274_NT\\mini_1stpass.mp4"

# Интересные параметры
profile = 'high'
preset = 'slower'

# Пример
target_stream_720p = ['-c:v:0', 'libx264', '-crf:0', '18', '-maxrate:0', '3968K', '-bufsize:0', '7936K', '-filter:v:0', 
                      'scale=1280:720']

# Простая перекодировка H.264, 25 кадров
ffmpeg_arguments_25 = ['-preset', preset, '-c:v', 'libx264', '-crf', '23', '-profile', profile, '-r:v', '25' ]
# Простая перекодировка H.264
ffmpeg_arguments = ['-preset', preset, '-c:v', 'libx264', '-crf', '30', '-profile', profile]
# Простая перекодировка H.264 и изменение масштаба
ffmpeg_arguments_scale = ['-preset', preset, '-c:v', 'libx264', '-crf', '23', '-profile', profile, '-filter:v', 'scale=trunc(oh*a/2)*2:240' ]

# Запуск ffmpeg
command = [ffmpeg_exe, '-i', file_name,'-preset','veryslow','-hide_banner']
out = [file_output]

final_list = command + ffmpeg_arguments + out
launch_str = ' '.join(final_list)
print(launch_str)

subprocess.run(launch_str, stdout=subprocess.PIPE, stdin=subprocess.PIPE)