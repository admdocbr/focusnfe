from datetime import datetime

from pydantic import Field, field_validator, model_validator

from .common import FocusNFeBaseModel


class NFSePrestador(FocusNFeBaseModel):
    """
    Service Provider details for NFS-e.
    """

    cnpj: str = Field(..., description="CNPJ of the service provider")
    inscricao_municipal: str = Field(..., description="Municipal registration of the provider")
    codigo_municipio: str = Field(..., description="7-digit IBGE code of the provider's city")

    @field_validator("cnpj")
    @classmethod
    def validate_cnpj(cls, v: str) -> str:
        return cls.validate_cnpj_value(v)


class NFSeTomadorEndereco(FocusNFeBaseModel):
    """
    Address details for the service taker (customer).
    """

    logradouro: str = Field(..., description="Street name/Address")
    numero: str = Field(..., description="Address number")
    bairro: str = Field(..., description="Neighborhood/Bairro")
    codigo_municipio: str = Field(..., description="7-digit IBGE code of the taker's city")
    uf: str = Field(..., description="State abbreviation (e.g., SP)")
    cep: str = Field(..., description="Postal/CEP code")
    complemento: str | None = Field(None, description="Address complement")


class NFSeTomador(FocusNFeBaseModel):
    """
    Service Taker (Customer) details for NFS-e.
    """

    cpf: str | None = Field(None, description="CPF of the taker (if person)")
    cnpj: str | None = Field(None, description="CNPJ of the taker (if company)")
    razao_social: str | None = Field(None, description="Name or company name of the taker", max_length=115)
    email: str | None = Field(None, description="Email for sending the NFSe")
    endereco: NFSeTomadorEndereco | None = Field(None, description="Address details of the taker")

    @field_validator("cpf")
    @classmethod
    def validate_cpf(cls, v: str | None) -> str | None:
        return cls.validate_cpf_value(v)

    @field_validator("cnpj")
    @classmethod
    def validate_cnpj(cls, v: str | None) -> str | None:
        return cls.validate_cnpj_value(v)

    @model_validator(mode="after")
    def validate_identifiers(self) -> "NFSeTomador":
        if self.cpf and self.cnpj:
            raise ValueError("Only one of 'cpf' or 'cnpj' can be defined, not both.")
        if not self.cpf and not self.cnpj:
            raise ValueError("One of 'cpf' or 'cnpj' must be defined.")
        return self


class NFSeServico(FocusNFeBaseModel):
    """
    Service details, including tax information and values.
    """

    valor_servicos: float = Field(..., description="Total value of the service")
    item_lista_servico: str = Field(..., description="LC 116/2003 service item code (e.g., 1.05)")
    discriminacao: str = Field(..., description="Detailed description of the service")
    codigo_municipio: str = Field(..., description="IBGE code where the service was provided")
    aliquota: float | None = Field(None, description="ISS tax rate percentage")
    iss_retido: bool | None = Field(False, description="Whether ISS is withheld by the taker")
    valor_pis: float | None = Field(None, description="PIS tax amount")
    valor_cofins: float | None = Field(None, description="COFINS tax amount")
    valor_inss: float | None = Field(None, description="INSS tax amount")
    valor_ir: float | None = Field(None, description="IR (Income Tax) amount")
    valor_csll: float | None = Field(None, description="CSLL tax amount")
    outras_retencoes: float | None = Field(None, description="Other tax retentions")
    desconto_incondicionado: float | None = Field(None, description="Unconditional discount")
    desconto_condicionado: float | None = Field(None, description="Conditional discount")


class NFSeRequest(FocusNFeBaseModel):
    """
    Request schema for issuing a new NFS-e.
    """

    data_emissao: datetime | None = Field(None, description="Date and time of issuance in ISO 8601 format")
    natureza_operacao: str = Field(..., description="Nature of the operation (e.g., 1 for Tributação no município)")
    optante_simples_nacional: bool = Field(..., description="Whether the company is opted for Simples Nacional")
    prestador: NFSePrestador = Field(..., description="Provider details")
    tomador: NFSeTomador = Field(..., description="Customer/Taker details")
    servico: NFSeServico = Field(..., description="Service details")


class NFSeResponse(FocusNFeBaseModel):
    """
    Response schema for NFS-e creation or consultation.
    """

    status: str = Field(..., description="Status of the NFSe (e.g., processando_autorizacao, autorizado, erro)")
    ref: str | None = Field(None, description="Unique reference provided in the request")
    cnpj_prestador: str | None = Field(None, description="Provider's CNPJ")

    @field_validator("cnpj_prestador")
    @classmethod
    def validate_cnpj_prestador(cls, v: str | None) -> str | None:
        return cls.validate_cnpj_value(v)

    numero: str | None = Field(None, description="Official NFSe number")
    codigo_verificacao: str | None = Field(None, description="Verification code for authenticity")
    data_emissao: str | None = Field(None, description="Date and time of issuance")
    url: str | None = Field(None, description="URL to view the NFSe in HTML")
    url_danfse: str | None = Field(None, description="URL to download the PDF (DANFSe)")
    caminho_xml_nota_fiscal: str | None = Field(None, description="URL or path to the XML file")
    mensagem: str | None = Field(None, description="Error or informational message")
    erros: list[dict] | None = Field(None, description="List of validation errors if status is erro")
