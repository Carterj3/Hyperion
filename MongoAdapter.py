from pymongo import MongoClient #pip install pymongo
import config

class MongoAdapter:
  def __init__(self,server,port,username,password):
    self.client = MongoClient(server, port)
    self.client.admin.authenticate(username,password, mechanism='MONGODB-CR')
    self.db = client['hyperion']
    
  def addFound(self,name,watch_id,game_id):
    '''
    Unique :: name@realm, watch_id, game_id
    {
        name        :   test@west
        watch_id    :   547cfd3e6c3d571b1035314c
        game_id     :   1337
    }
    '''
    found_db = self.db['found']
    found = {
        "name"       :   name,
        "watch_id"   :   watch_id,
        "game_id"    :   game_id
    }
    found_db.insert(found)

  def addWatch(self,submitter,ip,region,realm,start_date,duration):
    '''
    Unique :: submitter, ip, start date
    {
        submitter       :   test
        ip              :   1.2.3.4
        region          :   china
        realm           :   *
        start date      :   2014-12-1 18:56:00
        duration        :   234445
    }
    '''
    watch_db = self.db['watch']
    watch = {
      "submitter"       :   submitter,
        "ip"          :   ip,
        "region"      :   region,
        "realm"       :   realm,
        "start_date"  :   start_date,
        "duration"    :   duration
    }
    watch_db.insert(watch)

  def addUser(self,username,last_ip,last_region,first_played):
    '''
    Unique :: name@realm
    {
        name            :   test@west
        last_ip         :   { ip:1.2.3.4 , date:2014-12-1 18:56:00}
        last_region     :   {region:china , date2014-12-1 18:56:00}
        first_played    :   2014-12-1 18:56:00
    }
    '''
    ## May need to update user for the lastip/lastregion
    user_db = self.db['users']

    key = { "name":username }
    data = {
    "last_ip":last_ip,
    "last_region":last_region,
    "first_played":first_played
    }

    user_db.update(key,data,upsert=True)

  def addPlayer(self,player,game_id):
    '''
    Unique :: name@realm, game_id
    {
        name        :   test@west
        game_id     :   1337
        slot        :   2
        ip          :   1.2.3.4
        hostname    :   dhcp-1.2.3.4.test@example.com
        duration    :   13.4
        left        :   Left the Game Voluntarily
    }
    '''
    player_db = self.db['players']
    player['game_id'] = game_id
    player_db.insert(player)


  def addGame(self,game_id,game_name,date,duration,map,players):
    '''
    Unique :: game_id
    {
        game_id     :   1337
        game_name   :   Pro Game
        date        :   2014-12-1 18:56:00
        duration    :   13.4
        map         :   pro.w3x
    }
    For every game there will be corresponding player entries who were in the game
    '''
    game_db = self.db['games']
    game = {
      "game_id":game_id,
      "game name":game_name,
      "date":date,
      "duration":duration,
      "map":map
    }
    game_db.insert(game)
    for player in players:
      addPlayer(player,game_id)

if __name__ == "__main__":
  mongo = MongoAdapter(config.getKey('mongo-host'),config.getKey('mongo-port'),config.getKey('mongo-user'),config.getKey('mongo-pass'))