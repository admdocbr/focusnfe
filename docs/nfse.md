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


#### `NFSeRequest`
Request schema for issuing a new NFS-e.

| Field | Type | Description |
| :--- | :--- | :--- |
| `data_emissao` | `datetime.datetime \| None` | Date and time of issuance in ISO 8601 format |
| `natureza_operacao` | `str` | Nature of the operation (e.g., 1 for Tributação no município) |
| `optante_simples_nacional` | `bool` | Whether the company is opted for Simples Nacional |
| `prestador` | `NFSePrestador` | Provider details |
| `tomador` | `NFSeTomador` | Customer/Taker details |
| `servico` | `NFSeServico` | Service details |

#### `NFSeResponse`
Response schema for NFS-e creation or consultation.

| Field | Type | Description |
| :--- | :--- | :--- |
| `status` | `str` | Status of the NFSe (e.g., processando_autorizacao, autorizado, erro) |
| `ref` | `str \| None` | Unique reference provided in the request |
| `cnpj_prestador` | `str \| None` | Provider's CNPJ |
| `numero` | `str \| None` | Official NFSe number |
| `codigo_verificacao` | `str \| None` | Verification code for authenticity |
| `data_emissao` | `str \| None` | Date and time of issuance |
| `url` | `str \| None` | URL to view the NFSe in HTML |
| `url_danfse` | `str \| None` | URL to download the PDF (DANFSe) |
| `caminho_xml_nota_fiscal` | `str \| None` | URL or path to the XML file |
| `mensagem` | `str \| None` | Error or informational message |
| `erros` | `list[dict \| None` | List of validation errors if status is erro |

#### `NFSePrestador`
Service Provider details for NFS-e.

| Field | Type | Description |
| :--- | :--- | :--- |
| `cnpj` | `str` | CNPJ of the service provider |
| `inscricao_municipal` | `str` | Municipal registration of the provider |
| `codigo_municipio` | `str` | 7-digit IBGE code of the provider's city |

#### `NFSeTomador`
Service Taker (Customer) details for NFS-e.

| Field | Type | Description |
| :--- | :--- | :--- |
| `cpf` | `str \| None` | CPF of the taker (if person) |
| `cnpj` | `str \| None` | CNPJ of the taker (if company) |
| `razao_social` | `str` | Name or company name of the taker |
| `email` | `str \| None` | Email for sending the NFSe |
| `endereco` | `NFSeTomadorEndereco` | Address details of the taker |

#### `NFSeTomadorEndereco`
Address details for the service taker (customer).

| Field | Type | Description |
| :--- | :--- | :--- |
| `logradouro` | `str` | Street name/Address |
| `numero` | `str` | Address number |
| `bairro` | `str` | Neighborhood/Bairro |
| `codigo_municipio` | `str` | 7-digit IBGE code of the taker's city |
| `uf` | `str` | State abbreviation (e.g., SP) |
| `cep` | `str` | Postal/CEP code |
| `complemento` | `str \| None` | Address complement |

#### `NFSeServico`
Service details, including tax information and values.

| Field | Type | Description |
| :--- | :--- | :--- |
| `valor_servicos` | `float` | Total value of the service |
| `item_lista_servico` | `str` | LC 116/2003 service item code (e.g., 1.05) |
| `discriminacao` | `str` | Detailed description of the service |
| `codigo_municipio` | `str` | IBGE code where the service was provided |
| `aliquota` | `float \| None` | ISS tax rate percentage |
| `iss_retido` | `bool \| None` | Whether ISS is withheld by the taker |
| `valor_pis` | `float \| None` | PIS tax amount |
| `valor_cofins` | `float \| None` | COFINS tax amount |
| `valor_inss` | `float \| None` | INSS tax amount |
| `valor_ir` | `float \| None` | IR (Income Tax) amount |
| `valor_csll` | `float \| None` | CSLL tax amount |
| `outras_retencoes` | `float \| None` | Other tax retentions |
| `desconto_incondicionado` | `float \| None` | Unconditional discount |
| `desconto_condicionado` | `float \| None` | Conditional discount |

<!-- API_DOCS_END -->
