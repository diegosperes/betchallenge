from datetime import datetime

event = {
   "id": 994839351740,
   "name": "Real Madrid vs Barcelona",
   "startTime": "2018-06-20 10:30:00",
   "sport": {
      "id": 221,
      "name": "Football"
   },
   "markets": [
      {
         "id": 385086549360973392,
         "name": "Winner",
         "selections": [
            {
               "id": 8243901714083343527,
               "name": "Real Madrid",
               "odds": 1.01
            },
            {
               "id": 5737666888266680774,
               "name": "Barcelona",
               "odds": 1.01
            }
         ]
      }
   ]
}

sent_message = {
   "@uri": None,
   "event": event['id'],
   "status": "sent",
   "send_at": datetime.now(),
   "scheduled_at": None,
   "processed_at": None,
}

scheduled_message = sent_message.copy()
scheduled_message['status'] = 'scheduled'
scheduled_message['scheduled_at'] = datetime.now()

processed_message = scheduled_message.copy()
processed_message['status'] = 'processed'
processed_message['processed_at'] = datetime.now()
processed_message['@uri'] = '/api/match/{0}'.format(event['id'])
