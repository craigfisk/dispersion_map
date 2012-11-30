from myfruitcake.models import *
from myfruitcake.views import *
from datetime import datetime

testlist
#f = Fruitcake()
#f.id = 10
#u = User()
#u.id = 30
#shipment = Shipment(dt=datetime.now(),fruitcake=f,sender=u,message='Hi!') 

fauxshipment = FauxShipment(dt=datetime.now(),message='Hi!')
fauxshipment.save()
e = fauxshipment.emailcontacts.create(email=testlist[0])
e = fauxshipment.emailcontacts.create(email=testlist[1])
etc.
--> turn the above into a for loop on testlist list of email addresses, given the shipment info.

now:
f = FauxShipment.objects.filter(emailcontacts__email='shoujigui@gmail.com')
f.values()
--> 
[{'dt': datetime.datetime(2012, 11, 29, 21, 40, 54, 23406, tzinfo=<UTC>), 'message': u'Hi!', 'id': 1}]

--> trying to cover the Yuji Tomita explanation:
d = datetime.now()
flist = FauxShipment.objects.create(dt=d, message='Hi!')
flist.emailcontacts.add(testlist)
--> can't get that to work with a list, of course, so I'm back to a for loop.

How to get a list of addressees for a shipment?

