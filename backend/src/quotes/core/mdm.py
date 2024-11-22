def send_to_mdm(data):
    """
    Отправка данных на MDM микросервис.

    Args:
        data (QuoteData): Validated data.

    Returns:
        dict: словарь из run ID и subject IDs.
        tuple: в случае ошибки JSON response и HTTP status code.
    """
    run_id = data.quote.header.runId
    response_data = {"runId": run_id, "subjectIds": ["01937646", "02948576"]}
    return response_data
