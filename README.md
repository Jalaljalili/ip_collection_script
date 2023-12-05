# IP Collection Script

This script is designed to collect public IP addresses for multiple local IP addresses on a machine. It uses the `pycurl` library to make HTTP requests and the `netifaces` and `ipaddress` libraries to handle network interfaces and IP addresses.



## Requirements

- Python 3.x
- `ipaddress` library (`pip install ipaddress`)
- `netifaces` library (`pip install netifaces`)
- `pycurl` library (`pip install pycurl`)

## Usage

1. Ensure you have the required libraries installed. You can install them using
```bash
pip install pycurl netifaces ipaddress
```
2. Run the script:
```bash
python ip_collection_script.py [-t|--time] [interval1] [interval2] ...
```
The `-t` or `--time` option is used to specify the time intervals for IP collection in hours. If not provided, the script will use the default intervals of 1, 3, 12, and 24 hours.

The script will find the local interface with multiple IP addresses, collect the public IP addresses for each IP, and write the results to a CSV file named `ip_collection.csv`.


## Configuration

The script uses the DISALLOWED_NETWORKS environment variable to specify a list of disallowed IP networks. If this variable is not set, the script will use the default networks `192.168.0.0/16,172.17.0.0/16`.


## Output

The script writes the results to a CSV file named `ip_collection.csv`. The file contains the following columns:

- `Local IP`: The local IP address.

- `Public IP`: The public IP address at the start of the collection.

- `Public IP (after 1 hour)`: The public IP address after 1 hour.

- `Public IP (after 3 hour)`: The public IP address after 3 hours.

- `Public IP (after 12 hour)`: The public IP address after 12 hours.

- `Public IP (after 24 hour)`: The public IP address after 24 hours.

- `IP Changed`: A boolean value indicating whether the public IP address has changed during the collection period.

## Note

The script uses the `pycurl` library to perform HTTP requests. The `CONNECTTIMEOUT` and `TIMEOUT` options are set to 5 and 10 seconds respectively. If the HTTP request takes longer than these times, the script will raise a `pycurl.error`.

