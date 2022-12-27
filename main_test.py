from geopy.geocoders import Nominatim #Подключаем библиотеку
geolocator = Nominatim(user_agent="Tester") #Указываем название приложения (так нужно, да)
# adress = str(input('Введите адрес: \n')) #Получаем интересующий нас адрес
location = geolocator.geocode('Бровари Шевченка 12') #Создаем переменную, которая состоит из нужного нам адреса
print(location) #Выводим результат: адрес в полном виде
print(location.latitude, location.longitude) #И теперь выводим GPS-координаты нужного нам адреса

