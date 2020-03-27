# NLU sample for COTOBA Agent OSS

## Installation

1. Install MeCab.
1. Install Docker. (to run nlu service in localhost.)
1. Install python 3.6 (and above)
   - It is recommended to use virtual environment such as venv.
1. `$ pip install -r requirements.txt`

## Quick demo

1. `$ ./download_sample_model.sh`
   - Download sample model by using wget.
1. `$ docker-compose build`
1. `$ docker-compose up -d`
1. `$ curl -s -X POST -H 'Content-Type:application/json' -d '{"utterance": "渋谷でカレーがおいしいところ教えて"}' http://localhost:5000/nlu`

   ```json
   {
      "text": "渋谷でカレーがおいしいところ教えて",
      "intents": [
         {
            "intent": "レストラン検索",
            "score": 0.9993921518325806
         }
      ],
      "slots": [
         {
            "slot": "場所",
            "startOffset": 0,
            "endOffset": 2,
            "entity": "渋谷",
            "score": 1.0
         },
         {
            "slot": "料理名",
            "startOffset": 3,
            "endOffset": 6,
            "entity": "カレー",
            "score": 1.0
         }
      ]
   }
   ```

1. `$ docker-compose down`

## How to train and use your original model

1. Prepare training data in cotoba agent format.
   - See [training_data_sample.json](training_data_sample.json)
1. Convert training data.
   - `$ python script/convert.py config_samples/convert.yaml`
   - See [config_samples/convert.yaml](config_samples/convert.yaml)
1. Train model for intent.
   - `$ python script/train.py config_samples/train_intent.yaml`
   - See [config_samples/train_intent.yaml](config_samples/train_intent.yaml)
1. Train model for slot.
   - `$ python script/train.py config_samples/train_slot.yaml`
   - See [config_samples/train_slot.yaml](config_samples/train_slot.yaml)
1. Test model.
   - `$ python script/test.py config_samples/test.yaml`
   - See [config_samples/test.yaml](config_samples/test.yaml)
1. Intaractive demo.
   - `$ python script/run.py config_samples/run.yaml`
   - See [config_samples/run.yaml](config_samples/run.yaml)
1. Up nlu servcice by using docker-compose.
   - Modify `INTENT_MODEL_PATH` and `SLOT_MODEL_PATH` in [docker-compose.yml](docker-compose.yml) and run docker conatiner like the above-mentioned way.

Please see configure samples for details.

## License

[MIT License](LICENSE)
