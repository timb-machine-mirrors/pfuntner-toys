# `units`

## Purpose
Convert from imperial units (pounds, feet, Farenheit, et al) to metric (kilograms, meters, Celcius, et al).

## Syntax
```
usage: units [-h] [-m {length,volume,mass,temperature}] [-a] [-f] [-v]
             arg [arg ...]

Perform unit conversions

positional arguments:
  arg                   Measurement to convert

optional arguments:
  -h, --help            show this help message and exit
  -m {length,volume,mass,temperature}, --measurement {length,volume,mass,temperature}
                        Measurement system
  -a, --all             Show all equivalent values
  -f, --fractional      Break imperial fractions down to additional units
  -v, --verbose         Enable more debugging
```

### Options and arguments
| Option | Description | Default |
| ------ | ----------- | ------- |
| `-m MEASUREMENT` or `--measurement MEASUREMENT` | Indicates the type of measurement in case it cannot be determined implicitly.  The valid measurements are `length`, `volume`, `mass`, and `temperature`.<br><br>This is useful to express ounces since it could be volume or mass. | By default, the script tries to determine the type of measurement implicitly.  Usually this is sufficient.  The only time it's not sufficient is for ounces. |
| `-a` or --all` | Displays all equivalencies for the measurement.  For instance, if you provide pounds, ounces, tons, milligrams, grams, and kilgrams are displayed. | Only the most applicable equivalent measurement is displayed.  For example, pounds to kilograms. |
| `--f` or `--fractional` | Breaks fractions down to components.  For instance, instead display `5.5 feet`, it would display `5 feet, 6 inches`.  The option is only avaiable when supplying imperial measurements. | By default a single unit is used with fractions such as `5.5 feet` |
|  `-v`  | Enable verbose debugging | Debugging is not enabled |

The starting measurement can be expressed in a single string such as `5ft` or two words such as `5 ft`.

## Examples

```
$ units 100 lb
100.0 lb = 45.3592 kg
$ units -a 100 lb
100.0 lb = 45.3592 kg
0.05 ton
1600.0 oz
45359200.0 mg
45359.2 g
$ units -f 3.14 ton
3ton, 280lb
$ units 98.6F
98.6 F = 37.0 C
$
```

## Notes

- The conversions are driven by the relationships defined in`units.json`.  Currently only a strict set of units are accepted.  Maybe I'll extend that some day but we'll see.   The allowable units are:
  - Weight: `oz`, `lb`, `ton`, `mg`, `g`, `kg`
  - Length: `ft`, `in`, `mi`, `mm`, `m`, `km`
  - Volume: `tsp`, `tbsp`, `oz`, `cup`, `pint`, `gal`, `ml`, `l`, `kl`
  - Temperature: `C` or `F`

  This means that `ounces` and `ounce` are **not** acceptable.  Only `oz` is allowed.  You get the idea.

- While doing conversions, the script will try to find the nearest equivalent measurement in the other system.  For instance, if you provide feet, it will convert to meters (even if another unit might make more sense with respect to the scale) unless you tell it to show all the equivalent measurements.
