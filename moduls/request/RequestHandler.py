from requests import get
from requests.models import Response
from requests.exceptions import Timeout, ConnectionError

from untils.exceptions.request import ManyRequest, AccessIsDenied


class RequestHandler:
    def __init__(self):
        pass

    def request(self, url: str) -> Response:
        """
        Make a GET request to the specified URL with error handling.

        Args:
            url (str): The URL to request.

        Returns:
            Response or None: The response object if successful, None otherwise.

        Raises:
            AccessIsDenied: If access is denied (403).
            ManyRequest: If too many requests (429).
        """
        try:
            response = get(
                url=url,
                timeout=(3, 10)
            )

            if response.status_code == 403:
                raise AccessIsDenied()
            elif response.status_code == 429:
                raise ManyRequest()
            return response
        except (Timeout, ConnectionError):
            print("Проблемы с сетью")
            return None
        except AccessIsDenied as e:
            print("Ошибка: ", e)
            return None
        except ManyRequest as e:
            print("Ошибка: ", e)
        except Exception as e:
            print("Ошибка: ", e)
