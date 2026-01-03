from pydantic import Field

from .common import FocusNFeBaseModel


class NFeResponse(FocusNFeBaseModel):
    """
    Schema for NF-e (Product Invoice) responses.

    Contains authorization details, SEFAZ status, and DANFE/XML URLs.
    """

    status: str = Field(..., description="Current status of the NF-e (e.g., autorizado, processando, erro)")
    status_sefaz: str | None = Field(None, description="Status code returned by SEFAZ")
    mensagem_sefaz: str | None = Field(None, description="Detailed message returned by SEFAZ")
    chave_nfe: str | None = Field(None, description="Unique access key of the NF-e")
    numero: str | None = Field(None, description="Number of the NF-e")
    serie: str | None = Field(None, description="Series of the NF-e")
    url_pdf: str | None = Field(None, description="URL to download the PDF (DANFE)")
    url_xml: str | None = Field(None, description="URL to download the XML")
    protocolo: str | None = Field(None, description="Authorization protocol number")
    caminho_xml_nota_fiscal: str | None = Field(None, description="Path to the XML file")
