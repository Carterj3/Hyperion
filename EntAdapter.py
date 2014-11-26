import config
import re
import urllib.request as urllib2
import urllib
from http.cookiejar import CookieJar
from bs4 import BeautifulSoup

def debug(message,level):
  if config.getKey('verbose') <= level:
    print(message)

class EntAdapter:
  '''
    An Adapter to the Ent Gaming Login system to obtain the correct cookie for usage with the bans manager
  '''
  
  def __init__(self,username,password):
    self.cj = CookieJar()
    self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
    self.encoding = 'utf-8'
    self.username = username
    self.password = password
    
  def _login(self):
    params = urllib.parse.urlencode({
        'username' : self.username,
        'password' : self.password,
        'login' : 'Login'
      }).encode(self.encoding)
    
    response = self.opener.open(config.getKey('login_url'), params)
    return
    
  def _checkLogin(self):
    if len(self.cj) == 0: # allegedly the cookie jar will empty itself when cookies expire
      self._login()
    return
      
  def _postPage(self,page,params):
    self._checkLogin()
    
    url_encoded = urllib.parse.urlencode(params).encode(self.encoding)
    response = self.opener.open(page, url_encoded)
    return response.read()
    

  def getGame(self,id):
    page = auth._postPage(config.getUrl('games_url','id='+str(id)),{})
    soup = BeautifulSoup(page)
    
  def getGames(self,name,last_id):
    '''
    returns a tuple containing the last_id and a list of game ids that meet the criteria
    '''
    index=0
    games = []
    first_id = False
    while(True):
      page = auth._postPage(config.getUrl('games_url','start='+str(index)),{})
      soup = BeautifulSoup(page)
      for hyperlink in soup.findAll('a'):
        link = str(hyperlink['href'])
        text = str(hyperlink.contents)
        if not 'game.php?id=' in link: # is the url for games
          debug('Game Guard :: '+link,1)
          continue
        if not name in text: # Criteria meeting
          debug('Criteria Guard :: '+text,1)
          continue
        id = re.findall('\d+',link)[0]
        if not first_id:
          first_id = id
        if last_id >= id:
          return (first_id,set(games))
        games.append(id)
        debug('Added id :: '+str(id),1)
      debug('Index is:: '+str(index) + ' | '+str(id)+' : '+str(last_id),2)
      index = index + 100

# Start at https://entgaming.net/bans/games.php?start=0

# Mark last game id
# Check if last game id is after last known id
# If it is, keep incrememting url by 100 until it is not.
    
if __name__ == '__main__':
  auth = EntAdapter(config.getKey('username'),config.getKey('password'))
  print(auth._postPage('https://entgaming.net/bans/',{}))
  print(str(auth.getGames('Island Defense','4726776')))