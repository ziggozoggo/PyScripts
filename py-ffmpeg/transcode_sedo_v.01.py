# Точки в названии тоже нельзя! Пробелы нельзя!  С русскими файлами не работает флюсоник
# Транскодирование видео файла Один поток -> N потоков; H.264
# Операция выполняетя поочерёдно; всё прост.
# Алгоритм:
# 1. Получение списка файлов из заданной директории
# 2. Простое кодирование файла в H.264 с заданными параметрами (CFR: 23)
# 3. Анализ файла, получение информации о:
#       - разрешении видео;
#       - битрейде видео;
#       - битрейде аудио;
# 4. Определение числа и разрешения выходных потоков
# 5. Транскодирование, формирование ссылки
# 6. Журналирование
# Сообщение ffmpeg: More than 1000 frames duplicated
# Предлагается использовать фильтр -vf mpdecimate продолжительность будет та же, дублирование кадров будет исключено
import os, subprocess, datetime
import ffmpeg
import json

# Файлы
PROVIDER = 'NEO'
COURSE_CODE = 'HR2274_NT'
FOLDER_PATH = 'C:\\_myProgs\\Flussonic\\Courses\\NEO\\HR2274_NT'
#file_name = "C:\\_myProgs\\PyScripts\\source\\kiberbezopasnost_test_720p.mp4"
# Вместо FILE_OUTPU исопльзуй output_file_name()
#FILE_OUTPUT = "C:\\_myProgs\\PyScripts\\out\\out_2_VSlow_New.mp4"

TMP_FILE = 'C:\\_myProgs\\Flussonic\\Courses\\TEST2\\HR2274_NT\\mini.mp4'
TMP_FILE2 = 'C:\\_myProgs\\Flussonic\\Courses\\TEST2\\HR2274_NT\\mini_1stpass.mp4'
TMP_FILE3 = 'C:\\_myProgs\\Flussonic\\Courses\\TEST2\\HR2274_NT\\big_file.mp4'
TMP_FILE4 = 'C:\\_myProgs\\Flussonic\\Courses\\TEST2\\HR2274_NT\\FINAL\\mini_M.mp4'
TMP_FILE5 = 'C:\\_myProgs\\Flussonic\\Courses\\TEST2\\HR2274_NT\\FINAL\\video1_M.mp4'

# Параметры журналирования (вкл/выкл):
LOG_ALL = True


# Параметры ФС
# Папка для файлов первого преобразования (исходный файл -> H.264, AAC 128 Kbit/s)
FOLDER_PRE_PASS = '\\PRE'
# Папка для продуктивных файлов (H.264, AAC 128 Kbit/s -> многопоточный)
FOLDER_FINAL_PASS = '\\FINAL'
# Ссылка на файл:
# 'https://study-video.severstal.com/Vprod/flussonic.asp?stream=SEDO/MB/kiberbezopasnost_test/mini_1stpass_1stpass.mp4'
FINISH_LINK = 'https://study-video.severstal.com/Vprod/flussonic.asp?stream=SEDO/'

# Справочники и начальные значения
# Путь до ffmpeg; 
FFMPEG_EXE = "C:\\Progs\\ffmpeg-4.4-full_build\\bin\\ffmpeg.exe"
# Путь до ffprobe (утилита для получения информации о файле)
FFPROBE_EXE = "C:\\Progs\\ffmpeg-4.4-full_build\\bin\\ffprobe.exe"
# Видео файлы
ALLOW_FILE_TYPES = ['.m4v', '.mov', '.mp4', '.webm', '.wmv']
# Матрица каналов
BANDWICH_MATRIX = {
    'EDGE': 200000,
    'ASDL': 282000,
    '3G': 692000,
    '4G': 1511000,
    'Wi-Fi': 3968000,
    'Norm': 7800000,
}
# Матрица расширений (height) - кодируем только в них
RES_MATRIX = {
    '1080p': 1080,
    '720p': 720,
    '480p': 480,
    '360p': 360,
    '240p': 240,
}
# Матрица расширений (height) - исключения
RES_MATRIX_SKIP = {
    '980p': 960,
    '700p': 700,
    '682p': 682,
    '576p': 576,
    '540p': 540,
    '362p': 362,
    '252p': 252,
}

# Матрица частоты кадров (ffprobe возвращает строковый параметр)
RES_MATRIX_FRAMERATE = {
    '1499/50': 30,
    '15/1': 15,
    '24/1': 24,
    '25/1': 25,
    '2997/100': 30,
    '30/1': 30,
    '3000/1001': 30,
    '30303/1000': 30,
    '50/1': 50,
    '60/1':60,
}


