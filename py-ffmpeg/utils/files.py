# Ищёт в папке видео файлы, возвращает информацию об основном видео потоке
import os
from about_video import file_info

folder_path = '\\\stal-sap-video\\Videocontent\\providers'
#print(folder_path)

# Выгрузим все файлы вообще в файл:
out_file = open('out\stal-sap-video-info.txt', 'w', encoding='utf-8')
state_count = 0

for path, dirs, files in os.walk(folder_path):
    for f in files:
        f_path = os.path.join(path, f)
        f_name, f_ext = os.path.splitext(f_path)
        f_size = os.path.getsize(f_path)
        #print(f'{f_path}\t{f_ext}')
        out_string = file_info(f_path)
        print(out_string)
        out_file.write(f'{out_string}\n')
        #out_file.write(f'{f_path}\t{f_ext}\t{f_size}\n')
        #print(f'{f_name}\t{f_ext}')

out_file.close() 


