from datetime import datetime

from focusnfe import FocusNFe
from focusnfe.models.nfse import NFSeRequest


def test_nfse_date_serialization(requests_mock):
    client = FocusNFe(api_token="test_token")
    requests_mock.post(f"{client.SANDBOX_URL}/nfse?ref=test_ref", json={"status": "autorizado", "ref": "test_ref"})

    # Create request with a datetime object
    data_emissao = datetime(2024, 1, 1, 12, 0, 0)
    nfse_data = {
        "data_emissao": data_emissao,
        "natureza_operacao": "1",
        "optante_simples_nacional": True,
        "prestador": {"cnpj": "00000000000191", "inscricao_municipal": "123456", "codigo_municipio": "3550308"},
        "tomador": {
            "cpf": "52998224725",
            "razao_social": "Test Customer",
            "endereco": {
                "logradouro": "Street",
                "numero": "123",
                "bairro": "Center",
                "codigo_municipio": "3550308",
                "uf": "SP",
                "cep": "01001000",
            },
        },
        "servico": {
            "valor_servicos": 100.0,
            "item_lista_servico": "1.05",
            "discriminacao": "Test",
            "codigo_municipio": "3550308",
        },
    }

    # Test with dictionary containing datetime
    client.create_nfse(reference="test_ref", nfse_data=nfse_data)

    # Check if the request body was correctly serialized to ISO format
    last_request = requests_mock.request_history[-1]
    assert "2024-01-01T12:00:00" in last_request.text


def test_nfse_model_date_serialization(requests_mock):
    client = FocusNFe(api_token="test_token")
    requests_mock.post(f"{client.SANDBOX_URL}/nfse?ref=test_ref", json={"status": "autorizado", "ref": "test_ref"})

    data_emissao = datetime(2024, 1, 1, 12, 0, 0)
    request_model = NFSeRequest(
        data_emissao=data_emissao,
        natureza_operacao="1",
        optante_simples_nacional=True,
        prestador={"cnpj": "00000000000191", "inscricao_municipal": "123456", "codigo_municipio": "3550308"},
        tomador={
            "cpf": "52998224725",
            "razao_social": "Test Customer",
            "endereco": {
                "logradouro": "Street",
                "numero": "123",
                "bairro": "Center",
                "codigo_municipio": "3550308",
                "uf": "SP",
                "cep": "01001000",
            },
        },
        servico={
            "valor_servicos": 100.0,
            "item_lista_servico": "1.05",
            "discriminacao": "Test",
            "codigo_municipio": "3550308",
        },
    )

    client.create_nfse(reference="test_ref", nfse_data=request_model)

    last_request = requests_mock.request_history[-1]
    assert "2024-01-01T12:00:00" in last_request.text
