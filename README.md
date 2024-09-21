# home-assistant-smappee-charging-profiles
# Smappee Charging Profiles Integration

This Home Assistant integration allows you to manage charging profiles for Smappee charging stations.

## Installation via HACS

1. Open HACS in your Home Assistant.
2. Go to **Custom repositories** in the HACS settings.
3. Add this repository: `https://github.com/scruysberghs/home-assistant-smappee-charging-profiles`.
4. Install the integration.


## Configuration

Configuration is done when adding the integration trough the UI
You have to enter smappee api credentials :
- api key
- secret
- username (not the email adress)
- password (same a in web portal or app)

For now the integration will onle give you a service call to set the charging speed. Other functionality can easily be addedd to make this as full features as the smappee app... 
Still too bad sensor values can not be read from the api in realtime (only 5 min averages)


