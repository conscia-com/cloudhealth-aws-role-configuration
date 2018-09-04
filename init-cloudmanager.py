#!/usr/bin/python

account_list = "accounts-with-cloudmanager.txt"
template=open("init.cloudmanager-role.template").read()

with open(account_list) as f:
    accounts = [x.strip().split() for x in f.readlines() if not x.startswith('#') and x.strip()]

for account in accounts:
    print("creating cloudmanager-role-on-%s.tf" % (account[1]))
    with open("cloudmanager-role-on-%s.tf"%account[1], "w") as tf_config:
        tf_config.write(template.replace('ACCESS-ROLE', account[2]).replace('ACCOUNT-NAME', account[1]).replace('ACCOUNT-ID', account[0]))

