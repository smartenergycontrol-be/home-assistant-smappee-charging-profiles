# home-assistant-smappee-charging-profiles
# Smappee Charging Profiles Integration

This Home Assistant integration allows you to manage charging profiles for Smappee charging stations.

## Installation via HACS

1. Open HACS in your Home Assistant.
2. Go to **Custom repositories** in the HACS settings.
3. Add this repository manually or use the button : [https://github.com/smartenergycontrol-be/home-assistant-smappee-charging-profiles](https://github.com/smartenergycontrol-be/home-assistant-smappee-charging-profiles/).
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=smartenergycontrol-be&repository=home-assistant-smappee-charging-profiles&category=integration)
4. Install the integration. Click download and add the integration in the settings menu.


## Configuration

Configuration is done when adding the integration trough the UI
You have to enter smappee api credentials :
- api key
- secret
- username (not the email adress)
- password (same a in web portal or app)

For now the integration will only give you a service call to set the charging speed. Other functionality can easily be addedd to make this as full featured as the smappee app.
Still too bad sensor values can not be read from the api in realtime (only 5 min averages).

I might add a ui element to set charging speed and select charging mode later. For now you can do that manually using a input_number helper and an automation. Something like :



```
input_number:
  smappee_charging_speed:
    name: Charging Speed
    min: 0
    max: 32
    step: 1
    unit_of_measurement: "A"
    icon: mdi:flash
```

```
automation:
  - alias: Set Charging Speed via Slider
    trigger:
      platform: state
      entity_id: input_number.smappee_charging_speed
    action:
      service: smappee_charging_profiles.set_charging_mode
      data:
        serial: "YOUR_SERIAL_NUMBER"  # Replace with your charging station serial
        mode: "NORMAL"  # You can adjust the mode based on your integration's needs
        connector: 1    # Connector number
        limit: "{{ states('input_number.smappee_charging_speed') | int }}"
```
Also, you need your serial number for the charger to make the service calls, wasn't able to find this in the api but you can find it in the Smappee app.
