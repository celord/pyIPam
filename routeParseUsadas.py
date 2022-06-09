import shell
import re
import pandas as pd
import numpy as np

data = []

redes_ice = ['181.193.0.0/16']

#redes_ice = ['181.193.0.0/16', '181.194.0.0/15', '200.9.32.0/20', 
#              '200.9.48.0/20', '200.91.64.0/18', '200.91.128.0/18',
#              '201.191.0.0/16', '201.237.0.0/16', '201.192.0.0/12']

#redes_ice = ['201.192.0.0/12']

class GetBGPRoutes:
    
    """"Class to extract BGP route information from the network"""
    

        
    def getUsedNets(self,red,verbose):
        c = shell.SShConnection(verbose)
        out = c.output('show bgp ipv4 unicast ' + red + ' longer-prefixes')
        return out[1].readlines()
    
    def getNexHop(self,lst):
        rutas = {}
        for line in lst:
            if len(line.strip().split()) == 7:
                rutaBgp = line.strip().split()
                for i in rutaBgp:
                    if self.is_net(i):
                        k = self.is_net(i).group(1)
                    if self.is_ip(i):
                        v = self.is_ip(i).group(1)
                    try:
                        rutas[k] = v
                    except :
                        pass
        return rutas

        
    def is_net(self,field):
        pat = re.compile(".*(\d{3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{2})")
        # pat = re.compile("/30$")
        net = re.match(pat, field)
        if net:
           return net
        else:
           return False

    def is_ip(self,field):
        pat = re.compile("(\d{2}\.\d{1,3}\.\d{1,3}\.\d{1,3})")
        # pat = re.compile("/30$")
        host = re.match(pat, field)
        if host:
            return host
        else:
            return False

    def string_finder(self,string,field):
        pat = re.compile(string)
        pat = re.match(pat,field)
        if pat:
            return pat
        else:
            return False


    def get_info(self,nexthop):
        
        verbose = False
        c = shell.SShConnection(verbose)
        out = c.output('show ip route ' + nexthop)
        return out[1].readlines()




if __name__ == "__main__":
    b = GetBGPRoutes()
    kp = b.getNexHop(b.getUsedNets('181.193.0.0/16',True))
    for k,v in kp.items():
        print(k,v)
    #rinfo = b.get_info('10.178.72.23')










