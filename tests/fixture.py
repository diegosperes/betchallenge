from datetime import datetime

from betbright.models.message import (
   SENT_STATUS_MESSAGE, SCHEDULED_STATUS_MESSAGE, PROCESSED_STATUS_MESSAGE
)


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

message = {
   "id": 8661032861909884224,
   "message_type": "NewEvent",
   "event": event
}

sent_message = {
   "@uri": None,
   "event": event['id'],
   "status": SENT_STATUS_MESSAGE,
   "send_at": datetime.now(),
   "scheduled_at": None,
   "processed_at": None,
}

scheduled_message = sent_message.copy()
scheduled_message['status'] = SCHEDULED_STATUS_MESSAGE
scheduled_message['scheduled_at'] = datetime.now()

processed_message = scheduled_message.copy()
processed_message['status'] = PROCESSED_STATUS_MESSAGE
processed_message['processed_at'] = datetime.now()
processed_message['@uri'] = '/api/match/{0}'.format(event['id'])
