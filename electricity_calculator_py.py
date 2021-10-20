#!/usr/bin/env python
# coding: utf-8

# In[1]:


#get_ipython().system('pip install openpyxl #для работы с функциями файлов Excel в pandas является установка модуля openpyxl')
#Источник: https://tonais.ru/library/zapis-dataframe-v-list-excel


# In[2]:


import pandas as pd
import datetime
import numpy as np


# In[118]:


def today_season():
    """
        функция возвращает какой на данный день сезон в году
    """
    #Время года
    winter = ['10','11','12','1','2','3','4']
    summer = ['5','6','7','8','9']
    
    today = datetime.date.today() #сегодняшняя дата

    #today = datetime.date(2021,9,30) #временно для работы проги
    today_month = str(today.month)
    if today_month in summer:
        season = 'Summer'
    elif today_month in winter:
        season = 'Winter'
    else:
        print('Нет данных')

    print(f'Сейчас сезон - {season}, сегодня дата - {today}')
    return season, today


# In[73]:


#Создание функции формата для сохранения в формате exel
#создание объекта записи в excel format
def out_in_exel(today,season):
    """
    функция сохраняет данные в excel file
    """
    i = 0
    print("Создается таблица счетчиков: ")
    season = season
    columns = ['Date','T1','T2','T3','Tsum','Tarif','T1_kvt','T2_kvt','T3_kvt','Tsum_kvt','money(rub)']
    d = today
    t1 = float(input('Введите показания счетчика Т1: '))
    t2 = float(input('Введите показания счетчика T2: '))
    t3 = float(input('Введите показания счетчика T3: '))
    tsum = float(input('Введите показания счетчика Tобщ: '))
    tarif = season
    t1_kvt = 0
    t2_kvt = 0
    t3_kvt = 0
    tsum_kvt = 0
    money = 0
    data = [[d,t1,t2,t3,tsum,tarif,t1_kvt,t2_kvt,t3_kvt,tsum_kvt,money]]
    df = pd.DataFrame(data,columns = columns)
    
    writer = pd.ExcelWriter('output_el_calc_2.xlsx')

    #Записываем dataframe to excel
    df.to_excel(writer)

    #save the excel
    writer.save()
    i +=1
    return i
#out_in_exel()



#запись в exel
def write_exel(df, d = None,t1 = None,t2 = None,t3 = None,tsum = None,tarif = None, t1_kvt = None,
                     t2_kvt = None,t3_kvt = None,tsum_kvt = None, money = None):
    """
        Принимает на вход датафрейм, данные по умолчанию. 
        На выходе должени быть изменненый файл exel с новыми данными
    """
    
    
    len_idx = len(df.index)
    #print(len_idx)
    df.loc[len_idx + 1] = [d,t1,t2,t3,tsum,tarif,t1_kvt,t2_kvt,t3_kvt,tsum_kvt,money]
    
    writer = pd.ExcelWriter('output_el_calc_2.xlsx')

    #Записываем dataframe to excel
    df.to_excel(writer)

    #save the excel
    writer.save()
    
    
    
''''''   
# Reading (считывани) excel format dataframe

def read_out_excel():
    """
    функция возвращает считанный excel файл
    """
    return pd.read_excel('output_el_calc_2.xlsx',index_col = 0)
#df_elec = read_out_excel()
#df_elec


# In[8]:


# Функция создание файла csv для считывания и установки тарифов
def create_tarif_csv(today):  
    """
        функция создает файл csv тарифов нулевой
    """
    today = today
    tf_250 = float(input('Лето до 250 кВт: '))
    tf_250_800 = float(input('Лето от 250 до 800 кВт: '))
    tf_up800 = float(input('Лето свыше 800 кВт: '))
    tf_w5000 = float(input('Зима до 5000 кВт: '))
    tf_w_up5000 = float(input('Зима свыше 5000 кВт: '))
    dict_tarif = {
        'date':today,
        'price_kvt_sum_250':tf_250,
        'price_kvt_sum_800':tf_250_800,
        'price_kvt_sum_up800':tf_up800,
        'price_kvt_wint_5000':tf_w5000,
        'price_kvt_wint_up5000':tf_w_up5000

    }
    #create dataframe
    df = pd.DataFrame([dict_tarif])

    #save df_tarif in csv format
    df.to_csv('tarif_elec_2.csv',index=False)

    
