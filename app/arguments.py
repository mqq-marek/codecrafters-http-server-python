import argparse


def args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--port", type=int, required=False, help="port")
    ap.add_argument("--host", type=str, required=False, help="host")
    ap.add_argument(
        "-d", "--directory", type=str, required=False, help="web server home directory"
    )

    return vars(ap.parse_args())


values = args()
