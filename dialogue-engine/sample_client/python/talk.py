# -*- coding: utf-8 -*-

import argparse
import requests
import json
import pytz
from datetime import date, datetime


def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def cotoba_agent_call(endpoint, apikey, userid, utternce):

    now = datetime.now(pytz.timezone('Asia/Tokyo'))
    metadata = {}
    params = {
        "locale": "ja-JP",
        "time": now,
        "userId": userid,
        "utterance": utternce,
        "deleteVariable": False,
        "metadata": json.dumps(metadata, ensure_ascii=False)    }

    headers = {'Content-Type': 'application/json;charset="utf-8"'}
    headers = {'x-api-key': apikey}
    r = requests.post(url=endpoint, headers=headers, data=json.dumps(params, default=json_serial, ensure_ascii=False).encode("utf-8"))
    r.encoding = r.apparent_encoding
    r.encoding = 'UTF-8'
    return r.text


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='COTOBA Agent talk sample.')

    parser.add_argument('endpointurl', help='COTOBA Agent endpoint URL.', default=None)
    parser.add_argument('apikey', help='COTOBA Agent api-key.', default=None)
    parser.add_argument('userid', help='userid.', default=None)
    args = parser.parse_args()

    while True:
        utterance = input(">>> ")
        if utterance.startswith('q'):
            break
        response_json = cotoba_agent_call(args.endpointurl, args.apikey, args.userid, utterance)
        response_dict = json.loads(response_json)
        print(response_dict["response"])
