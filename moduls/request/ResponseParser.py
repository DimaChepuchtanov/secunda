from requests.models import Response
from json import loads
import pandas as pd


class ResponseParser:
    def __init__(self):
        pass

    def validate_response(func):
        def wrapper(*args, **kwargs):
            response = kwargs.get('response')

            if response.status_code != 200:
                print("Почему не 200!")

            result = func(*args, **kwargs)
            return result
        return wrapper

    @validate_response
    def parse(self, response: Response):
        content = loads(response.content)[1]["securities"]
        headers = {key: [] for key in content[0].keys()}

        for item in content:
            for key, value in item.items():
                headers[key].append(value)

        headers[f'Дата {content[0]["secid"]}'] = headers['tradedate']
        headers[f'Курс {content[0]["secid"]}'] = headers['rate']
        headers[f'Время {content[0]["secid"]}'] = headers['tradetime']

        dataframe = pd.DataFrame(headers)
        return dataframe
