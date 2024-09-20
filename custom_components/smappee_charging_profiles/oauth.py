import aiohttp

class SmappeeApiClient:
    def __init__(self, data):
        self.client_id = data.get("client_id")
        self.client_secret = data.get("client_secret")
        self.access_token = data.get("access_token")
        self.refresh_token = data.get("refresh_token")
        self.token_url = "https://app1pub.smappee.net/dev/v1/oauth2/token"

    async def authenticate(self):
        """Authenticate using client credentials and return tokens."""
        async with aiohttp.ClientSession() as session:
            response = await session.post(self.token_url, data={
                "grant_type": "password",
                "username": self.client_id,
                "password": self.client_secret,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            })
            tokens = await response.json()

            # Check if authentication succeeded
            if "access_token" in tokens:
                self.access_token = tokens["access_token"]
                self.refresh_token = tokens["refresh_token"]
                return tokens
            else:
                return None
