from __future__ import annotations

from typing import Any

from .base import BaseClient
from .models.common import WebhookResponse
from .models.nfe import NFeResponse
from .models.nfse import NFSeRequest, NFSeResponse


class FocusNFe(BaseClient):
    """
    Main FocusNFe Client for interacting with various fiscal services.

    Provides high-level methods for NF-e, NFS-e, and Webhooks.
    """

    def __init__(self, api_token: str, sandbox: bool = True):
        """
        Initialize the FocusNFe high-level client.

        :param api_token: Your FocusNFe API token.
        :param sandbox: Whether to use the sandbox/homologation environment.
        """
        super().__init__(api_token, sandbox)

    def get_webhooks(self) -> list[WebhookResponse]:
        """
        List all registered webhooks.

        :return: A list of WebhookResponse model instances.
        """
        # Note: FocusNFe webhooks might have a different path, this is an example
        response = self.get("/hooks")
        return [WebhookResponse.model_validate(hook) for hook in response]

    def create_nfe(self, reference: str, nfe_data: dict[str, Any]) -> NFeResponse:
        """
        Issue a new NF-e (Product Invoice).

        :param reference: Unique internal reference for the invoice.
        :param nfe_data: Dictionary containing NF-e data according to FocusNFe API.
        :return: An NFeResponse model instance.
        """
        # We pass response_model to the post method of BaseClient
        return self.post(f"/nfe2?ref={reference}", json_data=nfe_data, response_model=NFeResponse)

    def get_nfe(self, reference: str) -> NFeResponse:
        """
        Consult an existing NF-e by its internal reference.

        :param reference: The unique reference provided during creation.
        :return: An NFeResponse model instance.
        """
        return self.get(f"/nfe2/{reference}", response_model=NFeResponse)

    def cancel_nfe(self, reference: str, justification: str) -> NFeResponse:
        """
        Cancel an authorized NF-e.

        :param reference: The unique reference of the invoice.
        :param justification: Justification for cancellation (min 15 chars).
        :return: An NFeResponse model instance.
        """
        return self.delete(f"/nfe2/{reference}", params={"justificativa": justification}, response_model=NFeResponse)

    def create_nfse(self, reference: str, nfse_data: dict[str, Any] | NFSeRequest) -> NFSeResponse:
        """
        Issue a new NFS-e (Service Invoice).

        :param reference: Unique internal reference for the invoice.
        :param nfse_data: Dictionary or NFSeRequest model containing NFS-e data.
        :return: An NFSeResponse model instance.
        """
        data = nfse_data.model_dump() if hasattr(nfse_data, "model_dump") else nfse_data
        return self.post(f"/nfse?ref={reference}", json_data=data, response_model=NFSeResponse)

    def get_nfse(self, reference: str) -> NFSeResponse:
        """
        Consult an existing NFS-e by its internal reference.

        :param reference: The unique reference provided during creation.
        :return: An NFSeResponse model instance.
        """
        return self.get(f"/nfse/{reference}", response_model=NFSeResponse)

    def cancel_nfse(self, reference: str) -> NFSeResponse:
        """
        Cancel an authorized NFS-e.

        :param reference: The unique reference of the invoice.
        :return: An NFSeResponse model instance.
        """
        return self.delete(f"/nfse/{reference}", response_model=NFSeResponse)
