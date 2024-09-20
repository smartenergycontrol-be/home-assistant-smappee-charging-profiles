import aiohttp
from homeassistant.helpers import config_entry_oauth2_flow

class SmappeeApiClient:
    def __init__(self, data):
        self.client_id = data["client_id"]
        self.client_secret = data["client_secret"]
        self.access_token = data["access_token"]
        self.refresh_token = data["refresh_token"]
        self.token_url = "https://app1pub.smappee.net/dev/v1/oauth2/token"

    async def _refresh_token(self):
        """Refresh the access token."""
        async with aiohttp.ClientSession() as session:
            response = await session.post(self.token_url, data={
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            })
            tokens = await response.json()
            self.access_token = tokens["access_token"]
            self.refresh_token = tokens["refresh_token"]

    async def set_charging_mode(self, serial, mode, limit):
        """Set the charging mode of a connector."""
        await self._refresh_token()
        url = f"https://app1pub.smappee.net/dev/v3/chargingstations/{serial}/connectors/1/mode"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "mode": mode,
            "limit": {
                "unit": "AMPERE",
                "value": limit
            }
        }

        async with aiohttp.ClientSession() as session:
            response = await session.put(url, json=payload, headers=headers)
            return await response.json()
