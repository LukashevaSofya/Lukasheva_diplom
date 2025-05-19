import pandas as pd
import numpy as np
import urllib.request, datetime

today = datetime.date.today()  # Устанавливаем текущую дату в переменную 'today'


def get_page(url):  # Определяем функцию, принимающую URL в качестве аргумента
    req = urllib.request.Request(url, headers={
        'Connection': 'Keep-Alive',
        'Accept': 'text.py/html, application/xhtml+xml, */*',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
    })  # Создаём объект запроса с заданными заголовками
    opener = urllib.request.urlopen(req)  # Выполняем запрос по указанному URL
    page = opener.read()  # Считываем содержимое страницы
    return page


def download_data(index: str): # Определяем функцию загрузки данных по индексу
    url = 'http://quotes.money.163.com/service/chddata.html?code=%s&start=20090101&end=%s&fields=' \
          'TCLOSE;HIGH;LOW;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER' % (index, today.strftime("%Y%m%d"))

    raw_data = get_page(url)  # Загружаем данные с помощью функции get_page
    raw_data = str(raw_data, 'utf-8')# Преобразуем байты в строку (UTF-8)
    file = open('raw_data.txt', 'w')
    file.write(raw_data)
    file.close()

    df = pd.read_csv('raw_data.txt') # Загружаем файл как DataFrame с помощью pandas
    df.drop(columns=['Код акции', 'Название'], axis=1, inplace=True)
    df.columns = ['date', 'close', 'high', 'low', 'pre_close', 'range', 'change', 'vol', 'turnover']
   # Переименовываем оставшиеся столбцы для удобства
    df = df.replace(to_replace='None', value=np.nan)  # Replace any 'None' values with 'NaN'
    df.dropna(axis=0, how='any', inplace=True)  # Drop any rows that contain missing values
    df[['pre_close', 'range', 'change']] = df[['pre_close', 'range', 'change']].astype(float)
    # Преобразуем выбранные столбцы к типу float
    df.to_csv('raw_data.csv', index=False)
    return df
