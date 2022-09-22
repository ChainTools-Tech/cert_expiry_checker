import sys

from cert_exp_check.checker import check_certificates
from cert_exp_check.cli import process_command_line


def main():
    input_file, logging = process_command_line()
    url_list = []
    try:
        with open(input_file) as file:
            for line in file:
                url_list.append(line.rstrip())
    except IOError:
        sys.exit("Incorrect file name with list of URLs.")
    check_results, check_errors = check_certificates(url_list, input_file, logging)
    print(check_results)
    if logging == 'verbose':
        print('===')
        print("Errors during check")
        print('-')
        print(check_errors)


if __name__ == '__main__':
    main()