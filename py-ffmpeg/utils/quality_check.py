# Проверка качества (VMAF)
# https://www.youtube.com/watch?v=H55OoyyoJew
# ffmpeg -i compressed.mp4 -i original.mp4 -lavfi libvmaf="model_path='V\:\\ffmpeg\\bin\\vmaf_v0.6.1.json'" -f null
import subprocess

MODEL_PATH = "'C:\\\Progs\\\\ffmpeg-4.4-full_build\\\\vmaf-master\\\model\\\\vmaf_v0.6.1.json'"

MODEL_PATH2 = "'vmaf_v0.6.1.json'"
FFMPEG_EXE = "C:\\Progs\\ffmpeg-4.4-full_build\\bin\\ffmpeg.exe"

FILE_PATH_ORIGINAL = 'C:\\_myProgs\\Flussonic\\Courses\\NEO\\HR2274_NT\\1_Nachalo.mp4'
FILE_PATH_CODED = 'C:\\_myProgs\\Flussonic\\Courses\\NEO\\HR2274_NT\\PRE\\1_Nachalo_H264_pre.mp4'


# Запуск ffmpeg
command = [FFMPEG_EXE, '-i', FILE_PATH_CODED, '-i', FILE_PATH_ORIGINAL, '-lavfi', f'libvmaf="model_path={MODEL_PATH2}"', '-f', 'null', '-']
launch_str = ' '.join(command)

subprocess.run(launch_str, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
#print(launch_str)


