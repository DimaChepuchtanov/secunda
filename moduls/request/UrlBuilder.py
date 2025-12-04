from random import randint

from datetime import datetime, timedelta
from typing import Dict, Any, Optional


class UrlBuilder:
    def __init__(self):
        self.base_url = "https://iss.moex.com/iss/statistics/engines/futures/markets/indicativerates/securities/"

    def validate_params(func):
        """
        Decorator to validate and set default parameters for URL generation.

        Validates the 'params' and 'code' arguments, setting defaults where necessary.
        """
        def validate_param(user_params: Optional[Dict]) -> Dict:
            default_params = {
                "from": datetime.strftime(datetime.now() - timedelta(days=30), "%Y-%m-%d"),
                "tail": datetime.strftime(datetime.now(), "%Y-%m-%d"),
                "iss.json": "extended",
                "iss.meta": "off",
                "limit": randint(10, 30),
                "start": 0,
                "sort_order": "DESC"
            }

            if user_params is None:
                user_params = default_params
            else:
                for key, value in default_params.items():
                    if key not in user_params:
                        user_params[key] = value
                    else:
                        if key == "from":
                            try:
                                datetime.strptime(user_params[key], "%Y-%m-%d")
                            except Exception:
                                print("Ошибка формата начало даты. Приводим к дефолту")
                                user_params.update({key: value})
                        else:  # ВИДИМОСТЬ ВЫБОРА :)
                            user_params.update({key: value})

            return user_params

        def validate_code(code: str) -> str:
            try:
                from_, to = code.split('/')[0], code.split('/')[1]
                if not from_.isupper() or not to.isupper():
                    print("Ошибка валидации кода. Нужно писать с заглавной буквы")
                    return None
            except Exception as e:
                print(e)
                return None
            return code

        def wrapper(*args, **kwargs):
            "Проверка параметров. Обязательных и автоподстава для неточных"

            user_params: dict = validate_param(kwargs.get("params"))
            code: str = validate_code(kwargs.get('code'))

            if user_params is None or code is None:
                return None

            result = func(args[0], params=user_params, code=code)
            return result
        return wrapper

    @validate_params
    def generate_url(self, params: Dict[str, Any], code: str) -> str:
        """
        Generate a complete URL by appending parameters to the base URL.

        Args:
            params (Dict[str, Any]): Query parameters for the URL.
            code (str): The security code.

        Returns:
            str: The generated URL.
        """
        url = self.base_url + code + '.json?'

        for key, value in params.items():
            url += f"{key}={value}&"

        url = url.removesuffix("&")

        return url
