import argparse
import json

"""
Структура данных, получаемых от физического объекта:

                |motion: str
                |temperature: float
                |voltage: float
                |timestamp: int                

"""
def main():

    parser = argparse.ArgumentParser(description='JSON-file maker')
    parser.add_argument('motion', type=str, help='Input \'motion\' value')
    parser.add_argument('temperature', type=float, help='Input \'temperature\' value')
    parser.add_argument('voltage', type=float, help='Input \'voltage\' value')
    parser.add_argument('timestamp', type=int, help='Input \'timestamp\' value')
    args = parser.parse_args()
    json_string = {"motion" : f"{args.motion}", "temperature" : f"{args.temperature}",
                   "voltage" : f"{args.voltage}", "timestamp" : f"{args.timestamp}"}
    with open("values.json", "w") as write_file:
        json.dump(json_string, write_file)

if __name__ == '__main__':
    main()