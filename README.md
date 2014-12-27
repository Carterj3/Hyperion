Hyperion
========
Set-up

Rename config.py.sample to config.py
Now modify the values to be correct, ex : 'ent-user' would be changed to be 'cambrioleuse' and 'ent-pass' would be be changed to 'ChangeMe'

You can ignore the values related to mongo.

You need to install python3.

Afterwards you need to add the following modules
beautifulsoup4, which can be installed via "pip install beautifulsoup4"

========
Mass-Range bans

They can be preformed by going to the console and typing

from Hyperion import Hyperion
hyp = Hyperion(config.getKey('ent-user'),config.getKey('ent-pass'))
hyp.mass_rangeban(['ip1/mask1','ip2/mask2'],'reason')

where ip1/mask1 would look like 123.123.123.123/16 and would ban 123.123.
if ip1/mask1 was like 123.123.123.123/25 it would actually ban all the ips from 123.123.123.0 to .127

If you need to undo a rangeban you can easily do it by supplying the additonal parameters for mass_rangeban
ex. hyp.mass_rangeban(['ip1/mask1','ip2/mask2'],'reason',unban=True)

Or if you want to single out a bot
hyp.mass_rangeban(['ip1/mask1','ip2/mask2'],'reason',botid='60')
