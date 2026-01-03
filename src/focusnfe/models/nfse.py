from pydantic import Field

from .common import FocusNFeBaseModel


class NFSePrestador(FocusNFeBaseModel):
    cnpj: str = Field(..., description="CNPJ of the service provider")
    inscricao_municipal: str = Field(..., description="Municipal registration of the provider")
    codigo_municipio: str = Field(..., description="7-digit IBGE code of the provider's city")


class NFSeTomadorEndereco(FocusNFeBaseModel):
    logradouro: str = Field(..., description="Street name/Address")
    numero: str = Field(..., description="Address number")
    bairro: str = Field(..., description="Neighborhood/Bairro")
    codigo_municipio: str = Field(..., description="7-digit IBGE code of the taker's city")
    uf: str = Field(..., description="State abbreviation (e.g., SP)")
    cep: str = Field(..., description="Postal/CEP code")
    complemento: str | None = Field(None, description="Address complement")


class NFSeTomador(FocusNFeBaseModel):
    cpf: str | None = Field(None, description="CPF of the taker (if person)")
    cnpj: str | None = Field(None, description="CNPJ of the taker (if company)")
    razao_social: str = Field(..., description="Name or company name of the taker")
    email: str | None = Field(None, description="Email for sending the NFSe")
    endereco: NFSeTomadorEndereco = Field(..., description="Address details of the taker")


class NFSeServico(FocusNFeBaseModel):
    valor_servicos: float = Field(..., description="Total value of the service")
    item_lista_servico: str = Field(..., description="LC 116/2003 service item code (e.g., 1.05)")
    discriminacao: str = Field(..., description="Detailed description of the service")
    codigo_municipio: str = Field(..., description="IBGE code where the service was provided")
    aliquota: float | None = Field(None, description="ISS tax rate percentage")
    iss_retido: bool | None = Field(False, description="Whether ISS is withheld by the taker")
    valor_pis: float | None = Field(0.0, description="PIS tax amount")
    valor_cofins: float | None = Field(0.0, description="COFINS tax amount")
    valor_inss: float | None = Field(0.0, description="INSS tax amount")
    valor_ir: float | None = Field(0.0, description="IR (Income Tax) amount")
    valor_csll: float | None = Field(0.0, description="CSLL tax amount")
    outras_retencoes: float | None = Field(0.0, description="Other tax retentions")
    desconto_incondicionado: float | None = Field(0.0, description="Unconditional discount")
    desconto_condicionado: float | None = Field(0.0, description="Conditional discount")


class NFSeRequest(FocusNFeBaseModel):
    natureza_operacao: str = Field(..., description="Nature of the operation (e.g., 1 for Tributação no município)")
    optante_simples_nacional: bool = Field(..., description="Whether the company is opted for Simples Nacional")
    prestador: NFSePrestador = Field(..., description="Provider details")
    tomador: NFSeTomador = Field(..., description="Customer/Taker details")
    servico: NFSeServico = Field(..., description="Service details")


class NFSeResponse(FocusNFeBaseModel):
    status: str = Field(..., description="Status of the NFSe (e.g., processando_autorizacao, autorizado, erro)")
    ref: str | None = Field(None, description="Unique reference provided in the request")
    cnpj_prestador: str | None = Field(None, description="Provider's CNPJ")
    numero: str | None = Field(None, description="Official NFSe number")
    codigo_verificacao: str | None = Field(None, description="Verification code for authenticity")
    data_emissao: str | None = Field(None, description="Date and time of issuance")
    url: str | None = Field(None, description="URL to view the NFSe in HTML")
    url_danfse: str | None = Field(None, description="URL to download the PDF (DANFSe)")
    caminho_xml_nota_fiscal: str | None = Field(None, description="URL or path to the XML file")
    mensagem: str | None = Field(None, description="Error or informational message")
    erros: list[dict] | None = Field(None, description="List of validation errors if status is erro")
