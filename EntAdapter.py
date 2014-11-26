import config
import urllib.request as urllib2
import urllib
from http.cookiejar import CookieJar


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
    _checkLogin()
    
    url_encoded = urllib.parse.urlencode(params).encode(self.encoding)
    response = self.opener.open(page, url_encoded)
    return response.read()

if __name__ == '__main__':
  auth = AuthAdapter(config.getKey('username'),config.getKey('password'))
  print(auth.getPage('https://entgaming.net/bans/',{}))