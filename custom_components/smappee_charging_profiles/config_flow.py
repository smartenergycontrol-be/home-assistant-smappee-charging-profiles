import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv

from .oauth import SmappeeApiClient
from .const import DOMAIN  # Make sure you have a const.py file with your domain defined

@callback
def smappee_charging_profiles_entries(hass):
    """Return the list of smappee charging profiles."""
    return {
        entry.title: entry
        for entry in hass.config_entries.async_entries(DOMAIN)
    }

class SmappeeChargingProfilesConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for smappee charging profiles."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
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

        # Authenticate with the API using the credentials
        api_client = SmappeeApiClient(user_input)
        if not await api_client.authenticate():
            return self.async_show_form(
                step_id="user",
                errors={"base": "auth_failed"}
            )

        # Store the credentials in the config entry
        return self.async_create_entry(title="Smappee Charging Profiles", data=user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return SmappeeChargingProfilesOptionsFlowHandler(config_entry)


class SmappeeChargingProfilesOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle the options flow for smappee charging profiles."""

    def __init__(self, config_entry):
        """Initialize the options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is None:
            return self.async_show_form(
                step_id="init",
                data_schema=vol.Schema({
                    vol.Required("serial", default=self.config_entry.data.get("serial")): str,
                   
