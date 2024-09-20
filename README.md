# home-assistant-smappee-charging-profiles
# Smappee Charging Profiles Integration

This Home Assistant integration allows you to manage charging profiles for Smappee charging stations.

## Installation via HACS

1. Open HACS in your Home Assistant.
2. Go to **Custom repositories** in the HACS settings.
3. Add this repository: `https://github.com/scruysberghs/home-assistant-smappee-charging-profiles`.
4. Install the integration.

## Configuration

Add the following to your `configuration.yaml`:

```yaml
smappee_charging_profiles:
  client_id: YOUR_CLIENT_ID
  client_secret: YOUR_CLIENT_SECRET
