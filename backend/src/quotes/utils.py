from quotes.models import QuoteData


def validate_input_data(data):
    """
    Валидирует данные по QuoteData модели Pydantic.

    Args:
        data (dict): Входящий json.

    Returns:
        QuoteData: завалидированный json как экземпляр QuoteData.
        tuple: в случае ошибки JSON response и HTTP status code.
    """
    validated_data = QuoteData(**data)
    return validated_data