#Функция считывания файла тариф
def read_tarif_csv():
    return pd.read_csv('tarif_elec_2.csv')


# In[59]:


def read_counter():
    """
        функция считывает новые данные электросчетчика
    """
    print("Введите данные счетчика.")
    while True:
        try:
            print()
            t1_new = float(input('Введите новые показания счетчика Т1: '))
            t2_new = float(input('Введите навые показания счетчика T2: '))
            t3_new = float(input('Введите новые показания счетчика T3: '))
            tsum_new = float(input('Введите новые показания счетчика Tобщ: '))
            print()
            print(f'Проверяем показания счетчика:\nT1: {t1_new}\nT2: {t2_new}\nT3: {t3_new}\nTsum: {tsum_new}')
            y = input("Если все в порядке жми 'Д', если нет жми 'Н' ")
            if y.upper() == 'Д':
                break
            elif y.upper() == 'Н':
                print()
                print('Корректировка:')
            else:
                print()
                print('Выберите нужную букву.')
        except:
            print('Неправильный ввод данных показаний счетчика')
            
    return t1_new,t2_new,t3_new,tsum_new
        


# In[31]:


def tarif_on_elec():
    """
        Уточняем у пользователя его тарифы и если нужно меняем
    """
    df_tarif = pd.read_csv('tarif_elec_2.csv')
    wint_5000 = df_tarif.price_kvt_wint_5000.tolist()[-1]
    wint_up5000 = df_tarif.price_kvt_wint_up5000.tolist()[-1]
    sum_250 = df_tarif.price_kvt_sum_250.tolist()[-1]
    sum_800 = df_tarif.price_kvt_sum_800.tolist()[-1]
    sum_up800 = df_tarif.price_kvt_sum_up800.tolist()[-1]    
    
    print(f"Ваш тариф на электричество:\n     летний:\n     - до 250 кВт: {sum_250} р.\n     - от 250 до 800 кВт: {sum_800} р.\n     - свыше 800 кВт: {sum_up800} р.\n    зимний:\n     - до 5000 кВт: {wint_5000} р.\n     - свыше 5000 кВт: {wint_up5000} р.")
    print()
    #Нужна будет проверка ввода данных
    b = False

    while b == False:
        try:
            c = int(input('Если нужны изменения нажми "1", если нет нажми "0" '))
            if (c==0)or(c==1):
                if c == 1:
                    while True:
                        #Тариф зимний
                        try:
                            wint_5000 = float(input('Зима до 5000 кВт: ')) #тариф зимний до 5000 квт в мессяц
                            
                        except:
                            print('Не правильный ввод данных до 5000 кВт')
                            print('Начнем сначала :)')
                            break
                        try:
                            wint_up5000 = float(input('Зима свыше 5000 кВт: ')) #тариф зимний свыше 5000 квт в месяц
                            
                        except:
                            print('Не правильный ввод данных свыше 5000 кВт')
                            print('Начнем сначала :)')
                            break
                        #Тариф летний 
                        try:
                            sum_250 = float(input('Лето до 250 кВт: ')) # до 250 кВт
                            
                        except:
                            print('Не правильный ввод лето до 250 кВт')
                            print('Начнем сначала :)')
                            break
                        try:
                            sum_800 = float(input('Лето от 250 до 800 кВт: ')) # от 250 до 800 кВт
                            
                        except:
                            print('Не правильный ввод лето от 250 до 800 кВт')
                            print('Начнем сначала :)')
                            break
                        try:
                            sum_up800 = float(input('Лето свыше 800 кВт: ')) # свыше 800 кВт
                            
                        except:
                            print('Не правильный ввод лето свыше 800 кВт')
                            print('Начнем сначала :)')
                            break
                        
                        break
                    print()
                    print("Проверяем.")
                    print()
                    print(f"Ваш тариф на электричество:\n                     летний:\n                     - до 250 кВт: {sum_250} р.\n                     - от 250 до 800 кВт: {sum_800} р.\n                     - свыше 800 кВт: {sum_up800} р.\n                    зимний:\n                     - до 5000 кВт: {wint_5000} р.\n                     - свыше 5000 кВт: {wint_up5000} р.")
                    
                    date = datetime.date.today()
                    len_idx = df_tarif.index.tolist()[-1]
                    df_tarif.loc[len_idx + 1] = [date,sum_250,sum_800,sum_up800,
                                                 wint_5000,wint_up5000]

                    df_tarif.to_csv('tarif_elec_2.csv', index = False)
                    
                else:

                    print('Продолжаем')                   
                    
                    #df_tarif.to_csv('tarif_elec.csv', index = False)
                    b = True
        except:
            print("Нужно ввести цифры 0 или 1")


    
    return wint_5000, wint_up5000, sum_250, sum_800, sum_up800


