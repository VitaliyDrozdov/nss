import json
import os

from pydantic import ValidationError
from quotes.models import QuoteData

JSON_FOLDER = "./quotes"


def test_quote_validation(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        json_data = json.load(file)
    try:
        quote = QuoteData(**json_data)
        print("Данные успешно валидированы!")
        print(quote)
    except ValidationError as e:
        print("Ошибка валидации:")
        # print(json.dumps(e.errors(), indent=2))
        for error in e.errors():
            print(f"Поле: {error['loc']}, Ошибка: {error['msg']}")


def validate_all_quote_jsons(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            test_quote_validation(file_path)


if __name__ == "__main__":
    validate_all_quote_jsons(JSON_FOLDER)
