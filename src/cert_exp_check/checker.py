import datetime
import logging
import socket
import ssl

from colorama import Fore, Style
from prettytable import PrettyTable


logger = logging.getLogger("cert_exp_check")

def get_cert_details(hostname, port=443):
    """Connects to host and pulls certificate details, if available.

    :param hostname: IP address or hostname of target system
    :param port: indicates on which port host should respond

    :return: certificate details for specific hostname
    """
    context = ssl.create_default_context()

    try:
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                return ssock.getpeercert()
    except Exception as e:
        return f"Connection error {e}"


def calculate_cert_expiration_days(cert_info):
    """Calculate number of days till certificate expiration
    Time is calculated using UTC timezone.

    :param cert_info: certificate details provided by get_cert_details function

    :return: number od days to certificate expiration
    """
    expiry_date = datetime.datetime.strptime(cert_info['notAfter'], '%b %d %H:%M:%S %Y %Z')
    return expiry_date - datetime.datetime.utcnow()


def check_certificates(urls, source_file, log_level):
    """Checks SSL certificate expiration dates for a list of URLs.

    For each URL in the provided list, the function attempts to connect and retrieve the SSL certificate details.
    If successful, it calculates the number of days until expiration. If not, it logs an error and notes the issue.
    Results are returned as a PrettyTable with certificate details and a string of errors if any occurred.

    :param urls: List of URLs (with optional ports) to check, e.g., 'example.com:443' or 'example.com'
    :param source_file: Name of the file from which the URLs were sourced (used in the table title)
    :param log_level: Logging level, either 'info' or 'verbose' (verbose includes detailed error messages)

    :return: Tuple containing:
             - cert_table (PrettyTable): Table with certificate information (No., Hostname, Port, Expiration date, Expires in)
             - cert_errors (str): Concatenated error messages if any occurred, empty if none
    """
    logger.info(f"Checking certificates for URLs from {source_file}...")
    cert_table = PrettyTable()
    cert_table.title = f'Cert Checker --> Source file: {source_file}'
    cert_table.field_names = ['No.', 'Hostname', 'Port', 'Expiration date', 'Expires in']
    cert_no = 1
    cert_errors = ''
    for host_url in urls:
        try:
            check_hostname, check_port = host_url.split(':')
            cert_details = get_cert_details(check_hostname, check_port)
        except ValueError:
            check_hostname = host_url
            check_port = ''
            cert_details = f"Connection error. Incorrect host entry."

        if str(cert_details).startswith('Connection error') == True:
            logger.error(f"Connection error for {check_hostname}")
            cert_table.add_row([str(cert_no) + '.',
                                check_hostname,
                                check_port,
                                Fore.RED + 'Unable to connect.' + Style.RESET_ALL,
                                'NA'])
            cert_errors += f'{check_hostname}: {cert_details}\n' if log_level == 'verbose' else ''
        else:
            expiry_delta = calculate_cert_expiration_days(cert_details)

            cert_table.add_row([str(cert_no) + '.',
                                check_hostname,
                                check_port,
                                cert_details['notAfter'],
                                str(expiry_delta.days) + ' days'])
        cert_no += 1
    return cert_table, cert_errors