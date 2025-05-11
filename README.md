# Certificates Expiration Checker

Certificates Expiration Checker is a tool designed to check the number of days until SSL certificates expire for a list of websites. The app supports both CLI mode and Prometheus exporter mode.

## Requirements
- Python 3.8 or newer

## Installation

1. Clone the repository and create a Python virtual environment:

```bash
$ git clone https://github.com/qf3l3k/cert_expiry_checker
$ cd cert_expiry_checker
$ python -m venv ./venv
$ source venv/bin/activate
(venv) $
```

2. Install the requirements:

```bash
(venv) $ python -m pip install -r requirements.txt
```

3. Install the script:

```bash
(venv) $ pip install -e .
```

## Configuration

The configuration file is written in YAML format. Example:

```yaml
exporter:
  port: 8000
urls:
  - url: github.com:443
  - url: nonexistingserver:443
  - url: chaintools.tech:443
  - url: explorer.chaintools.tech:443
  - url: testnet.explorer.chaintools.tech:443
```

## Usage

### CLI Mode

```bash
(venv) $ python -m cert_exp_check --mode cli --config config.yaml --log-level verbose
```

Example Output:

```
+------------------------------------------------------------------------------------+
|                 Cert Checker --> Source file: config.yaml                          |
+-----+-------------------------------+------+--------------------------+------------+
| No. |           Hostname            | Port |     Expiration date      | Expires in |
+-----+-------------------------------+------+--------------------------+------------+
|  1. | github.com                    | 443  | Mar 15 23:59:59 2023 GMT |   164 days |
|  2. | nonexistingserver             | 443  |    Unable to connect.    |      NA    |
|  3. | chaintools.tech               | 443  | Dec 4 09:51:51 2022 GMT  |   62 days  |
|  4. | explorer.chaintools.tech      | 443  | Jan 10 12:00:00 2023 GMT |   99 days  |
|  5. | testnet.explorer.chaintools   | 443  | Feb 20 18:30:00 2023 GMT |   140 days |
+-----+-------------------------------+------+--------------------------+------------+
===
Errors during check
-
nonexistingserver: Connection error [Errno 11001] getaddrinfo failed
```

### Exporter Mode

```bash
(venv) $ python -m cert_exp_check --mode exporter --config config.yaml --log-level info
```

This mode runs a Prometheus exporter that exposes the number of days until SSL certificates expire. The exporter listens on the port defined in the `config.yaml` file.

Metrics are available at:

```
http://localhost:8000
```

Example Metric:

```
# HELP certificate_expiration_days Days until SSL certificate expires
# TYPE certificate_expiration_days gauge
certificate_expiration_days{hostname="github.com",port="443"} 164
certificate_expiration_days{hostname="chaintools.tech",port="443"} 62
certificate_expiration_days{hostname="explorer.chaintools.tech",port="443"} 99
certificate_expiration_days{hostname="testnet.explorer.chaintools.tech",port="443"} 140
```

## Options

- `--mode` (required): Defines the mode to run the app. Options: `cli`, `exporter`.
- `--config` (required): Specifies the YAML configuration file.
- `--log-level` (required): Defines the logging level. Options: `info`, `verbose`.
- `--log-file` (optional): Specifies the log file path. Default: `cert_exp_check.log`.

## Logging

- Console logs are colored and simplified.
- File logs are detailed, with timestamps, module names, and log levels.

## Uninstall

```bash
(venv) $ pip uninstall cert_exp_check
```

## About the Author

Email: contact@chaintools.tech

## License

Distributed under the MIT license. See `LICENSE` in the root directory of this repository for more information.

---
Internal tag: 004