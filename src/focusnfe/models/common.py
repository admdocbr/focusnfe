from pydantic import BaseModel, ConfigDict, Field
from validate_docbr import CNPJ, CPF

cpf_validator = CPF()
cnpj_validator = CNPJ()


class FocusNFeBaseModel(BaseModel):
    """
    Base model for all FocusNFe request and response schemas.

    Configured to allow population by field name or alias.
    """

    model_config = ConfigDict(populate_by_name=True)

    @staticmethod
    def validate_cpf_value(v: str | None) -> str | None:
        if v is None:
            return v
        # Remove common separators before validation
        clean_v = v.replace(".", "").replace("-", "").strip()
        if not cpf_validator.validate(clean_v):
            raise ValueError(f"Invalid CPF: {v}")
        return clean_v

    @staticmethod
    def validate_cnpj_value(v: str | None) -> str | None:
        if v is None:
            return v
        # Remove common separators before validation
        clean_v = v.replace(".", "").replace("-", "").replace("/", "").strip()
        if not cnpj_validator.validate(clean_v):
            raise ValueError(f"Invalid CNPJ: {v}")
        return clean_v


class WebhookResponse(FocusNFeBaseModel):
    """
    Schema for registered webhook information.
    """

    id: str = Field(..., description="Unique identification of the webhook")
    url: str = Field(..., description="URL that will receive the requests")
    event: str = Field(..., description="Type of event that triggers the webhook (e.g., nfe, nfse)")
