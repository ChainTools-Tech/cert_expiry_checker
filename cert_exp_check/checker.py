import datetime
import socket
import ssl

from prettytable import PrettyTable


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

    :param cert_info: certificate details provided by get_cert_details function

    :return: number od days to certificate expiration
    """
    expiry_date = datetime.datetime.strptime(cert_info['notAfter'], '%b %d %H:%M:%S %Y %Z')
    return expiry_date - datetime.datetime.utcnow()


def check_certificates(urls, source_file, log_level):
    cert_table = PrettyTable()
    cert_table.title = f'Cert Checker --> Source file: {source_file}'
    cert_table.field_names = ['No.', 'Hostname', 'Port', 'Expiration date', 'Expires in']
    cert_no = 1
    cert_errors = ''
    for host_url in urls:
        check_hostname, check_port = host_url.split(':')
        cert_details = get_cert_details(check_hostname, check_port)

        if str(cert_details).startswith('Connection error') == True:
            cert_table.add_row([str(cert_no) + '.',
                                check_hostname,
                                check_port,
                                'Unable to connect.',
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