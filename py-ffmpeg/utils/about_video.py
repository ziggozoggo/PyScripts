# Выводит информацию заданного видеофайла
import ffmpeg
import json

ffmpeg_exe = "C:\\Progs\\ffmpeg-4.4-full_build\\bin\\ffmpeg.exe"
ffprobe_exe = "C:\\Progs\\ffmpeg-4.4-full_build\\bin\\ffprobe.exe"

#file_name = '\\\stal-sap-video\\Videocontent\\providers\\8sp\\PPD0942_8sp\\02_Navstrechu_DrugDrugu_750.mp4'

# Вывод инфо в словарь, где ключ - file_name
def file_info(f_name):
    ''' Возвращает строку с информацией о формате видео файла
        file_name - полный путь до файла'''
    # Искомая информация находится по ключу streams
    # это список list, для нормального файла список имеет два элемента - видео, аудио; набор полей одинаков.
    # определение размера файла: print(dict_data['format']['size']) (в байтах)
    try:
        json_data = json.dumps(ffmpeg.probe(f_name,ffprobe_exe), sort_keys=True, indent=4)
        dict_data = json.loads(json_data)

        # Список искомых параметров, видео:
        codec_type = 'codec_type'
        height = 'height'
        width = 'width'
        r_frame_rate = 'r_frame_rate'
        bit_rate = 'bit_rate'

        out_str = f'{f_name}\t'
        v_str = ''
        a_str = ''

        for stream in dict_data['streams']:
            try:
                if stream[codec_type] == 'video':
                    #print (stream[height])
                    v_str = f'{stream[codec_type]}\t{stream[height]}\t{stream[width]}\t{stream[r_frame_rate]}\t{stream[bit_rate]}\t'
                else:
                    a_str = f'{stream[codec_type]}\t{stream[bit_rate]}'
            except:
                v_str = 'Error'
        out_str += v_str + a_str
    except:
        out_str = 'ffprobe error'
    return out_str









