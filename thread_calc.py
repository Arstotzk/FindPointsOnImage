import numpy as np
from concurrent.futures import ProcessPoolExecutor
import math


class ArrSum:

    def __init__(self):
        self.arrays = []
        self.blocks = []


def calc_sum(_x, _y, _img, _template, _size):
    """
    Рачет суммы совпадения пикселя и области вокруг него с шаблоном.
    :param _x: X координата пикселя.
    :param _y: Y координата пикселя.
    :param _img: Изображение.
    :param _template: Шаблон.
    :param _size: Размер шаблона\2.
    :return: Сумма сопадения пикселя с шаблоном.
    """
    sum = 0
    xs = -1
    width, height = _img.size
    for x in range(_x - _size, _x + _size):
        xs += 1
        ys = -1
        for y in range(_y - _size, _y + _size):
            ys += 1
            if width <= x or height <= y:
                continue
            r = _img.getpixel((x, y))
            rs = _template.getpixel((xs, ys))
            if r == rs:
                sum += 1
            else:
                sum += 1 / ((r - rs) ** 2)
    return sum


def culc_sum_thread(_x, _y, _img, _template, _size, _thread, _blocks, _processing_size):
    """
    Расчет совпадения шаблона через потоки.
    :param _x: X координата начала области для обработки.
    :param _y: Y координата начала области для обработки.
    :param _img: Изображение.
    :param _template: Шаблон.
    :param _size: Размер шаблона\2.
    :param _thread: Номер потока.
    :param _blocks: Блоки для обработки.
    :param _processing_size: Область для обработки.
    :return: Массив совпадений по найденным блокам в потоке.
    """
    arr_sum = ArrSum()
    for block in _blocks:
        arr_sum.arrays.append(culc_sum_block(_x, _y, _img, _template, _size, block, _processing_size))
        arr_sum.blocks.append(block)

    #print("Поток " + str(_thread) + " завершен")
    return arr_sum


def culc_sum_block(_x, _y, _img, _template, _size, _block, _processing_size):
    """
    Расчет суммы совпадения на область в блоке.
    :param _x: X координата начала области для обработки.
    :param _y: Y координата начала области для обработки.
    :param _img: Изображение.
    :param _template: Шаблон.
    :param _size: Размер шаблона\2.
    :param _block: Номер блока.
    :param _processing_size: Область обработки.
    :return: Сумма совпадений по блоку.
    """
    _xStart = (_block * 2) - 2
    arr_sum = np.full((2, _processing_size), 0)
    for x in range(_xStart, _xStart + 2):
        for y in range(0, _processing_size):
            arr_sum[x - _xStart, y] = calc_sum(_x + x, _y + y, _img, _template, _size)
    #print("Расчет блока " + str(_block) + " завершен")
    return arr_sum


def get_blocks_by_threads(_thread_num, _thread_nums, _processing_size):
    """
    Получить блоки для расчета на поток.
    Делит область на блоки по 2 пикселя шириной, затем по потоку назначает блоки в цикле.
    Соответствие потока и блока вычисляется: номер блока = (номер потока + всего потоков * x),
    где x - номер итерации по прохождению массива блоков.
    :param _thread_num: Номер потока.
    :param _thread_nums: Всего потоков.
    :param _processing_size: Размер области обработки.
    :return: Массив блоков соответствующий номеру потока.
    """
    blocks_num = int(_processing_size / 2)
    blocks = []
    max_block_num = math.ceil(_processing_size / _thread_nums)
    for iteration in range(0, max_block_num - 1):
        block_num = int(_thread_num + _thread_nums * iteration)
        if block_num < blocks_num:
            blocks.append(block_num)
    return blocks


def start(_x_point_th, _y_point_th, _img_full, _template_full, _thread_nums, _processing_size):
    """
    Старт расчета через многопоточный процесс.
    :param _x_point_th: X координата начала области для обработки.
    :param _y_point_th: Y координата начала области для обработки.
    :param _img_full: Изображение.
    :param _template_full: Шаблон.
    :param _thread_nums: Кол-во потоков.
    :param _processing_size: Размер области обработки.
    :return: Массив с вероятностным нахождением точки по пикселям области.
    """

    executor = ProcessPoolExecutor(_thread_nums)
    params = [[], [], [], [], [], [], [], []]
    for threadNum in range(0, _thread_nums):
        params[0].append(_x_point_th)
        params[1].append(_y_point_th)
        params[2].append(_img_full)
        params[3].append(_template_full)
        params[4].append(int(_template_full.size[0] / 2))
        params[5].append(threadNum)
        params[6].append(get_blocks_by_threads(threadNum, _thread_nums, _processing_size))
        params[7].append(_processing_size)

    result = list(executor.map(culc_sum_thread, *params))

    # Собираем массивы блоков в один двумерный массив
    block_counter = 0
    block_end = int(_processing_size / 2)
    result_array = None
    while block_counter < block_end:
        for arr_sum in result:
            counter = 0
            for blockNum in arr_sum.blocks:
                if blockNum == block_counter and blockNum == 0:
                    result_array = arr_sum.arrays[counter][0]
                    result_array = np.vstack((result_array, arr_sum.arrays[counter][1]))
                    block_counter = block_counter + 1
                elif blockNum == block_counter:
                    result_array = np.vstack((result_array, arr_sum.arrays[counter][0]))
                    result_array = np.vstack((result_array, arr_sum.arrays[counter][1]))
                    block_counter = block_counter + 1
                counter = counter + 1

    return result_array
