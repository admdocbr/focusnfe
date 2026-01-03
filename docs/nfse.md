# NFS-e (Electronic Service Invoice) Documentation

This document describes how to use the FocusNFe library to interact with NFS-e (Municipal Service Invoices) services.

## Support Status

- [x] Create NFS-e
- [x] Consult NFS-e
- [x] Cancel NFS-e
- [ ] List NFS-e - Not implemented yet

## Usage

### Issuing an NFS-e

You can pass a raw dictionary or use the `NFSeRequest` model for better type safety.

```python
from focusnfe import FocusNFe
from focusnfe.models.nfse import NFSeRequest

client = FocusNFe(api_token="your_token")

nfse_data = {
    "natureza_operacao": "1",
    "optante_simples_nacional": True,
    "prestador": {
        "cnpj": "12345678000101",
        "inscricao_municipal": "123456",
        "codigo_municipio": "3550308"
    },
    "tomador": {
        "cnpj": "98765432000101",
        "razao_social": "Test Customer",
        "endereco": {
            "logradouro": "Test Street",
            "numero": "123",
            "bairro": "Test Bairro",
            "codigo_municipio": "3550308",
            "uf": "SP",
            "cep": "01001000"
        }
    },
    "servico": {
        "valor_servicos": 100.0,
        "item_lista_servico": "1.05",
        "discriminacao": "Test service",
        "codigo_municipio": "3550308"
    }
}

# Option 1: Using a dictionary
response = client.create_nfse(reference="ref_001", nfse_data=nfse_data)

# Option 2: Using the model
request_model = NFSeRequest(**nfse_data)
response = client.create_nfse(reference="ref_001", nfse_data=request_model)

print(f"Status: {response.status}, Ref: {response.ref}")
```

### Consulting an NFS-e

```python
response = client.get_nfse(reference="ref_001")
print(f"Status: {response.status}")
if response.url_danfse:
    print(f"PDF URL: {response.url_danfse}")
```

### Cancelling an NFS-e

```python
response = client.cancel_nfse(reference="ref_001")
print(f"Status: {response.status}")
```

## Models

We use Pydantic models to validate both requests and responses.
- `NFSeRequest`: Validation for emission.
- `NFSeResponse`: Validation for the API response.
