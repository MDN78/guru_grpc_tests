import pytest
import grpc
from grpc import insecure_channel

from internal.grpc.interceptors.allure import AllureInterceptor
from internal.grpc.interceptors.logging import LoggingInterceptor
from internal.pb.niffler_currency_pb2_pbreflect import NifflerCurrencyServiceClient

INTERCEPTORS = [
    LoggingInterceptor(),
    AllureInterceptor(),
]


@pytest.fixture(scope="session")
def grpc_client() -> NifflerCurrencyServiceClient:
    """ Фикстура для подключения канала """

    channel = insecure_channel('localhost:8092')
    intercept_channel = grpc.intercept_channel(channel, *INTERCEPTORS)
    return NifflerCurrencyServiceClient(intercept_channel)
