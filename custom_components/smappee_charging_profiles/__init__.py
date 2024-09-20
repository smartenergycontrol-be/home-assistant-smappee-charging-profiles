import logging
from homeassistant.core import HomeAssistant

from .oauth import SmappeeApiClient
from .const import DOMAIN  # Import your domain from a const.py file

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry):
    """Set up Smappee Charging Profiles from a config entry."""
    api_client = SmappeeApiClient(entry.data)
    
    # Perform any required setup tasks for your integration here
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = api_client

    return True