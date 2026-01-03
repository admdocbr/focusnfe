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

## API Reference

<!-- API_DOCS_START -->

### Client Methods


#### create\_nfse

```python
def create_nfse(reference: str,
                nfse_data: dict[str, Any] | NFSeRequest) -> NFSeResponse
```

Issue a new NFS-e (Service Invoice).

**Arguments**:

- `reference`: Unique internal reference for the invoice.
- `nfse_data`: Dictionary or NFSeRequest model containing NFS-e data.

**Returns**:

An NFSeResponse model instance.

<a id="focusnfe.client.FocusNFe.get_nfse"></a>


#### get\_nfse

```python
def get_nfse(reference: str) -> NFSeResponse
```

Consult an existing NFS-e by its internal reference.

**Arguments**:

- `reference`: The unique reference provided during creation.

**Returns**:

An NFSeResponse model instance.

<a id="focusnfe.client.FocusNFe.cancel_nfse"></a>


#### cancel\_nfse

```python
def cancel_nfse(reference: str) -> NFSeResponse
```

Cancel an authorized NFS-e.

**Arguments**:

- `reference`: The unique reference of the invoice.

**Returns**:

An NFSeResponse model instance.



### Models


## NFSeRequest Objects

```python
class NFSeRequest(FocusNFeBaseModel)
```

Request schema for issuing a new NFS-e.

<a id="focusnfe.models.nfse.NFSeResponse"></a>


## NFSeResponse Objects

```python
class NFSeResponse(FocusNFeBaseModel)
```

Response schema for NFS-e creation or consultation.


## NFSePrestador Objects

```python
class NFSePrestador(FocusNFeBaseModel)
```

Service Provider details for NFS-e.

<a id="focusnfe.models.nfse.NFSeTomadorEndereco"></a>


## NFSeTomador Objects

```python
class NFSeTomador(FocusNFeBaseModel)
```

Service Taker (Customer) details for NFS-e.

<a id="focusnfe.models.nfse.NFSeServico"></a>


## NFSeTomadorEndereco Objects

```python
class NFSeTomadorEndereco(FocusNFeBaseModel)
```

Address details for the service taker (customer).

<a id="focusnfe.models.nfse.NFSeTomador"></a>


## NFSeServico Objects

```python
class NFSeServico(FocusNFeBaseModel)
```

Service details, including tax information and values.

<a id="focusnfe.models.nfse.NFSeRequest"></a>

<!-- API_DOCS_END -->
