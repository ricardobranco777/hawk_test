#!/usr/bin/python3
"""HAWK GUI interface Selenium test: tests hawk GUI with Selenium using firefox or chrome"""

import argparse
import ipaddress
import re
import socket
import sys

import hawk_test_driver
import hawk_test_ssh
import hawk_test_results


def hostname(string):
    try:
        socket.getaddrinfo(string, 1)
        return string
    except socket.gaierror:
        raise argparse.ArgumentTypeError("unknown host: %s" % string)


def cidr_address(string):
    try:
        ipaddress.ip_network(string, False)
        return string
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid CIDR address: %s" % string)


def check_port(port):
    if port.isdigit() and 1 <= int(port) <= 65535:
        return port
    raise argparse.ArgumentTypeError("%s is an invalid port number" % port)


def parse_args():
    parser = argparse.ArgumentParser(description='HAWK GUI interface Selenium test')
    parser.add_argument('-b', '--browser', required=True, choices=['firefox', 'chrome', 'chromium'],
                        help='Browser to use in the test')
    parser.add_argument('--headless', action='store_true',
                        help="Use headless mode")
    parser.add_argument('-H', '--host', default='localhost', type=hostname,
                        help='Host or IP address where HAWK is running')
    parser.add_argument('-I', '--virtual-ip', type=cidr_address,
                        help='Virtual IP address in CIDR notation')
    parser.add_argument('-P', '--port', default='7630', type=check_port,
                        help='TCP port where HAWK is running')
    parser.add_argument('-p', '--prefix',
                        help='Prefix to add to Resources created during the test')
    parser.add_argument('-t', '--test-version', required=True,
                        help='Test version. Ex: 12-SP3, 12-SP4, 15, 15-SP1')
    parser.add_argument('-s', '--secret',
                        help='root SSH Password of the HAWK node')
    parser.add_argument('-r', '--results',
                        help='Generate hawk_test.results file')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    # Create driver instance
    browser = hawk_test_driver.HawkTestDriver(addr=args.host.lower(), port=args.port,
                                              browser=args.browser.lower(),
                                              version=args.test_version.lower())

    # Initialize results set
    results = hawk_test_results.ResultSet()

    # Establish SSH connection to verify status only if SSH password was supplied
    if args.secret:
        ssh = hawk_test_ssh.HawkTestSSH(args.host.lower(), args.secret)
        results.add_ssh_tests()

    # Resources to create
    if args.prefix and not re.match(r"^\w+$", args.prefix.lower()):
        print("ERROR: Prefix must contain only numbers and letters. Ignoring")
        args.prefix = ''
    mycluster = args.prefix.lower() + 'Anderes'
    myprimitive = args.prefix.lower() + 'cool_primitive'
    myclone = args.prefix.lower() + 'cool_clone'
    mygroup = args.prefix.lower() + 'cool_group'

    # Tests to perform
    browser.test('test_set_stonith_maintenance', results)
    if args.secret:
        ssh.verify_stonith_in_maintenance(results)
    browser.test('test_disable_stonith_maintenance', results)
    browser.test('test_view_details_first_node', results)
    browser.test('test_clear_state_first_node', results)
    browser.test('test_set_first_node_maintenance', results)
    if args.secret:
        ssh.verify_node_maintenance(results)
    browser.test('test_disable_maintenance_first_node', results)
    browser.test('test_add_new_cluster', results, mycluster)
    browser.test('test_remove_cluster', results, mycluster)
    browser.test('test_click_on_history', results)
    browser.test('test_generate_report', results)
    browser.test('test_click_on_command_log', results)
    browser.test('test_click_on_status', results)
    browser.test('test_add_primitive', results, myprimitive)
    if args.secret:
        ssh.verify_primitive(myprimitive, args.test_version.lower(), results)
    browser.test('test_remove_primitive', results, myprimitive)
    if args.secret:
        ssh.verify_primitive_removed(myprimitive, results)
    browser.test('test_add_clone', results, myclone)
    browser.test('test_remove_clone', results, myclone)
    browser.test('test_add_group', results, mygroup)
    browser.test('test_remove_group', results, mygroup)
    browser.test('test_click_around_edit_conf', results)
    if args.virtual_ip:
        browser.test('test_add_virtual_ip', results, args.virtual_ip)
        browser.test('test_remove_virtual_ip', results)

    # Save results if run with -r or --results
    if args.results:
        results.logresults(args.results)

    return results.get_failed_tests_total()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(1)
