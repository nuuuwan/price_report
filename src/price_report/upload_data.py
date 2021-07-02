"""Uploaded data to nuuuwan/price_report:data branch."""

import os


def upload_data():
    """Upload data."""
    os.system('echo "test data" > /tmp/price_report.test.txt')
    os.system('echo "# price_report" > /tmp/README.md')


if __name__ == '__main__':
    upload_data()
