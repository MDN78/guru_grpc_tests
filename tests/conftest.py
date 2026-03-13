import pytest
import grpc
from grpc import insecure_channel

from internal.grpc.interceptors.allure import AllureInterceptor
from internal.grpc.interceptors.logging import LoggingInterceptor
from internal.pb.niffler_currency_pb2_pbreflect import NifflerCurrencyServiceClient
from settings.settings import Settings

INTERCEPTORS = [
    LoggingInterceptor(),
    AllureInterceptor(),
]


@pytest.fixture(scope="session")
def settings() -> Settings:
    """ Fixture for settings """
    return Settings()


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--mock", action="store_true", default=False)


@pytest.fixture(scope="session")
def grpc_client(settings: Settings, request: pytest.FixtureRequest) -> NifflerCurrencyServiceClient:
    """ Фикстура для подключения канала """
    host = settings.currency_service_host
    if request.config.getoption("--mock"):
        host = settings.wiremock_host
    channel = insecure_channel(host)
    intercept_channel = grpc.intercept_channel(channel, *INTERCEPTORS)
    return NifflerCurrencyServiceClient(intercept_channel)