# Параметры ffmpeg
PRESET = 'slower'
# Для тестов:
#PRESET = 'veryfast'
CRF = '23'
SCALE_FACTOR = 'trunc(oh*a/2)*2'
AUDIO_BITRATE = '128k'
MOVFLAGS = '+faststart'


# Функции
# Выбираем видео-файлы из папки
def get_files(files_path):
    ''' Выбирает все файлы заданного расширения в папке
        Вход: папка/раздел
        Выход: список файлов (с полным путём до них)
    '''
    decode_log('I', files_path, 'Выборка видео файлов из директории')
    output_list = []
    for path, dirs, files in os.walk(files_path):
        for f in files:
            f_path = os.path.join(path, f)
            f_name, f_ext = os.path.splitext(f_path)
            if f_ext in ALLOW_FILE_TYPES:
                output_list.append(f_path)
                #f_size = os.path.getsize(f_path)  
                #print(f'{f_path} {f_size}')
    decode_log('I', files_path, 'Выборка завершена, количество:', f'{str(len(output_list))}')
    return output_list

# Генерим финальную ссылку
def create_link(file_name, provider, course_code):
    """[summary]

    Args:
        finish_folder ([type]): [description]

    Returns:
        [type]: [description]
    """ 
    dir_name = f'{os.path.dirname(file_name)}\\' 
    link_file = f'{dir_name}links.txt'

    with open(link_file, 'a', encoding='utf-8') as file_object:
        file_object.write(f'{FINISH_LINK}{provider}/{course_code}/{os.path.basename(file_name)}\n')

# Определяем параметры видео-потока: разрешение (height), битрейт, частоту кадров
def get_h264_file_info(file_path):
    '''Возвращает информацию о видео-файле:
        - height (высота разрешения)
        - текущий битрейт (видео v_bit_rate, аудио a_bit_rate)
        - частота кадров v_frame_rate
      Вход: путь до файла
   '''
    msg_type = 'I'
    decode_log(msg_type, file_path, 'Получение информации о файле')
    output_dict = {}
    try:
        json_data = json.dumps(ffmpeg.probe(file_path,FFPROBE_EXE), sort_keys=True, indent=4)
        video_file_data = json.loads(json_data)
        # Список искомых параметров, видео:
        height = 'height'
        bit_rate = 'bit_rate'
        frame_rate = 'r_frame_rate'
        for stream in video_file_data['streams']:
            if stream['codec_type'] == 'video':
                output_dict['v_height'] = stream[height]
                output_dict['v_bit_rate'] = stream[bit_rate]
                output_dict['v_frame_rate'] = stream[frame_rate]
            else: 
                output_dict['a_bit_rate'] = stream[bit_rate]
    except:
        decode_log('E', file_path, 'Получение информации о файле', 'Возникла ошибка')
    try:
        log_string = str(output_dict['v_height']) + 'p' + ' ' + str(output_dict['v_bit_rate']) + ' ' + str(output_dict['v_frame_rate']) + ' ' + 'a_bitrate ' + str(output_dict['a_bit_rate'])
    except:
        msg_type = 'E'
        log_string = 'ERROR'
    decode_log(msg_type, file_path, 'Данные о файле получены', f'{log_string}')
    return output_dict

