import subprocess

# Файл для экспериментов
file_name = "C:\\_myProgs\\PyScripts\\source\\Mashinist_ustanovok-Talant.mp4"
# Путь до ffmpeg; PATH прописать админы не дают же
ffmpeg_exe = "C:\\Progs\\ffmpeg-4.4-full_build\\bin\\ffmpeg.exe"
# Результат эксперимента
file_output = "C:\\_myProgs\\PyScripts\\out\\Mashinist_ustanovok-Talant_H265.mp4"

# Интересные параметры
profile = 'high'
preset = 'slow'

# Пример
target_stream_720p = ['-c:v:0', 'libx265', '-crf:0', '28', '-x265-params:0', 'vbv-maxrate=1700:vbv-bufsize=3400','-filter:v:0', 
                      'scale=1280:720']

# Простая перекодировка H.265
ffmpeg_arguments = ['-preset', preset, '-c:v', 'libx265', '-crf', '28', '-tag:v', 'hvc1' ]
# Простая перекодировка H.264 и изменение масштаба
# ffmpeg_arguments = ['-preset', preset, '-c:v', 'libx264', '-crf', '23', '-profile', profile, '-filter:v', 'scale=trunc(oh*a/2)*2:240' ]

# Запуск ffmpeg
command = [ffmpeg_exe, '-i', file_name,'-preset', preset]
out = [file_output]

final_list = command + ffmpeg_arguments + out
launch_str = ' '.join(final_list)
print(launch_str)

subprocess.run(launch_str, stdout=subprocess.PIPE, stdin=subprocess.PIPE)