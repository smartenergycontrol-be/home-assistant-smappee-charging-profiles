import aiohttp
import logging

_LOGGER = logging.getLogger(__name__)

class OAuth2Client:
    def __init__(self, data):
        self.client_id = data.get("client_id")
        self.client_secret = data.get("client_secret")
        self.access_token = data.get("access_token")
        self.refresh_token = data.get("refresh_token")
        self.token_url = "https://app1pub.smappee.net/dev/v1/oauth2/token"
        self.base_url = "https://app1pub.smappee.net/dev/v3"  # Base URL for API requests
        self.username = data.get("username")
        self.password = data.get("password")

    async def authenticate(self):
        """Authenticate using client credentials and return tokens."""
        _LOGGER.debug("Starting authentication with client_id: %s, username: %s", self.client_id, self.username)

        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "grant_type": "password",
                    "username": self.username,
                    "password": self.password,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                }

                _LOGGER.debug("Sending payload: %s", payload)

                response = await session.post(self.token_url, data=payload)

                _LOGGER.debug("Received response: %s", await response.text())

                if response.status != 200:
                    _LOGGER.error("Authentication failed with status: %s", response.status)
                    return None

                tokens = await response.json()
                _LOGGER.debug("Received tokens: %s", tokens)

                if "access_token" in tokens:
                    self.access_token = tokens["access_token"]
                    self.refresh_token = tokens["refresh_token"]
                    return tokens
                else:
                    _LOGGER.error("No access token in response: %s", tokens)
                    return None

        except Exception as e:
            _LOGGER.error("Exception occurred during authentication: %s", e)
            return None

    async def _refresh_token(self):
        """Refresh the access token if needed."""
        async with aiohttp.ClientSession() as session:
            response = await session.post(self.token_url, data={
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            })
            tokens = await response.json()
            self.access_token = tokens.get("access_token")
            self.refresh_token = tokens.get("refresh_token")
            _LOGGER.debug("Refreshed tokens: %s", tokens)
