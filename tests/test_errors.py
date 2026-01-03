from focusnfe import FocusNFe, FocusNFeError


def test_focus_nfe_error_readable_message(requests_mock):
    client = FocusNFe(api_token="test_token")

    # Mock a complex error response common in FocusNFe
    error_response = {
        "codigo": "erro_validacao",
        "mensagem": "Erro de validação nos campos",
        "erros": [
            {"codigo": "E01", "mensagem": "CNPJ inválido"},
            {"codigo": "E02", "mensagem": "Município não suportado"},
        ],
    }

    requests_mock.get(f"{client.SANDBOX_URL}/test", status_code=422, json=error_response)

    try:
        client.get("/test")
    except FocusNFeError as e:
        error_str = str(e)
        assert "[422]" in error_str
        assert "Erro de validação nos campos" in error_str
        assert "E01: CNPJ inválido" in error_str
        assert "E02: Município não suportado" in error_str


def test_focus_nfe_error_simple_message(requests_mock):
    client = FocusNFe(api_token="test_token")

    requests_mock.get(f"{client.SANDBOX_URL}/test", status_code=500, json={"message": "Internal Server Error"})

    try:
        client.get("/test")
    except FocusNFeError as e:
        error_str = str(e)
        assert "[500]" in error_str
        assert "Internal Server Error" in error_str
