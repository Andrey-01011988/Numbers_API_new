import requests
from typing import Dict
from requests import Response


def _make_response(method: str, url: str, headers: Dict, params: Dict,
                   timeout: int) -> Response:
    """
    Запрос у сервера данных  по сформированному url
    :param method: метод запроса
    :param url: адрес страницы
    :param headers: пользовательские заголовки
    :param params: запросы
    :param timeout: задержка
    :return: response: ответ от сервера
    """
    response = requests.request(
        method,
        url,
        params=params,
        headers=headers,
        timeout=timeout,
    )

    return response


def get_date_fact(method: str, url: str, headers: Dict, params: Dict, date_day: str,
                  date_month: str, timeout: int, func=_make_response) -> Response:
    """
    Запрашивает у сервера факт о дате по сформированному адресу

    """

    url_date_fact = '{}/{}/{}/date'.format(url, date_month, date_day)

    response_date_fact = func(method, url_date_fact, headers=headers, params=params,
                              timeout=timeout)

    return response_date_fact


def get_math_fact(method: str, url: str, headers: Dict, params: Dict, number: str,
                  timeout: int, func=_make_response) -> Response:
    """
    Запрашивает у сервера факт о числе по сформированному адресу

    """

    url_math_fact = '{}/{}/math'.format(url, number)

    response_math_fact = func(method, url_math_fact, headers=headers, params=params,
                              timeout=timeout)

    return response_math_fact


def get_random_fact(method: str, url: str, headers: Dict, params: Dict,
                    timeout: int, func=_make_response) -> Response:
    """
    Запрашивает у сервера факт о числе изи заданного диапазона по сформированному адресу.
    Диапазон формируется в обработчике сообщений и предается в params

    """

    url_random_fact = '{}/random/trivia'.format(url)

    response_random_fact = func(method, url_random_fact, headers=headers, params=params,
                                timeout=timeout)

    return response_random_fact


def get_trivia_fact(method: str, url: str, headers: Dict, params: Dict, number: str,
                    timeout: int, func=_make_response) -> Response:
    """
    Запрашивает у сервера факт о числе по сформированному адресу и отправляет на сервер

    """

    url_trivia_fact = '{}/{}/trivia'.format(url, number)

    response_trivia_fact = func(method, url_trivia_fact, headers=headers, params=params,
                                timeout=timeout)

    return response_trivia_fact
