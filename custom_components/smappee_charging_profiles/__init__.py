import logging
from homeassistant.helpers import config_entry_oauth2_flow
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

DOMAIN = "smappee_charging_profiles"
SMAPPEE_API = None  # Placeholder for API client

async def async_setup_entry(hass: HomeAssistant, entry):
    """Set up Smappee Charging Profiles from a config entry."""
    global SMAPPEE_API
    SMAPPEE_API = SmappeeApiClient(entry.data)
    hass.data[DOMAIN] = SMAPPEE_API

    async def set_charging_mode_service(call):
        """Handle the service call to set charging mode."""
        serial = call.data["serial"]
        mode = call.data["mode"]
        limit = call.data.get("limit", 0)
        await SMAPPEE_API.set_charging_mode(serial, mode, limit)

    hass.services.async_register(DOMAIN, "set_charging_mode", set_charging_mode_service)

    return True
