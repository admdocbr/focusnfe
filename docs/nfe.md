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

## API Reference

<!-- API_DOCS_START -->

### Client Methods


#### create\_nfe

```python
def create_nfe(reference: str, nfe_data: dict[str, Any]) -> NFeResponse
```

Issue a new NF-e (Product Invoice).

**Arguments**:

- `reference`: Unique internal reference for the invoice.
- `nfe_data`: Dictionary containing NF-e data according to FocusNFe API.

**Returns**:

An NFeResponse model instance.

<a id="focusnfe.client.FocusNFe.get_nfe"></a>


#### get\_nfe

```python
def get_nfe(reference: str) -> NFeResponse
```

Consult an existing NF-e by its internal reference.

**Arguments**:

- `reference`: The unique reference provided during creation.

**Returns**:

An NFeResponse model instance.

<a id="focusnfe.client.FocusNFe.cancel_nfe"></a>


#### cancel\_nfe

```python
def cancel_nfe(reference: str, justification: str) -> NFeResponse
```

Cancel an authorized NF-e.

**Arguments**:

- `reference`: The unique reference of the invoice.
- `justification`: Justification for cancellation (min 15 chars).

**Returns**:

An NFeResponse model instance.

<a id="focusnfe.client.FocusNFe.create_nfse"></a>



### Models


## NFeResponse Objects

```python
class NFeResponse(FocusNFeBaseModel)
```

Schema for NF-e (Product Invoice) responses.

Contains authorization details, SEFAZ status, and DANFE/XML URLs.

<!-- API_DOCS_END -->
