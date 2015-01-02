import config
from ipaddress import IPv4Address, IPv4Network
from EntAdapter import EntAdapter

class Hyperion:
  def __init__(self,username,password):
    self.ent = EntAdapter(username,password)

  def forum_rangeban(self,cdirs,reason='',botid='',unban=False):
    for cdir in cdirs:
      for ip in self.generate_cdir(cdir):
        try:
          print(str(ip))
        except:
          print('error:: '+str(ip))
  
  def whois_rangeban(self,whois_results,reason,botid='',unban=False):
    import netaddr # pip install netaddr
    import re
    for cdirs in re.findall('([\d]+\.[\d]+\.[\d]+\.[\d]+\s*-\s*[\d]+\.[\d]+\.[\d]+\.[\d]+)',whois_results):
      splits = cdirs.split('-')
      for cdir in netaddr.iprange_to_cidrs(splits[0].strip() , splits[1].strip()):
        self.mass_rangeban([str(cdir)],reason,botid,unban)
          
    
  def mass_rangeban(self,cdirs,reason,botid='',unban=False):
    for cdir in cdirs:
      for ip in self.generate_cdir(cdir):
        try:
          self.ent.rangeBan(ip,reason,botid,unban)
          print('banned:: '+str(ip))
        except:
          print('error:: '+str(ip))

  def generate_cdir(self,cdir):
    splits = cdir.split('/')
    range = int(splits[1])
    net = IPv4Network(cdir,False)
    ip = net[0]
    if range == 32:
      return [ip]
    elif range > 24:
      steps = 1 # + 1 = 256^0
      dots = 3 # xxx.xxx.xxx.xxx
    elif range > 16:
      steps = 256 # + 256 = 256^1
      dots = 2 # xxx.xxx.xxx.
    elif range > 8:
      steps = 65536 # + 65536 = 256^2
      dots = 1 # xxx.xxx.
    elif range > 0:
      steps = 16777216# + 16777216 256^3
      dots = 0 # xxx.
    else:
      return [] # never ban /0
    i = 0
    retVal = []
    while IPv4Address(ip+i*steps) in net:
      address = str(ip+i*steps)
      indexes = [j for j,x in enumerate(address) if x == '.']
      indexes.append(32) # Whole string
      endpoint = indexes[dots]
      if dots < 3: # trailing dot needs to be readded
        retVal.append(address[:endpoint]+'.')
      else:
        retVal.append(address[:endpoint])
      i =  i + 1
    return retVal

if __name__ == "__main__":
   from Hyperion import Hyperion
   hyp = Hyperion(config.getKey('ent-user'),config.getKey('ent-pass'))
   f = open('E:\\Hyperion\\tmp\\rangeban.txt', 'r')
   hyp.whois_rangeban(f.read(),'vpn tid=28764 lancom mass ban')   
   f.close()