import pytest
import requests_mock

from focusnfe import FocusNFe, FocusNFeError
from focusnfe.models.nfe import NFeResponse


def test_client_init():
    client = FocusNFe(api_token="test_token", sandbox=True)
    assert client.api_token == "test_token"
    assert client.base_url == client.SANDBOX_URL
    assert client.session.auth == ("test_token", "")


def test_client_production_init():
    client = FocusNFe(api_token="test_token", sandbox=False)
    assert client.base_url == client.PRODUCTION_URL


def test_get_nfe_success():
    with requests_mock.Mocker() as m:
        client = FocusNFe(api_token="test_token")
        mock_response = {
            "status": "autorizado",
            "chave_nfe": "12345678901234567890123456789012345678901234",
            "numero": "1",
            "serie": "1",
        }
        m.get(f"{client.SANDBOX_URL}/nfe2/ref123", json=mock_response)

        response = client.get_nfe("ref123")
        assert isinstance(response, NFeResponse)
        assert response.status == "autorizado"
        assert response.chave_nfe == "12345678901234567890123456789012345678901234"


def test_get_nfe_error():
    with requests_mock.Mocker() as m:
        client = FocusNFe(api_token="test_token")
        m.get(f"{client.SANDBOX_URL}/nfe2/ref123", json={"mensagem": "Nota não encontrada"}, status_code=404)

        with pytest.raises(FocusNFeError) as excinfo:
            client.get_nfe("ref123")

        assert "FocusNFe API Error: Nota não encontrada" in str(excinfo.value)
        assert excinfo.value.status_code == 404


def test_create_nfe_success():
    with requests_mock.Mocker() as m:
        client = FocusNFe(api_token="test_token")
        mock_response = {"status": "processando", "chave_nfe": "12345"}
        m.post(f"{client.SANDBOX_URL}/nfe2?ref=ref123", json=mock_response, status_code=202)

        response = client.create_nfe("ref123", {"dummy": "data"})
        assert response.status == "processando"
        assert response.chave_nfe == "12345"


def test_validation_error():
    with requests_mock.Mocker() as m:
        client = FocusNFe(api_token="test_token")
        # Missing 'status' which is required in NFeResponse
        mock_response = {"chave_nfe": "12345"}
        m.get(f"{client.SANDBOX_URL}/nfe2/ref123", json=mock_response)

        with pytest.raises(FocusNFeError) as excinfo:
            client.get_nfe("ref123")

        assert "Validation Error" in str(excinfo.value)
