import pandas as pd
import random as rnd
import math

#считывание информации из файлов данных
data = pd.read_csv("data.csv", sep=",", skiprows=[0], header=None)
context = pd.read_csv("context.csv", sep=",", skiprows=[0], header=None)
#информация ищется для юзера 31
variant = 31
#всего юзеров
users = 40
#print(data)

#считаем среднюю оценку для каждого юзера
Average = [] #список со средними оценками
for j in range(0, 40):#для каждого юзера
    average = 0#суммарная оценка для просмотренн. фильмов юзера
    films = 0#кол-во оцененных фильмов для юзера
    for i in range(1, 31):#по всем фильмам
        if data[i][j] != -1:#если фильм просмотрен
            average += data[i][j]
            films += 1
    Average.append(round((average / films), 2))
#print(Average)

#вычисляем метрику косинуса для юзеров по формуле из условия
#функция метрики
def sim(a, b):
    sum = 0#сумма из числителя формулы
    sumSqrtA = 0#суммы корней квадратов из знаменателя формулы
    sumSqrtB = 0
    for i in range(1, 31):# для всех фильмов, если они оценены обоими юзерами
        if data[i][a] != -1 and data[i][b] != -1:
            sum += data[i][a] * data[i][b]
            sumSqrtA += pow(data[i][a], 2)
            sumSqrtB += pow(data[i][b], 2)
    return round((sum / (math.sqrt(sumSqrtA) * math.sqrt(sumSqrtB))), 3)
#само вычисление метрики для юзеров
#выглядит в формате {1: 0.85899999999999999, 2: 0.86599999999999999...}
metric = {}
for x in range(users):
    if x != variant - 1:
        metric.update({(x + 1): sim(variant - 1, x)})
# сортируем данные, чтобы получить список метрик от high до low
sortmetr = sorted(metric.items(), key=lambda x: x[1], reverse=True)
#print(metric)
#print(sortmetr)
# получ. 5 ближайших пользователей и их наивысш. фильм (по 1 на каждого)
def high_movie(user):
    flag = 0
    for y in range(1, 31):
        if data[y][user] == 5 and flag == 0:
            high_film = y
            flag = 1
    return high_film
user = []#юзеры получ.
addMovies = []#их фильмы с макс. оценкой
for x in range(5):
    user.append(sortmetr[x][0])
    addMovies.append(high_movie(sortmetr[x][0] - 1))
#print(user)
#print(addMovies)

filmsList = []#неоцененные фильмы нашего варианта
for x in range(1, 31):
    if data[x][variant-1] == -1:
        filmsList.append(x)
#print(filmsList)

# оцениваем фильмы
movies = {} #оценки для наших неоцененных фильмов: {13: 2.085, 17: 2.4910000000000001...}
for i in filmsList:
    chisl = 0  #числитель из формулы вычисления оценки
    znam = 0  #знаменатель
    ocenka = 0
    for x in user:
        if data[i][x - 1] != -1:#для неоцен. фильма
            chisl += sortmetr[x][1] * (data[i][x - 1] - Average[x - 1])
            znam += abs(sortmetr[x][1])
    ocenka = round((Average[variant - 1] + chisl / znam), 3)
    movies.update({i: round(ocenka, 3)})
print('Оценки для неоцененных фильмов User ' + str(variant) + ':')
print(movies)

'''вторая часть'''
# сортируем наши непросмотренные изначально фильмы от самого high до самого low
sortMovies = sorted(movies.items(), key=lambda x: x[1], reverse=True)

workDays = [" Mon", " Tue", " Wed", " Thu", " Fri"] #будни отдельно

#ищем фильмы, которые пользователь посмотрел бы в будни
moviesDays = []
for i in filmsList:
    Weekday = 0 #2 вероятности - для будней и выходных
    Weekend = 0
    count = 0 #счетчик просмотров
    for x in range(0, 40):#для всех user
        if x != variant - 1:#исключаем нашего юзера т.к. он ж не смотрел
            if context[i][x] != " -":#если фильм просмотрен
                count += 1
                if context[i][x] in workDays:
                    Weekday += 1
                else:
                    Weekend += 1
    if (Weekday/count) > (Weekend/count):
        moviesDays.append(i)
#print(moviesDays)

# рекомендуем 1 фильм к просмотру в будни из дз №1 (если это возможно)

ourAverage = Average[variant - 1] #средняя оценка для нашего пользователя
flag = 0
for x in sortMovies:#для всех фильмов из 1 задания полученных
    #если фильм в списке для просмотра в будни и его оценка больше средней оценки нашего юзера и флаг не изменен -
    #получаем наш фильм для рекоменд.
    if x[0] in moviesDays and abs(x[1] - ourAverage) > 0 and flag == 0:
        flag = 1
        recommendedMovie = x[0]
        print("Рекомендуемый фильм к просмотру:", recommendedMovie)

if flag == 0:# ну или же берем любой из тех, что получ. в 1 задании у похожих людей
    print("Посмотрите то, что нравится людям, похожим на Вас: Фильм №", rnd.choice(addMovies))