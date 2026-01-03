# NF-e (Electronic Product Invoice) Documentation

This document describes how to use the FocusNFe library to interact with NF-e services.

## Support Status

- [x] Create NF-e
- [x] Consult NF-e
- [x] Cancel NF-e
- [ ] CC-e (Correction Letter) - Not implemented yet

## Usage

### Issuing an NF-e

```python
from focusnfe import FocusNFe

client = FocusNFe(api_token="your_token")

nfe_data = {
    "natureza_operacao": "Venda de mercadoria",
    "data_emissao": "2024-01-01T12:00:00-03:00",
    "tipo_operacao": "1", # 1-Saida, 0-Entrada
    "finalidade_emissao": "1", # 1-Normal
    "presenca_comprador": "1", # 1-Operacao presencial
    # ... more fields required by SEFAZ
}

response = client.create_nfe(reference="my_ref_001", nfe_data=nfe_data)
print(f"Status: {response.status}, Chave: {response.chave_nfe}")
```

### Consulting an NF-e

```python
response = client.get_nfe(reference="my_ref_001")
print(f"Status: {response.status}")
if response.url_pdf:
    print(f"PDF URL: {response.url_pdf}")
```

### Cancelling an NF-e

```python
response = client.cancel_nfe(reference="my_ref_001", justification="Justication for cancellation")
print(f"Status: {response.status}")
```

## Models

We use Pydantic models to validate the responses. The main response model is `NFeResponse`.
