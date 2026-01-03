import pytest
import requests

from focusnfe import FocusNFe, FocusNFeError


def test_put_request(requests_mock):
    client = FocusNFe(api_token="test_token")
    requests_mock.put(f"{client.SANDBOX_URL}/test", json={"success": True})
    response = client.put("/test", json_data={"key": "value"})
    assert response["success"] is True


def test_delete_request(requests_mock):
    client = FocusNFe(api_token="test_token")
    requests_mock.delete(f"{client.SANDBOX_URL}/test", json={"deleted": True})
    response = client.delete("/test")
    assert response["deleted"] is True


def test_non_json_response(requests_mock):
    client = FocusNFe(api_token="test_token")
    requests_mock.get(f"{client.SANDBOX_URL}/test", text="not json")
    response = client.get("/test")
    assert response["text"] == "not json"


def test_request_exception(requests_mock):
    client = FocusNFe(api_token="test_token")
    requests_mock.get(f"{client.SANDBOX_URL}/test", exc=requests.RequestException("Connection error"))
    with pytest.raises(FocusNFeError) as excinfo:
        client.get("/test")
    assert "Request failed" in str(excinfo.value)


def test_get_webhooks(requests_mock):
    client = FocusNFe(api_token="test_token")
    mock_hooks = [
        {"id": "1", "url": "http://test.com/1", "event": "nfe"},
        {"id": "2", "url": "http://test.com/2", "event": "nfse"},
    ]
    requests_mock.get(f"{client.SANDBOX_URL}/hooks", json=mock_hooks)
    hooks = client.get_webhooks()
    assert len(hooks) == 2
    assert hooks[0].id == "1"


def test_nfse_methods(requests_mock):
    client = FocusNFe(api_token="test_token")
    # Create NFSe
    requests_mock.post(f"{client.SANDBOX_URL}/nfse?ref=ref123", json={"status": "autorizado"})
    response = client.create_nfse("ref123", {"data": "foo"})
    assert response.status == "autorizado"

    # Get NFSe
    requests_mock.get(f"{client.SANDBOX_URL}/nfse/ref123", json={"status": "autorizado"})
    response = client.get_nfse("ref123")
    assert response.status == "autorizado"

    # Cancel NFSe
    requests_mock.delete(f"{client.SANDBOX_URL}/nfse/ref123", json={"status": "cancelado"})
    response = client.cancel_nfse("ref123")
    assert response.status == "cancelado"


def test_cancel_nfe(requests_mock):
    client = FocusNFe(api_token="test_token")
    mock_response = {"status": "cancelado"}
    requests_mock.delete(f"{client.SANDBOX_URL}/nfe2/ref123?justificativa=test", json=mock_response)
    response = client.cancel_nfe("ref123", "test")
    assert response.status == "cancelado"
