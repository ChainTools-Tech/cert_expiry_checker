# Certificates Expiration Checker

Certificates Expiration Checker checks number of days till certificate expires. 
It takes file with list of websites as input parameter and checks certificates assigned to those websites.
In case of any issues error is reported accordingly.

## Requirements
 - Python 3.8 or newer

## Installation

1. Clone repository and create a Python virtual environment
```bash
$ git clone https://github.com/ChainTools-Tech/cert_expiry_checker
$ cd cert_expiry_checker
$ python -m venv ./venv
$ source venv/bin/activate
(venv) $
```

2. Install the requirements
```bash
(venv) $ python -m pip install -r requirements.txt
```

3. Install script
```bash
(venv) $ pip install -e .
```

## Usage

```
(venv) $ python -m cert_exp_check --f urls.txt -l verbose
+------------------------------------------------------------------------+
|                 Cert Checker --> Source file: urls.txt                 |
+-----+-------------------+------+--------------------------+------------+
| No. |      Hostname     | Port |     Expiration date      | Expires in |
+-----+-------------------+------+--------------------------+------------+
|  1. |     github.com    | 443  | Mar 15 23:59:59 2023 GMT |  164 days  |
|  2. | nonexistingserver | 443  |    Unable to connect.    |     NA     |
|  3. |   incorrectentry  |      |    Unable to connect.    |     NA     |
|  4. |  chaintools.tech  | 443  | Dec  4 09:51:51 2022 GMT |  62 days   |
+-----+-------------------+------+--------------------------+------------+
===
Errors during check
-
nonexistingserver: Connection error [Errno 11001] getaddrinfo failed
incorrectentry: Connection error. Incorrect host entry.
(venv) $
```

### Content of urls.txt
```bash
github.com:443                                                                                                                                                                                                                                                                                                         
nonexistingserver:443
incorrectentry
chaintools.tech:443
```

## Options

RP Checker provides the following options:

- `-f` or `--file` specifies file with list of URLs.
- `-l` or `--log` defines level of error reporting.


## Uninstall
```bash
(venv) $ pip uninstall cert_exp_check
```

## About the Author

Email: support@chaintools.tech

## License

Distributed under the MIT license. See `LICENSE` in the root directory of this repo for more information.
