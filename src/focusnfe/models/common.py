from pydantic import BaseModel, ConfigDict, Field


class FocusNFeBaseModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)


class WebhookResponse(FocusNFeBaseModel):
    id: str = Field(..., description="Unique identification of the webhook")
    url: str = Field(..., description="URL that will receive the requests")
    event: str = Field(..., description="Type of event that triggers the webhook (e.g., nfe, nfse)")
