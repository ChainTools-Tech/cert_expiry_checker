import argparse


def process_command_line():
    """Command line processor

    :return: name of file with list of hostnames to check
    """
    cmdparser = argparse.ArgumentParser(prog='cert_check',
                                        usage='%(prog)s [options] path',
                                        description='Checks status of certificates on specified hosts.')
    cmdparser.version = "0.1"

    cmdparser.add_argument("-f", "--file",
                           type=str,
                           nargs=1,
                           action="store",
                           dest="file",
                           required=True,
                           help="specifies file with list of URLs to check")

    cmdparser.add_argument("-l", "--log",
                           type=str,
                           nargs=1,
                           action="store",
                           dest="log",
                           choices=["info", "verbose"],
                           required=True,
                           help="defines error logging level")

    cmdparser.add_argument("-v", "--version", action="version")
    args = cmdparser.parse_args()

    return args.file[0], args.log[0]