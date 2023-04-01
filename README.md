# py_railway-navigation - просмотр маршрутов ж/д на карте (Dash + OSMnx)
## Зависимости
[requirements.txt](https://github.com/MichaelODeli/py_railway-navigation/blob/main/requirements.txt)
## Необходимые файлы
 * [Список станций](https://github.com/MichaelODeli/railway_materials/blob/main/stations_parcer/RU_stations_new.csv)
 * [Граф соединений станций - простой](https://github.com/MichaelODeli/railway_materials/blob/main/svzd_graph/full_svzd_graph.graphml.zip) (предварительно распакуйте его из архива)
 * [Граф соединений станций - полный](https://github.com/MichaelODeli/railway_materials/blob/main/svzd_graph/simple_svzd_graph.graphml)
 * [Соседства станций](https://github.com/MichaelODeli/railway_materials/blob/main/stations_neighbourhood/svzd_sosedi.csv)   
    
 Скачивать оба файла графа соединения станций необязательно - выберите только один (прим. - полный граф использует в 7 раз больше ОЗУ - около 3 Гб на одного клента (будет исправлено в будущей версии))


## Инструкция по использованию
### Скачать файлы и поместить в нужные папки
* [Список станций](https://github.com/MichaelODeli/railway_materials/blob/main/stations_parcer/RU_stations_new.csv) - в подпапку `all_stations` (итоговый путь до файла - `all_stations/RU_stations_new.csv`)
* [Граф соединений станций - простой](https://github.com/MichaelODeli/railway_materials/blob/main/svzd_graph/full_svzd_graph.graphml.zip) - в корень папки
* [Граф соединений станций - полный](https://github.com/MichaelODeli/railway_materials/blob/main/svzd_graph/simple_svzd_graph.graphml) - в корень папки
* [Соседства станций](https://github.com/MichaelODeli/railway_materials/blob/main/stations_neighbourhood/svzd_sosedi.csv) - в подпапку `all_stations` (итоговый путь до файла - `all_stations/svzd_sosedi.csv`)
### Настройка проекта
* Редактирование типа используемого графа   
В первой строке файла `railway_navigation.py` есть строка следующего содержания:
```python
graph_type = 'full' # or 'simple'
```   
Используйте данный режим для личного использования (данный режим потребляет большой объем ОЗУ). В остальных случаях рекомендую использовать режим `graph_type = 'simple'` - он требует меньше ресурсов
### Запуск и использование проекта
Дерево файлов должно иметь следующий вид:
```
.
├── all_stations/
│   ├── svzd_sosedi.csv
│   └── RU_stations_new.csv
├── railway_navigation.py
└── full_svzd_graph.graphml (or simple_svzd_graph.graphml)
```
Достаточно запустить файл [railway_navigation.py](https://github.com/MichaelODeli/py_railway-navigation/blob/main/railway_navigation.py) после загрузки всех файлов и установки всех зависимостей
#### Интерфейс
![Интерфейс программы](/img/interface.png)
Карта отображается средствами Plotly, остальной интерфейс приведен инструментами Dash.   
Слева снизу вы можете выбрать станции отправления и назначения (поддерживается ввод словами - для поиска по предоставленным станциям). На данный момент предоставлена маршрутизация только по СвЖД   
![Выбор станции отправления](/img/selector.png)
## To-Do
- Отображение промежуточных станций (на данный момент - слишком ресурсоемкая реализация закомментирована в основном коде программы)
- 
