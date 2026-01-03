from __future__ import annotations

from typing import Any

from .base import BaseClient
from .models.common import WebhookResponse
from .models.nfe import NFeResponse
from .models.nfse import NFSeRequest, NFSeResponse


class FocusNFe(BaseClient):
    """
    Main FocusNFe Client
    """

    def __init__(self, api_token: str, sandbox: bool = True):
        super().__init__(api_token, sandbox)

    def get_webhooks(self) -> list[WebhookResponse]:
        """List all webhooks"""
        # Note: FocusNFe webhooks might have a different path, this is an example
        response = self.get("/hooks")
        return [WebhookResponse.model_validate(hook) for hook in response]

    def create_nfe(self, reference: str, nfe_data: dict[str, Any]) -> NFeResponse:
        """Issue a new NF-e"""
        # We pass response_model to the post method of BaseClient
        return self.post(f"/nfe2?ref={reference}", json_data=nfe_data, response_model=NFeResponse)

    def get_nfe(self, reference: str) -> NFeResponse:
        """Consult an NF-e by reference"""
        return self.get(f"/nfe2/{reference}", response_model=NFeResponse)

    def cancel_nfe(self, reference: str, justification: str) -> NFeResponse:
        """Cancel an NF-e"""
        return self.delete(f"/nfe2/{reference}", params={"justificativa": justification}, response_model=NFeResponse)

    def create_nfse(self, reference: str, nfse_data: dict[str, Any] | NFSeRequest) -> NFSeResponse:
        """Issue a new NFS-e"""
        data = nfse_data.model_dump() if hasattr(nfse_data, "model_dump") else nfse_data
        return self.post(f"/nfse?ref={reference}", json_data=data, response_model=NFSeResponse)

    def get_nfse(self, reference: str) -> NFSeResponse:
        """Consult an NFS-e by reference"""
        return self.get(f"/nfse/{reference}", response_model=NFSeResponse)

    def cancel_nfse(self, reference: str) -> NFSeResponse:
        """Cancel an NFS-e"""
        return self.delete(f"/nfse/{reference}", response_model=NFSeResponse)
