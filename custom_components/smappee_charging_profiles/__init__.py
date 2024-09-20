import logging
from homeassistant.core import HomeAssistant

from .oauth import SmappeeApiClient
from .const import DOMAIN  # Import your domain from a const.py file

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry):
    """Set up Smappee Charging Profiles from a config entry."""
    try:
        api_client = SmappeeApiClient(entry.data)
    except KeyError as e:
        _LOGGER.error(f"Missing authentication token: {e}")
        return False

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = api_client

    return True