from cert_exp_check.checker import check_certificates
from cert_exp_check.cli import process_command_line
from cert_exp_check.config import load_config
from cert_exp_check.exporter import run_exporter
from cert_exp_check.logger import setup_logger


def cli_mode(config, log_level):
    """Runs the CLI mode"""
    url_list = [item['url'] for item in config.get('urls', [])]
    check_results, check_errors = check_certificates(url_list, 'config.yaml', log_level)
    print(check_results)
    if check_errors:
        print('===')
        print("Errors during check")
        print('-')
        print(check_errors)


def main():
    working_mode, config_path, log_level, log_file_path = process_command_line()
    print(working_mode, config_path, log_level, log_file_path)
    logger = setup_logger(log_level=log_level, log_file=log_file_path)

    logger.info(f'working_mode: {working_mode}, config_path: {config_path}, log_level: {log_level}')
    config = load_config(config_path)
    logger.debug(f'config: {config}')

    if working_mode == 'exporter':
        logger.info("Starting exporter mode...")
        run_exporter(config)
    elif working_mode == 'cli':
        logger.info("Starting CLI mode...")
        cli_mode(config, log_level)


if __name__ == '__main__':
    main()