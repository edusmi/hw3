import pandas as pd
import random as rnd
import math

# чтение данных из файлов
data = pd.read_csv("data.csv", sep=",", skiprows=[0], header=None)
context = pd.read_csv("context.csv", sep=",", skiprows=[0], header=None)
# кол-во users
users = 40
# вариант (по таблице моей группы)
usersNumber = 32


# вычисляет среднее значение для каждого user
def average_func():
    averageArray = []
    for j in range(0, 40):
        average = 0
        films = 0
        for i in range(1, 31):
            if data[i][j] != -1:
                average += data[i][j]
                films += 1
        averageArray.append(round((average / films), 3))
    return averageArray


# рассчет метрики для косинуса из data
def sim(x, y):
    sum = 0
    sumSqrtX = 0
    sumSqrtY = 0
    for i in range(1, 31):
        if data[i][x] != -1 and data[i][y] != -1:
            sum += data[i][x] * data[i][y]
            sumSqrtX += pow(data[i][x], 2)
            sumSqrtY += pow(data[i][y], 2)
    return round((sum / (math.sqrt(sumSqrtX) * math.sqrt(sumSqrtY))), 3)


# ф-ия используется, если нет рекоменд. фильма
def max_movie(user):
    flag = False
    for y in range(1,31):
        if data[y][user] == 5 and flag is False:
            max_film = y
            flag = True
    return max_film


# №1

usersAverage = average_func()

# вычисление метрики для users
metric = {}
for jy in range(users):
    if jy != usersNumber - 1:
        metric.update({(jy + 1): sim(usersNumber - 1, jy)})

# сортируем данные, чтобы получить список метрик от high до low
sortedd = sorted(metric.items(), key=lambda x: x[1], reverse=True)

# получ. 5 соответ. пользователей
user = []
additionalMovies = []
for x in range(5):
    user.append(sortedd[x][0])
    additionalMovies.append(max_movie(sortedd[x][0] - 1))
# финальный список фильмов
movies = {}

filmsList = []
for x in range(1,31):
    if data[x][usersNumber-1] == -1:
        filmsList.append(x)

# финальный рейтинг
ri = 0
for i in filmsList:

    chisl = 0 #числитель в формуле
    znam = 0# знаменатель
    ri = 0
    for x in user:
        if data[i][x-1] != -1:
            chisl += sortedd[x][1] * (data[i][x-1] - usersAverage[x-1])
            znam += abs(sortedd[x][1])
    ri = round((usersAverage[usersNumber - 1] + chisl / znam), 3)
    movies.update({i:round(ri,3)})

# сортируем фильмы от самого high до самого low
rangeMovies = sorted(movies.items(), key=lambda x: x[1], reverse=True)

# №2

weekdays = [" Mon", " Tue", " Wed", " Thu", " Fri"]
weekends = [" Sat", " Sun"]

# алгоритм ищет фильмы, котор. лучше посмотреть в будни
moviesDays = []
for i in filmsList:
    Weekday = 0 #2 вероятности - для будней и выходных
    Weekend = 0
    count = 0
    for x in range(0,40):
        if x != usersNumber - 1:
            if context[i][x] != " -":
                count+=1
                if context[i][x] in weekdays:
                    Weekday += 1
                else:
                    Weekend += 1
    if (Weekday/count) > (Weekend/count):
        moviesDays.append(i)

# рекомендуем 1 фильм к просмотру в будни из дз№1 (если это real)

userAverage = usersAverage[usersNumber - 1]
flag = True
for x in rangeMovies:
    if x[0] in moviesDays and abs(x[1] - userAverage) > 0 and flag:
        flag = False
        recommendedMovie = x[0]

#flag = True
if not flag:
    print("Рекомендуемый фильм к просмотру:",recommendedMovie)
else:
    print("Посмотрите то, что оценили Ваши товарищи: Фильм №",rnd.choice(additionalMovies) )
for x in rangeMovies:
    print('Фильм № '+ str(x[0])+':'+ str(round(x[1],3)))