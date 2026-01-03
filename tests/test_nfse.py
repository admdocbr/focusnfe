import pytest

from focusnfe import FocusNFe
from focusnfe.models.nfse import NFSeRequest, NFSeResponse


@pytest.fixture
def client():
    return FocusNFe(api_token="test_token")


@pytest.fixture
def sample_nfse_data():
    return {
        "natureza_operacao": "1",
        "optante_simples_nacional": True,
        "prestador": {"cnpj": "00000000000191", "inscricao_municipal": "123456", "codigo_municipio": "3550308"},
        "tomador": {
            "cnpj": "00000000000191",
            "razao_social": "Test Customer",
            "endereco": {
                "logradouro": "Test Street",
                "numero": "123",
                "bairro": "Test Bairro",
                "codigo_municipio": "3550308",
                "uf": "SP",
                "cep": "01001000",
            },
        },
        "servico": {
            "valor_servicos": 100.0,
            "item_lista_servico": "1.05",
            "discriminacao": "Test service",
            "codigo_municipio": "3550308",
        },
    }


def test_create_nfse_success(client, requests_mock, sample_nfse_data):
    mock_response = {"status": "processando_autorizacao", "ref": "ref123", "cnpj_prestador": "00000000000191"}
    requests_mock.post(f"{client.SANDBOX_URL}/nfse?ref=ref123", json=mock_response, status_code=201)

    response = client.create_nfse("ref123", sample_nfse_data)
    assert isinstance(response, NFSeResponse)
    assert response.status == "processando_autorizacao"
    assert response.ref == "ref123"


def test_create_nfse_with_model(client, requests_mock, sample_nfse_data):
    mock_response = {"status": "processando_autorizacao", "ref": "ref123"}
    requests_mock.post(f"{client.SANDBOX_URL}/nfse?ref=ref123", json=mock_response, status_code=201)

    request_model = NFSeRequest(**sample_nfse_data)
    response = client.create_nfse("ref123", request_model)
    assert response.status == "processando_autorizacao"


def test_get_nfse_success(client, requests_mock):
    mock_response = {
        "status": "autorizado",
        "numero": "1234",
        "codigo_verificacao": "ABC-123",
        "url_danfse": "http://test.com/pdf",
    }
    requests_mock.get(f"{client.SANDBOX_URL}/nfse/ref123", json=mock_response)

    response = client.get_nfse("ref123")
    assert response.status == "autorizado"
    assert response.numero == "1234"
    assert response.url_danfse == "http://test.com/pdf"


def test_cancel_nfse_success(client, requests_mock):
    mock_response = {"status": "cancelado"}
    requests_mock.delete(f"{client.SANDBOX_URL}/nfse/ref123", json=mock_response)

    response = client.cancel_nfse("ref123")
    assert response.status == "cancelado"
