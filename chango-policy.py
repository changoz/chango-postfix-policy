#!/usr/bin/python3.9

###### Postfix Active Directory user membership policy service, por Cristian Zanni ####
##
##
##
## v1.0
## cristian.zanni at gmail dot com

import sys
import subprocess

# Change variables

# Active Directory Group to check membership
adgroup = 'some_ad_group_in_your_domain'

# Main program

def dunno():
    """Answer with dunno to proceed further processing
    of restriction following the policy service
    """
    print("action=dunno\n")


def reject():
    """Answer with reject to stop restriction processing
    and reject the message
    """
    print("action=reject Rejected by python-chango-policy-service \n")


def permit():
    """Answer with permit to stop restriction processing
    and permit the message
    """
    print("action=permit\n")


def read_input():
    """Write input from stdin into buffer until we
    encounter an empty line which signals that postfix
    finished delivering the message
    """
    buff = []
    while True:
        line = sys.stdin.readline().rstrip('\n')
        if line == '':
            break
        buff.append(line)
    return buff


def main():
    """ Main function that wraps things up """
    lines = read_input()

    # x is the flag to check. For security, by default if policy can't be executed or check value against AD, it would reject email
    x = -1

    # start logic
    try:
        # convert key=value pairs into dict
        attributes = dict(line.split('=') for line in lines)

        # get authenticated user
        # pollable atributes can be found here: http://www.postfix.org/SMTPD_POLICY_README.html        
        auth_user = attributes.get('sasl_username')
        
        ## If you want to check sender user instead of authenticated user, uncomment following two lines:
        # sender = attributes.get('sender')
        # auth_user = sender.split('@')[0]

        # Command
        proc = subprocess.run(
            ['getent', 'group', adgroup], stdout=subprocess.PIPE)

        result = proc.stdout.decode('utf-8')

        if auth_user is not None:
            x = result.find(auth_user)

        # Logic
        if (x == -1):
            reject()
        else:
            dunno()

    except ValueError:
        reject()


if __name__ == '__main__':
    main()
