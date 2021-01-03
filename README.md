# Home Assistant My Gas Chevrolet
This is a modification of the My Chevrolet Integration from Home Assistant.  While I do not has an electric vehicle (EV), I do have a gas Chrevolet that uses the My Chevrolet app.  With a little bit of fiddling, it is possible to retrieve the gas-related inforation, so I can track my fuel economy, and how much gass I have left.

## Installation
1. Copy the `mygaschevy` folder to the `custom_components` folder in your Home Assistant configuration directory:
```
/home/homeassistant/
├── .homeassistant
│   ├── custom_components
│   │   └── mygaschevy

```
2. Add the following code in your `configuration.yaml` file, or modify your google_maps configuration:
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
