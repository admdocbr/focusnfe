from pydantic import BaseModel, ConfigDict, Field


class FocusNFeBaseModel(BaseModel):
    """
    Base model for all FocusNFe request and response schemas.

    Configured to allow population by field name or alias.
    """

    model_config = ConfigDict(populate_by_name=True)


class WebhookResponse(FocusNFeBaseModel):
    """
    Schema for registered webhook information.
    """

    id: str = Field(..., description="Unique identification of the webhook")
    url: str = Field(..., description="URL that will receive the requests")
    event: str = Field(..., description="Type of event that triggers the webhook (e.g., nfe, nfse)")