# In[106]:


#Функции расчета летнего периода
#функция расчета kvt и денег до 250
def do_250(t1_kv,t2_kv,t3_kv,tsum_kv,sum_250):
    kv_1_250 = (250 * t1_kv)/tsum_kv    
    r_1_250 = kv_1_250 * sum_250 *1.5
    
    kv_2_250 = (250 * t2_kv)/tsum_kv    
    r_2_250 = kv_2_250 * sum_250 * 1.
    
    kv_3_250 = (250 * t3_kv)/tsum_kv    
    r_3_250 = kv_3_250 * sum_250 * 0.4
    
    Rsum_250 = r_1_250 + r_2_250 + r_3_250
    
    return kv_1_250,kv_2_250,kv_3_250,round(Rsum_250,0)



#функция расчета kvt и денег до 800
def ot_250_do_800(t1_kv,t2_kv,t3_kv,tsum_kv,sum_800):
    kv_1_800 = (550 * t1_kv)/tsum_kv    
    r_1_800 = kv_1_800 * sum_800 *1.5
    
    kv_2_800 = (550 * t2_kv)/tsum_kv    
    r_2_800 = kv_2_800 * sum_800 * 1.
    
    kv_3_800 = (550 * t3_kv)/tsum_kv    
    r_3_800 = kv_3_800 * sum_800 * 0.4
    
    Rsum_800 = r_1_800 + r_2_800 + r_3_800
    
    return kv_1_800,kv_2_800,kv_3_800,round(Rsum_800,0)

#функция расчета больше 800 kvt лето
def up_800(t1_kv,t2_kv,t3_kv, kv_1_250,kv_2_250,kv_3_250, kv_1_800,kv_2_800,kv_3_800, sum_up800):
    kv_1_u800 = t1_kv - kv_1_250 - kv_1_800
    r_1_u800 = kv_1_u800 * sum_up800 * 1.5
    
    kv_2_u800 = t2_kv - kv_2_250 - kv_2_800
    r_2_u800 = kv_2_u800 * sum_up800 * 1
    
    kv_3_u800 = t3_kv - kv_3_250 - kv_3_800
    r_3_u800 = kv_3_u800 * sum_up800 * 0.4
    
    Rsum_u800 = r_1_u800 + r_2_u800 + r_3_u800
    return kv_1_u800, kv_2_u800, kv_3_u800, round(Rsum_u800,0)
    
#Функция расчета денег за полученые квт
def money_sum(Rsum_250,Rsum_800,Rsum_u800):   
    R_sum = Rsum_250 + Rsum_800 + Rsum_u800
    return round(R_sum,0)


#Функции расчета зимнего периода
def w_5000(tsum_kv, wint_5000):
    R_5000 = tsum_kv * wint_5000
    return round(R_5000,0)

#Функция расчета зиммнего периода больше 5000квт
def w_u5000(tsum_kv, wint_5000,wint_up5000):
    delta_tsum_kv = tsum_kv - 5000
    R_5000 = 5000 * wint_5000
    R_u5000 = delta_tsum_kv * wint_up5000
    R_sum_w = R_5000 + R_u5000
    
    return round(R_sum_w,0)


# In[115]:



