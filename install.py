#!/usr/bin/env python

import sys
import yaml
import argparse
import random
import string

try:
    from ansible.cli.playbook import PlaybookCLI  as mycli
except Exception:
    print "Please install ansible , 'dpkg -i ./ansible/*.deb' "
    sys.exit(1)

def read_vars(vars_file):
    f = open(vars_file)
    s = yaml.load(f)
    f.close()
    return s

def parse_args():
    parser = argparse.ArgumentParser(description="kylincloud2 install tools")
    parser.add_argument('-f','--vars_file',default='./default.yml',help = "configuration file,default: ./default.yml")
    parser.add_argument('--master', action='store_true', help = "execute  master node install only")
    parser.add_argument('--nodes', action='store_true', help = "execute nodes node install  only")
    parser.add_argument('--uninstall', action='store_true', help = "uninstall kylincloud2")
    args = parser.parse_args();
    return args

if __name__ == "__main__":
    args = parse_args()
    var = read_vars(args.vars_file)
    try:
        salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        host_tmp = "/tmp/" + salt + ".host"
        hfile = open(host_tmp,'w+')
        print host_tmp
    except Exception:
        print "Cannot create host file : " + host_tmp 
    hfile.write("[master]\n")
    try:
        for i in var['master']:
            hfile.write(i['ip'] + "\n")
    except Exception :
        pass
    hfile.write("[nodes]\n")
    try:
        for i in var['nodes']:
            hfile.write(i['ip'] + "\n")
    except Exception :
        pass
    hfile.write("[local]\n")
    hfile.write(var['master'][0]['ip'] + "\n")
    hfile.write("[kube-cluster:children]\n")
    hfile.write("master\n")
    hfile.write("nodes\n")
    hfile.close()
    
    tags='all'
    if args.master == True :
        tags = 'master'
    elif args.nodes == True :
        tags = 'nodes'
    if args.uninstall == True :
       cmd = ['ansible-playbook','uninstall.yml','-i',host_tmp]
    else:      
       cmd = ['ansible-playbook','main.yml','-i',host_tmp,'--tags',tags]
    print cmd
    cli = mycli(cmd)
    cli.parse()
    #sys.exit(cli.run())

