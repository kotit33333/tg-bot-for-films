from KinoPoiskAPI import kinopoisk_api

kinopoisk = kinopoisk_api.KP(token='abf47b9d-8db7-4a5e-ac8f-60492e9e8180')



top500 = kinopoisk.top500()

for item in top500:
    print(item.ru_name, item.year)
