import logging
import time

from prometheus_client import start_http_server, Gauge
from cert_exp_check.checker import check_certificates


# Prometheus metric
CERT_EXPIRATION_DAYS = Gauge('certificate_expiration_days', 'Days until SSL certificate expires', ['hostname', 'port'])

logger = logging.getLogger("cert_exp_check")


def run_exporter(config):
    """
    Runs the Prometheus exporter to expose certificate expiration metrics.

    This function starts an HTTP server that Prometheus can scrape. It periodically checks the SSL
    certificates of the URLs listed in the configuration file and updates the metric
    `certificate_expiration_days` with the number of days until each certificate expires.

    :param config: Dictionary containing configuration details, including:
                   - 'exporter': Contains settings such as the port number.
                   - 'urls': List of URLs to check.

    The function runs indefinitely, updating metrics every 5 minutes.
    """
    port = config.get('exporter', {}).get('port', 8000)
    url_list = [item['url'] for item in config.get('urls', [])]
    logger.debug(f'Exporter URL list: {url_list}')

    logger.info(f'Exporter list: {url_list}')
    start_http_server(port)
    logger.info(f"Exporter running on port {port}...")

    while True:
        check_results, _ = check_certificates(url_list, 'config.yaml', 'info')
        for row in check_results._rows:
            hostname, port, _, expiration = row[1], row[2], row[3], row[4]
            if expiration != 'NA':
                expiration_days = int(expiration.split()[0])
                CERT_EXPIRATION_DAYS.labels(hostname=hostname, port=port).set(expiration_days)
        logger.debug("Metrics updated successfully.")
        time.sleep(300)  # Update every 5 minutes