def main():
    #Получаем дату и сезон
    season, today = today_season()

    #Проверка на первый вход в базу счетчиков
    try:
        df_elec = read_out_excel()
    except:
        print('Вы первый раз в этой программе')
        out_in_exel(today,season)

    df_elec = read_out_excel()
    print('Поехали дальше')
    # df_elec


    #Проверка на первый вход базу тарифы
    try:
        df_tarif = read_tarif_csv()
    except:
        print("Вы первый раз создаете файл тарифов")
        create_tarif_csv(today)

    df_tarif = read_tarif_csv()
    print('Поехали дальше')
    #df_tarif


    #Считываем или записываем новые счетчики
    t1_new,t2_new,t3_new,tsum_new = read_counter()


    #Получение данных по тарифам и если надо изменение и внесение в таблицу
    wint_5000, wint_up5000, sum_250, sum_800, sum_up800 = tarif_on_elec()




    #
    #Read data from database df_elec
    t1 = df_elec.T1.tolist()[-1]
    t2 = df_elec.T2.tolist()[-1]
    t3 = df_elec.T3.tolist()[-1]
    tsum = df_elec.Tsum.tolist()[-1]

    #Высчитываю разницу киловат
    #t1_kvt,t2_kvt,t3_kvt,tsum_kvt,money
    t1_kv = t1_new - t1
    t2_kv = t2_new - t2
    t3_kv = t3_new - t3
    tsum_kv = tsum_new - tsum
    #print(t1_kv,t2_kv,t3_kv,tsum_kv)


    #Расчеты
    if season == 'Summer'and tsum_kv <= 250:
        print("Input 1")
        _,_,_,R_sum_250 = do_250(t1_kv,t2_kv,t3_kv,tsum_kv,sum_250)
        write_exel(df_elec,today,t1_new,t2_new,t3_new,tsum_new,season,t1_kv,t2_kv,t3_kv,tsum_kv,R_sum_250)
        print(f"Платить {R_sum_250}, кВт1 = {t1_kv}, кВт2 = {t2_kv}, кВт3 = {t3_kv}, кВт_общ = {tsum_kv}")
    elif season == 'Summer'and(250<tsum_kv<=800):
        print("Input 2")
        _,_,_,R_sum_250 = do_250(t1_kv,t2_kv,t3_kv,tsum_kv,sum_250)
        _,_,_,R_sum_800 = ot_250_do_800(t1_kv,t2_kv,t3_kv,tsum_kv,sum_800)
        R_250_800 = R_sum_250 + R_sum_800
        write_exel(df_elec,today,t1_new,t2_new,t3_new,tsum_new,season,t1_kv,t2_kv,t3_kv,tsum_kv,R_250_800)
        print(f"Платить {R_250_800}, кВт1 = {t1_kv}, кВт2 = {t2_kv}, кВт3 = {t3_kv}, кВт_общ = {tsum_kv}")
    elif season == 'Summer'and tsum_kv > 800:
        print("Input 3")
        kv_1_250,kv_2_250,kv_3_250,Rsum_250 = do_250(t1_kv,t2_kv,t3_kv,tsum_kv,sum_250)

        kv_1_800,kv_2_800,kv_3_800,Rsum_800 = ot_250_do_800(t1_kv,t2_kv,t3_kv,tsum_kv,sum_800)

        _, _, _, Rsum_u800 = up_800(t1_kv,t2_kv,t3_kv, kv_1_250,kv_2_250,kv_3_250, kv_1_800,kv_2_800,kv_3_800, sum_up800)

        R_sum = money_sum(Rsum_250,Rsum_800,Rsum_u800)
        write_exel(df_elec,today,t1_new,t2_new,t3_new,tsum_new,season,t1_kv,t2_kv,t3_kv,tsum_kv,R_sum)
        print(f"Платить {R_sum}, кВт1 = {t1_kv}, кВт2 = {t2_kv}, кВт3 = {t3_kv}, кВт_общ = {tsum_kv}")
    elif season == 'Winter'and tsum_kv <= 5000:
        print("Input 4")
        R_w_5000 = w_5000(tsum_kv, wint_5000)
        write_exel(df_elec,today,t1_new,t2_new,t3_new,tsum_new,season,t1_kv,t2_kv,t3_kv,tsum_kv,R_w_5000)
        print(f"Платить {R_w_5000}, кВт1 = {t1_kv}, кВт2 = {t2_kv}, кВт3 = {t3_kv}, кВт_общ = {tsum_kv}")
    elif season == 'Winter'and tsum_kv > 5000:
        print("Input 5")
        R_sum_w = w_u5000(tsum_kv, wint_5000,wint_up5000)
        write_exel(df_elec,today,t1_new,t2_new,t3_new,tsum_new,season,t1_kv,t2_kv,t3_kv,tsum_kv,R_sum_w)
        print(f"Платить {R_sum_w}, кВт1 = {t1_kv}, кВт2 = {t2_kv}, кВт3 = {t3_kv}, кВт_общ = {tsum_kv}")
    else:
        print('Ошибка в водных данных')
    #
    
    

# if __name__ == '__main__':
#     main()

    

