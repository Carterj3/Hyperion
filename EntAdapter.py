import config
import re
import math
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
    '''
    Performs a login by posting the username, password and collecting the cookie.
    
    returns nothing
    '''
    params = urllib.parse.urlencode({
        'username' : self.username,
        'password' : self.password,
        'login' : 'Login'
      }).encode(self.encoding)
    
    response = self.opener.open(config.getKey('login_url'), params)
    return
    
  def _checkLogin(self):
    '''
    Checks if there are no cookies left in the cookie jar and then attempts to login if that is the case.
    
    returns nothing
    '''
    if len(self.cj) == 0: # allegedly the cookie jar will empty itself when cookies expire
      self._login()
    return
      
  def _postPage(self,page,params):
    '''
    Posts the given params to the url endpoint (page).
    
    returns the raw html of the page
    '''
    self._checkLogin()
    
    url_encoded = urllib.parse.urlencode(params).encode(self.encoding)
    response = self.opener.open(page, url_encoded)
    return response.read()
    

  def getGame(self,id):
    '''
    Gets the information for the given game on Ent.
    
    returns 
    {
      game_name     :       one_gom
      game_id       :       1337
      date          :       2014-12-1 18:56:00
      duration      :       13.37
      bot_id        :       7
      players       :   [
                            {
                                name        :   test
                                realm       :   west
                                ip          :   133.713.371.337
                                left        :   13
                                left_reason :   Left the game voluntarily
                            }
                        ]
    }
    '''
    page = auth._postPage(config.getUrl('games_url','id='+str(id)),{})
    soup = BeautifulSoup(page)
    index = 0
    for ele in soup.findAll('td'):
      print(index,ele)
      index = index + 1
    tds = soup.findAll('td')
    users = []
    for i in range(0,math.ceil((len(tds)-17)/5)): #players
      users.append(
      {
        'userpage' : tds[16+5*i+0], #username
        'realm' : tds[16+5*i+2],
        'ip' : tds[16+5*i+1],
        'left' : tds[16+5*i+3],
        'left_reason' : tds[16+5*i+4]
      })
    game = {
      'game_name' : tds[1],
      'game_id' : id,
      'date' : tds[3],
      'url' : tds[5], # game id? ## Remove?
      'duration' : tds[7],
      'botid' : tds[11],
      'players' : users
      
    return game
    
  def getGames(self,name,last_id):
    '''
    Gets a tuple containing the last_id (highest) and a list of game ids that meet the criteria
    
    returns
    (1337, [1121,1337,1223,1332,1321])
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

# https://entgaming.net/bans/game.php?id=4740840
# view-source:https://entgaming.net/bans/game.php?id=4740840?id=4740840

if __name__ == '__main__':
  auth = EntAdapter(config.getKey('username'),config.getKey('password'))
  print(auth._postPage('https://entgaming.net/bans/',{}))
  #print(str(auth.getGames('Island Defense','4726776')))
  temp = auth._postPage('https://entgaming.net/bans/game.php?id=4740840',{})
  soup = BeautifulSoup(temp)
  index = 0
  for ele in soup.findAll('td'):
    print(index,ele)
    index = index + 1
  tds = soup.findAll('td')
  users = []
  for i in range(0,math.ceil((len(tds)-17)/5)): #players
    users.append(
    {
      'userpage' : tds[16+5*i+0], #username
      'realm' : tds[16+5*i+2],
      'ip' : tds[16+5*i+1],
      'left' : tds[16+5*i+3],
      'left_reason' : tds[16+5*i+4]
    })
  game = {
   'gamename' : tds[1],
   'date' : tds[3],
   'url' : tds[5], # game id?
   'duration' : tds[7],
   'botid' : tds[11],
   'players' : users
  }
  print(game)