import shell
import re
import getpass
import pandas as pd
import numpy as np

data = {}
#redes_ice = ['181.193.0.0/16']
redes_ice = ['181.193.0.0/16', '181.194.0.0/15', '200.9.32.0/20', '200.9.48.0/20', '200.91.64.0/18', '200.91.128.0/18','201.191.0.0/16', '201.237.0.0/16', '201.192.0.0/12']
#redes_ice = ['201.192.0.0/12']

def is_net(field):
    pat = re.compile(".*(\d{3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{2})")
    # pat = re.compile("/30$")
    net = re.match(pat, field)
    if net:
        return net
    else:
        return False

def is_ip(field):
    pat = re.compile(".*(\d{2}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{2})")
    # pat = re.compile("/30$")
    host = re.match(pat, field)
    if host:
        return host
    else:
        return False


def get_nets(out):
    nets = []
    for i in out:
        if i.startswith('*>'):
            for n in i.strip().split():
                if is_net(n):
                    nets.append(is_net(n).group(1))
    return nets


def ssh_to_router(net):

    sh = shell.SShConnection(True)
    raw_routes = sh.output('show bgp ipv4 unicast ' + net + ' longer-prefixes')
    out = []
    out = raw_routes[1].readlines()
    subnets = get_nets(out)
    return subnets


if __name__ == '__main__':
    co = '10.178.76.1'
    username = 'cgarcia'
    password = 'celord23.'
#   username = str(input("Nombre de usuario: "))
#   password = getpass.getpass('password: ')

    for net in redes_ice:
        data[net] = ssh_to_router(net)
#    Crea el dataframe para el csv

#    print(data)
    df_rutas = pd.DataFrame()
    for  i in redes_ice:
        df_rutas[i] = pd.Series(data[i])

    df_rutas.to_csv('rutas.csv')






