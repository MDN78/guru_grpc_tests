from google.protobuf import empty_pb2

from internal.pb.niffler_currency_pb2_pbreflect import NifflerCurrencyServiceClient


def test_get_all_currencies(grpc_client: NifflerCurrencyServiceClient) -> None:
    """ Передаем запрос с пустым телом"""
    response = grpc_client.get_all_currencies(empty_pb2.Empty())
    print(response)
    assert len(response.allCurrencies) == 4