# Первичное перекодирование в h.264 (пусть будет для всех) + аудио приводим к 128 Kbit/s
# для аудио: ffmpeg -i input_file -c:a libfdk_aac -b:a 128k output
def first_decode_h264(file_path, output_file_name):
    '''Первичная обработка файла:
        Видео: CRF 23; Аудио: 128 kbit/s
        Результат - файл в tmp директории'''
    file_data = get_h264_file_info(file_path)

    decode_log('I', file_path, 'Старт предварительного кодирования')
    
    # Простая перекодировка H.264
    ffmpeg_arguments = ['-preset', PRESET, '-c:v', 'libx264', '-crf', CRF]
    ffmpeg_audio_arg = []   
    
    if 'a_bit_rate' in file_data:
        if int(file_data['a_bit_rate']) > 127882:
            # собираем параметры декодирования аудио
            ffmpeg_audio_arg = ['-c:a', 'aac', '-b:a', AUDIO_BITRATE]

    command = [FFMPEG_EXE, '-y', '-i',  file_path,'-preset', PRESET, '-movflags', MOVFLAGS]
    final_list = command + ffmpeg_arguments + ffmpeg_audio_arg
    launch_str = ' '.join(final_list) + ' ' + output_file_name
    subprocess.run(launch_str, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    decode_log('I', file_path, 'Создан файл: ', f'{output_file_name}')
    
# Опеределение выходного файла
def output_file_name(file_path, code_pass = 1):
    """Путь и название целевого файла

    Args:
        file_path ([str]): [путь до исходного файла]
        code_pass ([int]): [тип кодирования (1 - первичное, 2 - продуктивное)]
    Returns:
        [str]: [строка с полным именем файла]
    """       
    decode_log('I', file_path, 'Определим название целевого файла', f'Прогон: {code_pass}')
    # Определяем целевые директории
    if code_pass == 1:
        dir_name = f'{os.path.dirname(file_path)}{FOLDER_PRE_PASS}\\'
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
    elif code_pass == 2:
        dir_name = f'{os.path.dirname(file_path)}{FOLDER_FINAL_PASS}\\'
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
    
    f_full_name = os.path.basename(file_path)
    try:
        f_name = f_full_name.split('.')[0]
        f_ext = f_full_name.split('.')[1]
    except:
        decode_log('E', file_path, 'Целевой файл: ', 'Ошибка')
        print('Unknown Error')
    #f_name, f_ext = os.path.splitext(file_path)
    # Разное название файла, в зависимости от прогона
    if code_pass == 1:
        out_file_name = f'{dir_name}{f_name}_H264_pre.{f_ext}'
    elif code_pass == 2:
        out_file_name = f'{dir_name}{f_name}_M.{f_ext}'
    decode_log('I', file_path, 'Целевой файл: ', f'Прогон: {code_pass} {out_file_name}')
    return out_file_name


#first_decode_h264(tmp_file)
#print(output_file_name(tmp_file))

# Вычисляем число потоков выходного файла
def get_final_streams_data(first_pass_file_path):
    
    decode_log('I', first_pass_file_path, 'Вычисление числа потоков')
    file_data = get_h264_file_info(first_pass_file_path)
    # определяем параметры:
    bitrate = int(file_data['v_bit_rate'])
    height_p = int(file_data['v_height'])
    frame_rate = RES_MATRIX_FRAMERATE[file_data['v_frame_rate']]
    # строка параметров запуска ffmpeg
    target_streams = []
    mapping_streams = []
    # максимальное число потоков:
    max_streams = 1
    for key in BANDWICH_MATRIX:
        if bitrate >= BANDWICH_MATRIX[key]:
            max_streams +=1
        else:
            break
    if max_streams >= 6:
        max_streams = 5
    decode_log('I', first_pass_file_path, 'Потоков:',f'{str(max_streams)}')

    # Определяем маппинг для ffmpeg
    for i in range(0, max_streams):
        mapping_streams.append(['-map', '0:0'])
    # Не забываем про аудиодорожку:
    mapping_streams.append(['-map', '0:1'])
    
    for i in range(0,max_streams):
        if i == 0:
            # Для 720p и меньше режем частоту кадров до 25
            if height_p <= 720 and frame_rate > 25:
                target_streams.append([f'-c:v:{i}', 'libx264', f'-crf:{i}', CRF, f'-r:v:{i}', '25'])
            else:
                target_streams.append([f'-c:v:{i}', 'libx264', f'-crf:{i}', CRF])
        else:
            new_height_p = next_res(height_p)
            # Для 720p и меньше режем частоту кадров до 25
            if new_height_p <= 720 and frame_rate > 25:
                if new_height_p != 0:
                    target_streams.append([f'-c:v:{i}', 'libx264', f'-crf:{i}', CRF, f'-filter:v:{i}', f'scale={SCALE_FACTOR}:{new_height_p}', f'-r:v:{i}', '25'])
                    height_p = new_height_p
                else:
                    break
            else:
                if new_height_p != 0:
                    target_streams.append([f'-c:v:{i}', 'libx264', f'-crf:{i}', CRF, f'-filter:v:{i}', f'scale={SCALE_FACTOR}:{new_height_p}'])
                    height_p = new_height_p
                else:
                    break

    # Списки в строку:
    mapping_streams_str = ''
    target_streams_str = ''
    for map in mapping_streams:
        mapping_streams_str += ' ' + ' '.join(map)
    
    for stream in target_streams:
        target_streams_str += ' ' + ' '.join(stream)
    result_parameters = mapping_streams_str + target_streams_str
    decode_log('I', first_pass_file_path, 'Строка для запуска ffmpeg сформирована')
    return result_parameters

# Журнал
def decode_log(msg_type, file_path, operation_name, data=''):
    """Запись действий в журнал transcode_sedo.log
    Коневая директория: FOLDER_PATH

    Args:
        msg_type ([str]): [код сообщения, E/W/I]
        file_path ([str]): [полный путь до файла]
        operation_name ([str]): [код, ИД функции, операции]
        data ([str]): [данные, результат операции]
    """    
    log_file_path = f'{FOLDER_PATH}\\transcode_sedo.log'
    
    if LOG_ALL:
        timestamp = datetime.datetime.now()
        with open(log_file_path, 'a', encoding='utf-8') as file_object:
            file_object.write(f'{msg_type}:\t{timestamp}\t{file_path}\t{operation_name}\t{data}\n')
        #print(f'{msg_type}: {timestamp} {file_path} {operation_name} {data}\n')
    else:
        pass



def next_res(height_p, first_pass_file_path = ''):
    """Определение следующего расширения по высоте (p)
    от большего к меньшему

    Args:
        height_p ([int]): Раширение по высоте
        first_pass_file_path ([type]): это не нужно
    Возвращает:
        Расширение по высоте (int) 
        либо 0 - если вариантов больше нет или разрешение отсутствует в матрицах
    """        
    decode_log('I', first_pass_file_path, 'Ищем следующее разрешение, текущее: ', f'{height_p}')
    key_res_matrix_list = list(RES_MATRIX.keys())
    # Проверим, не является ли текущее разрешение не стандартым
    if height_p in RES_MATRIX_SKIP.values():
        # если да - определяем близкое разрешение "вниз"
        if height_p == RES_MATRIX_SKIP['252p']:
            height_p = RES_MATRIX['240p']
        elif height_p == RES_MATRIX_SKIP['362p']:
            height_p = RES_MATRIX['360p']
        elif height_p == RES_MATRIX_SKIP['540p']:
            height_p = RES_MATRIX['480p']
        elif height_p == RES_MATRIX_SKIP['576p']:
            height_p = RES_MATRIX['480p']
        elif height_p == RES_MATRIX_SKIP['682p']:
            height_p = RES_MATRIX['480p']
        elif height_p == RES_MATRIX_SKIP['700p']:
            height_p = RES_MATRIX['480p']
        elif height_p == RES_MATRIX_SKIP['980p']:
            height_p = RES_MATRIX['720p'] 
    else:
        try:
            for i in range(0, len(key_res_matrix_list)):
                if height_p == RES_MATRIX[key_res_matrix_list[i]]:
                    height_p = RES_MATRIX[key_res_matrix_list[i+1]]
                    break
        except:
            # Вышли за пределы RES_MATRIX
            height_p = 0
    # Защита от дурака:
    if height_p > 1080:
        height_p = 0           
    decode_log('I', first_pass_file_path, 'Нашли: ', f'{height_p}')
    return height_p

def decode_finish(file_path, output_file_name):
    """

    Args:
        file_path ([type]): [description]
        output_file_name ([type]): [description]
    """
    decode_log('I', file_path, 'Старт финального кодирования')
    # Команда для запуска ffmpeg:
    command = [FFMPEG_EXE, '-y', '-i', file_path,'-preset', PRESET, '-movflags', MOVFLAGS]
    final_streams = get_final_streams_data(file_path)
    command_str = ' '.join(command)
    launch_str = f'{command_str} {final_streams} {output_file_name}'
    subprocess.run(launch_str, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    decode_log('I', file_path, 'Создан файл:', f'{output_file_name}')


#decode_log(TMP_FILE2,'delete')
# test_multi = get_final_streams_data(TMP_FILE2)
# out_file = output_file_name(TMP_FILE2)
# command = [FFMPEG_EXE, '-i', TMP_FILE2,'-preset', PRESET, '-movflags', MOVFLAGS, '-hide_banner']
# command_str = ' '.join(command)
# launch_str = f'{command_str} {test_multi} {out_file}'
# subprocess.run(launch_str, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

#print(output_file_name(TMP_FILE3))
#first_decode_h264(TMP_FILE)

#print(get_h264_file_info(TMP_FILE2))

def decode_files(folder_path):
    """Главная функция, запускает весь процесс

    Args:
        folder_path ([str]): [каталог, видео файлы которого будем кодировать]
    """    
    decode_log('I', folder_path, f'START ffmpeg preset {PRESET}')
    # Сначала получим список файлов:
    files_list = get_files(folder_path)

    # Теперь тупо в лоб, по очереди перебираем файлы и деколируем их.
    # Долго и прямолинейно
    for file in files_list:
        # Первый проход:
        # Сначала получим и сохраним новое имя файла:
        pre_file_name = output_file_name(file, 1)
        # Запустим конвертацию:
        first_decode_h264(file, pre_file_name)
        # Второй проход
        # Сначала получим и сохраним новое имя финального файла:
        fin_file_name = output_file_name(file, 2)
        # Поехали!
        decode_finish(pre_file_name,fin_file_name)
        # Создаём ссылку
        create_link(fin_file_name, PROVIDER, COURSE_CODE)
    decode_log('I', folder_path, 'FINISH')


decode_files(FOLDER_PATH)

#print(get_files(FOLDER_PATH))