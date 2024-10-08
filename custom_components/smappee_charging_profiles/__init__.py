import logging
from homeassistant.core import HomeAssistant

from .oauth import OAuth2Client
from .api_client import SmappeeApiClient
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry):
    """Set up Smappee Charging Profiles from a config entry."""
    
    _LOGGER.debug("Setting up entry for Smappee Charging Profiles.")
    
    # Initialize the API client
    oauth_client = OAuth2Client(entry.data)
    api_client = SmappeeApiClient(oauth_client)
    
    # Store the API client in hass.data
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    hass.data[DOMAIN][entry.entry_id] = api_client

    # Register the set_charging_mode service (now called actions in Home Assistant)
    async def set_charging_mode_service(call):
        """Handle the action to set the charging mode."""
        serial = call.data.get("serial")
        mode = call.data.get("mode")
        limit = call.data.get("limit", 0)

        _LOGGER.debug(f"Setting charging mode for serial {serial} to {mode} with limit {limit}.")
        
        api_client = hass.data[DOMAIN][entry.entry_id]
    
        try:
            await api_client.set_charging_mode(serial, mode, limit)
            _LOGGER.debug(f"Charging mode set successfully for {serial}")
        except Exception as e:
            _LOGGER.error(f"Failed to set charging mode for {serial}: {e}")
            raise  # Ensures that the exception is re-raised and properly logged

    # Register the service/action in Home Assistant
    hass.services.async_register(DOMAIN, "set_charging_mode", set_charging_mode_service)

    return True