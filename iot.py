import argparse
import json
import random
import time

#                                   Практическая 7
"""
                                    Доп. задание 1
                                    
Структура данных, получаемых от физического объекта:

                |motion: str
                |temperature: float
                |voltage: float
                |timestamp: int                

"""


def catch_data():
    # ---Конфигурируем ввод с консоли
    parser = argparse.ArgumentParser(description='JSON-file maker')
    parser.add_argument('motion', type=str, help='Input \'motion\' value')
    parser.add_argument('temperature', type=float, help='Input \'temperature\' value')
    parser.add_argument('voltage', type=float, help='Input \'voltage\' value')
    parser.add_argument('timestamp', type=int, help='Input \'timestamp\' value')
    args = parser.parse_args()
    # ---Конфигурируем ввод с консоли

    # ---Запись данных в файл
    json_string = {"motion": f"{args.motion}", "temperature": f"{args.temperature}",
                   "voltage": f"{args.voltage}", "timestamp": f"{args.timestamp}"}
    with open("values.json", "w") as write_file:
        json.dump(json_string, write_file)


def read_data():
    with open('values.json', 'r', encoding='utf-8') as f:
        value = json.load(f)
        print(value)


"""
                                    Доп. задание 2
"""


def emulate_data():
    while 1:
        try:
            for x in range(1, 5):
                data = {"motion": int(random.random() * x), "temperature": random.random() * x,
                        "voltage": random.random() * x,
                        "timestamp": random.random() * x}
                jsonstring = json.dumps(data)
                print(jsonstring)
                time.sleep(0.4)
        except (KeyboardInterrupt):
            exit("Передача данных остановлена")


#                                   Практическая 7

if __name__ == '__main__':
    # catch_data()
    # read_data()
    emulate_data()
