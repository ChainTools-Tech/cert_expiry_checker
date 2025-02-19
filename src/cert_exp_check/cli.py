import argparse


def process_command_line():
    """Command line processor

    :return: name of file with list of hostnames to check
    """
    cmdparser = argparse.ArgumentParser(prog='cert_check',
                                        usage='%(prog)s [options] path',
                                        description='Checks when certificate for specified hosts expires.')
    cmdparser.version = "0.2"

    cmdparser.add_argument("--mode",
                           type=str,
                           action="store",
                           dest="mode",
                           choices=['cli', 'exporter'],
                           required=True,
                           help="Mode to run the application")

    cmdparser.add_argument("--config",
                           type=str,
                           action="store",
                           dest="config",
                           required=True,
                           help="specifies file with list of URLs to check")

    cmdparser.add_argument("--log-level",
                           type=str,
                           action="store",
                           dest="log_level",
                           choices=["info", "verbose"],
                           required=True,
                           help="defines logging level")

    cmdparser.add_argument("--log-file",
                           type=str,
                           action="store",
                           dest="log_file",
                           required=False,
                           default="cert_exp_check.log",
                           help="defines logging file")

    cmdparser.add_argument("-v", "--version", action="version")
    args = cmdparser.parse_args()

    return args.mode, args.config, args.log_level, args.log_file