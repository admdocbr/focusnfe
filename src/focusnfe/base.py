import json
from datetime import date, datetime
from typing import Any, TypeVar

import requests
from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)


class FocusNFeError(Exception):
    """
    Base exception for the FocusNFe library.

    Provides human-readable messages by parsing API error responses,
    including status codes and nested detailed messages.
    """

    def __init__(self, message: str, status_code: int | None = None, response: dict[str, Any] | None = None):
        """
        Initialize the FocusNFeError.

        :param message: The high-level error message.
        :param status_code: The HTTP status code returned by the API.
        :param response: The full JSON response from the API.
        """
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)

    def __str__(self):
        """
        Format the error as a human-readable string.
        """
        msg = f"[{self.status_code}] {self.message}" if self.status_code else self.message
        if self.response and "erros" in self.response:
            extra_errors = []
            for error in self.response["erros"]:
                code = error.get("codigo")
                message = error.get("mensagem")
                if code and message:
                    extra_errors.append(f" - {code}: {message}")
                elif message:
                    extra_errors.append(f" - {message}")
            if extra_errors:
                msg += "\nDetails:\n" + "\n".join(extra_errors)
        return msg


class FocusNFeJSONEncoder(json.JSONEncoder):
    """
    Custom JSON encoder that supports date and datetime objects.

    Automatically converts these objects to their ISO 8601 string representation.
    """

    def default(self, obj):
        """
        Standard default method for JSON conversion.
        """
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)


class BaseClient:
    """
    Standard Base Client to handle HTTP communication with FocusNFe API.

    Handles authentication, environment selection, and Pydantic model validation.
    """

    SANDBOX_URL = "https://homologacao.focusnfe.com.br/v2"
    PRODUCTION_URL = "https://api.focusnfe.com.br/v2"

    def __init__(self, api_token: str, sandbox: bool = True):
        """
        Initialize the base client with API token and environment.

        :param api_token: Your FocusNFe API token.
        :param sandbox: Whether to use the sandbox/homologation environment.
        """
        self.api_token = api_token
        self.base_url = self.SANDBOX_URL if sandbox else self.PRODUCTION_URL
        self.session = requests.Session()
        self.session.auth = (api_token, "")

    def _request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
        response_model: type[T] | None = None,
    ) -> dict[str, Any] | T:
        """
        Internal method to swallow standard requests and return parsed data.

        :param method: HTTP method (GET, POST, etc).
        :param path: The API endpoint path.
        :param params: Optional query parameters.
        :param json_data: Optional JSON payload.
        :param response_model: Optional Pydantic model to validate the response.
        :return: A dictionary or a validated Pydantic model instance.
        :raises FocusNFeError: If the API returns an error or validation fails.
        """
        url = f"{self.base_url}{path}"

        try:
            # Handle JSON serialization manually if json_data is present to support date/datetime
            kwargs = {"method": method, "url": url, "params": params, "timeout": 30}
            if json_data is not None:
                kwargs["data"] = json.dumps(json_data, cls=FocusNFeJSONEncoder)
                kwargs["headers"] = {"Content-Type": "application/json"}

            response = self.session.request(**kwargs)

            response_json = {}
            if response.content:
                try:
                    response_json = response.json()
                except ValueError:
                    response_json = {"text": response.text}

            if not (200 <= response.status_code < 300):
                error_msg = response_json.get("mensagem", response_json.get("message", "API Error"))
                raise FocusNFeError(
                    message=f"FocusNFe API Error: {error_msg}", status_code=response.status_code, response=response_json
                )

            if response_model:
                try:
                    return response_model.model_validate(response_json)
                except ValidationError as e:
                    raise FocusNFeError(
                        f"Validation Error: {str(e)}", status_code=response.status_code, response=response_json
                    )

            return response_json

        except requests.RequestException as e:
            raise FocusNFeError(f"Request failed: {str(e)}")

    def get(
        self, path: str, params: dict[str, Any] | None = None, response_model: type[T] | None = None
    ) -> dict[str, Any] | T:
        """
        Perform a GET request.
        """
        return self._request("GET", path, params=params, response_model=response_model)

    def post(
        self, path: str, json_data: dict[str, Any] | None = None, response_model: type[T] | None = None
    ) -> dict[str, Any] | T:
        """
        Perform a POST request.
        """
        return self._request("POST", path, json_data=json_data, response_model=response_model)

    def put(
        self, path: str, json_data: dict[str, Any] | None = None, response_model: type[T] | None = None
    ) -> dict[str, Any] | T:
        """
        Perform a PUT request.
        """
        return self._request("PUT", path, json_data=json_data, response_model=response_model)

    def delete(
        self, path: str, params: dict[str, Any] | None = None, response_model: type[T] | None = None
    ) -> dict[str, Any] | T:
        """
        Perform a DELETE request.
        """
        return self._request("DELETE", path, params=params, response_model=response_model)
