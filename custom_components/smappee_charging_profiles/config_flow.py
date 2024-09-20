from homeassistant import config_entries
from .oauth import SmappeeApiClient

class SmappeeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=vol.Schema({
                vol.Required("client_id"): str,
                vol.Required("client_secret"): str,
                vol.Required("username"): str,
                vol.Required("password"): str
            }))
        
        api_client = SmappeeApiClient(user_input)
        await api_client.authenticate()

        return self.async_create_entry(title="Smappee Charging Profiles", data=user_input)
