from .oauth import SmappeeApiClient
from .const import DOMAIN  # Make sure you have a const.py file with your domain defined

class SmappeeChargingProfilesConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({
                    vol.Required("client_id"): str,
                    vol.Required("client_secret"): str,
                    vol.Required("username"): str,
                    vol.Required("password"): str,
                })
            )

        # Authenticate with the API and get access and refresh tokens
        api_client = SmappeeApiClient(user_input)
        tokens = await api_client.authenticate()

        # If authentication fails
        if not tokens:
            return self.async_show_form(step_id="user", errors={"base": "auth_failed"})

        # Store the tokens in the config entry
        user_input["access_token"] = tokens["access_token"]
        user_input["refresh_token"] = tokens["refresh_token"]

        return self.async_create_entry(title="Smappee Charging Profiles", data=user_input)
