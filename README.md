# py_railway-navigation - просмотр маршрутов ж/д на карте (Dash + OSMnx)
## Зависимости

## Необходимые файлы
 * [Список станций](https://github.com/MichaelODeli/railway_materials/blob/main/stations_parcer/RU_stations_new.csv)
 * [Граф соединений станций - простой](https://github.com/MichaelODeli/railway_materials/blob/main/svzd_graph/full_svzd_graph.graphml.zip)
 * [Граф соединений станций - полный](https://github.com/MichaelODeli/railway_materials/blob/main/svzd_graph/simple_svzd_graph.graphml)
 * [Соседства станций](https://github.com/MichaelODeli/railway_materials/blob/main/stations_neighbourhood/svzd_sosedi.csv)   
    
 Скачивать оба файла графа соединения станций необязательно - выберите только один (прим. - полный граф использует в 7 раз больше ОЗУ - около 3 Гб на одного клента (будет исправлено в будущей версии))


## Инструкция по использованию
1. Скачать файлы и поместить в нужные папки
    * [Список станций](https://github.com/MichaelODeli/railway_materials/blob/main/stations_parcer/RU_stations_new.csv) - в подпапку `all_stations` (итоговый путь до файла - `all_stations/RU_stations_new.csv`)
    * [Граф соединений станций - простой](https://github.com/MichaelODeli/railway_materials/blob/main/svzd_graph/full_svzd_graph.graphml.zip) - в корень папки
    * [Граф соединений станций - полный](https://github.com/MichaelODeli/railway_materials/blob/main/svzd_graph/simple_svzd_graph.graphml) - в корень папки
    * [Соседства станций](https://github.com/MichaelODeli/railway_materials/blob/main/stations_neighbourhood/svzd_sosedi.csv) - в подпапку `all_stations` (итоговый путь до файла - `all_stations/svzd_sosedi.csv`)
1. Настройка проекта
    * Редактирование типа используемого графа
1. Запуск и использование проекта
    * Демонстрация навигации
