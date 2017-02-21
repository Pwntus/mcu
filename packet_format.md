# Packet format

### FTTTTTTSSSSSDDDDD

### F `Packet format`
Possible values:

* 0 - all sensors included
* 1 - temperature excluded
* 2 - wind speed excluded
* 3 - wind direction excluded
* 4 - only temperature
* 5 - only wind speed
* 6 - only wind direction
	
### T `Temperature`
If included, always 6 bytes.

E.g. -10.22
	
### S `Speed`
If included, always 5 bytes.

E.g. 04.50 (m/s)
	
### D `Direction`
If included, always 5 bytes.

E.g. 45.87 (degrees)

### Max packet size: 17b
E.g. 0-01.1503.0515.00

All sensors included, -1.15°C, 3.05 m/s, 15 degrees

### Min packet size: 6b
E.g. 645.15

Only wind direction included, 45.15 degrees
