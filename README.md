[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

[![hacs][hacsbadge]](hacs)
![Project Maintenance][maintenance-shield]
# Home Assistant My Gas Chevrolet
This is a modification of the My Chevrolet Integration from Home Assistant.  While I do not has an electric vehicle (EV), I do have a gas Chrevolet that uses the My Chevrolet app.  With a little bit of fiddling, it is possible to retrieve the gas-related inforation, so I can track my fuel economy, and how much gas I have left. Eventually I would like to figure out how to retrieve other information such as oil life and tire pressures.

## Installation
### Manual
Copy the `mygaschevy` folder to the `custom_components` folder in your Home Assistant configuration directory:
```
/home/homeassistant/
├── .homeassistant
│   ├── custom_components
│   │   └── mygaschevy

```
### HACS
Under Custom Repositories, add https://github.com/dennyreiter/hass-mygaschevy as an integration. Then install.

## Configuration
Add the following code in your `configuration.yaml` file, or modify your google_maps configuration:
```
mygaschevy:
    username: YOUR_USERNAME
    password: YOUR_PASSWORD
```


## Configuration
| key              | required | type    | usage
|------------------|----------|---------|-----------------------------------------------|
| username         | true     | string  | The email address for the MyChevrolet account |
| password         | true     | string  | The password for the MyChevrolet account      |

Just like the My Chevrolet integration, it can take two to three minutes for the results to be returned.

The created sensors will be in the form of `sensor.mygaschevy_VEHICLE_NAME.*`

| sensor                                          | description                             |
|-------------------------------------------------|-----------------------------------------|
| sensor.mygaschevy_VEHICLE_NAME_fuel_economy     | miles per gallon per vehicle            |
| sensor.mygaschevy_VEHICLE_NAME_fuel_percentage  | percentage of fuel left in the tank     |
| sensor.mygaschevy_VEHICLE_NAME_gas_range        | approximate range in miles per vehicle  |
| sensor.mygaschevy_VEHICLE_NAME_mileage          | the vehicle mileage                     |

## Example Binary Sensor
```
binary_sensor:

  - platform: template
    sensors:
      truck_gas_low:
        friendly_name: "Truck Gas Level Low"
        device_class: gas
        value_template: >-
          {{ states('sensor.mygaschevy_2011_chevrolet_silverado_1500_fuel_percentage') | int < 18 }}
  ```
## Resources
Built upon the package and Home Assistant integration by @sdague
https://github.com/sdague/mychevy

  [hacs]: https://github.com/custom-components/hacs
  [hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
  [maintenance-shield]: https://img.shields.io/badge/maintainer-dennyreiter-blue.svg?style=for-the-badge
