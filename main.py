from typing import Dict, Any

import pandas as pd

from moduls.request.UrlBuilder import UrlBuilder
from moduls.request.RequestHandler import RequestHandler
from moduls.request.ResponseParser import ResponseParser
from moduls.ExcelGenerate import ExcelGenerate
from moduls.request.sender import Sender


class Main:
    def __init__(self, secid: Dict[str, Any]):
        """
        Initialize the Main class with security IDs.

        Args:
            secid (Dict[str, Any]): Dictionary of security IDs and their parameters.
        """
        self.url_build = UrlBuilder()
        self.request = RequestHandler()
        self.response = ResponseParser()
        self.generate_excel = ExcelGenerate()
        self.sender = Sender()

        self.secid = secid

    def get_data_form_url(self, code: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Retrieve data from a URL by building the URL, making a request, and parsing the response.

        Args:
            code (str): The security code.
            params (Dict[str, Any]): Parameters for the URL.

        Returns:
            Dict[str, Any]: Parsed response data.
        """
        url = self.url_build.generate_url(params=params, code=code)
        if not url:
            print("Ошибка программы, смотри логи")

        response = self.request.request(url=url)
        return self.response.parse(response=response)

    def first_course_delim_second_course(self, dataframes: list):
        """
        Merge two dataframes and calculate the absolute difference between their rates.

        Args:
            dataframes (list): List of dataframes to merge.

        Returns:
            pd.DataFrame: Merged dataframe with result column.
        """
        dataframe = pd.merge(dataframes[0], dataframes[1], on=["tradedate", "tradetime"], how='inner')
        dataframe['Result'] = abs(dataframe['rate_x'] - dataframe['rate_y'])

        return dataframe

    def main(self):
        """
        Main execution method to process security data and generate Excel.
        """
        dataframes = []
        for key, value in self.secid.items():
            result = self.get_data_form_url(key, value)
            dataframes.append(result)

        result = self.first_course_delim_second_course(dataframes=dataframes)

        dataframes = dataframes + [result]
        dataframes = [self.generate_excel.update_dataframe(x) for x in dataframes]

        self.generate_excel.generate_excel(dataframes)

        if len(result) % 10 == 1 and len(result) % 100 != 11:
            lines_word = "строка"
        elif 2 <= len(result) % 10 <= 4 and not (12 <= len(result) % 100 <= 14):
            lines_word = "строки"
        else:
            lines_word = "строк"

        msg = self.sender.generate_body_email(to_user="user@yandex.ru", text=f"Было рассчитано {len(result)} {lines_word}")
        self.sender.send_email(to_user="user@yandex.ru", msg=msg)


if __name__ == "__main__":
    secid = {
        "JPY/RUB": {
            "from": "21"
        },
        "USD/RUB": {
            "from": "21"
        }
    }
    main = Main(secid=secid)
    main.main()
