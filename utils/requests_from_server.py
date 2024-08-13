import httpx
import requests

async def request_get_endpoint_from_server(url, params=None):
    try:
        if 'localhost' in url:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)
                response = response.json()
        else:
            response = requests.get(url, params=params).json()

        return response
    except Exception as e:
        raise e
