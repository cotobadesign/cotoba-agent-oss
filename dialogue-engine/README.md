# COTOBA Agent dialogue engine

COTOBA Agent dialogue engine is an AIML dialogue description language processing engine written in Python3.  
Contains programs for building your own interactions using the Artificial Intelligence Markup Language (AIML).  
The COTOBA Agent dialogue engine supports tags defined in the interactive language AIML2.0.  
In addition, we extend our own extensions, such as tags that handle json, tags that call the REST interface, and tags that use the results of advanced interpretation.  
The interactive description language can support multilingual input, and the program supports Japanese and English, and it is possible to support multiple languages by adding its own tokenize processing.  
Please refer to [Wiki](https://github.com/cotobadesign/cotoba-agent-dialogue-engine/wiki) for the COTOBA Agent dialogue engine, its functions and details.  


# Requirements

The COTOBA Agent dialogue engine runs across the cross-platform of Mac OSX, Linux, and Windows.  
The program is written in Python3 and the version is confirmed to work in 3.7.


# Quick Start

## Preparation
You need to install the tokenizer [mecab](https://taku910.github.io/mecab/) for japanese processing.

* Mac OSX
```
        $brew install mecab
        $brew install mecab-ipadic
```

* Linux(Ubuntu)

```
        $sudo apt install mecab
        $sudo apt install libmecab-dev
        $sudo apt install mecab-ipadic-utf8
```

* Windows  
        See: https://github.com/ikegami-yukino/mecab/releases/tag/v0.996


## Installation

```
$ git clone https://github.com/cotobadesign/cotoba-agent-dialogue-engine.git
$ cd cotoba-agent-dialogue-engine
$ pip3 install -r requirements.txt
```

## Running the program by console
To start the program as a console application, run the following command.

```
$ cd basic/script
$ export PYTHONPATH=PYTHONPATH=:../../src 
$ python3 -m programy.clients.events.console.client --config ../config/config.yaml --cformat yaml --logging ../config/logging.yaml
```

### Dialogue processing by console
When the program starts, you will be prompted, entering a utterance.  
  
Example:
``` 
>>> good morning  
Did you sleep well until morning?  
>>> yes  
It's nice to wake up in the morning.  
>>> おはよう  
夜更かしせずに寝ていますか？  
>>> はい  
朝は、すっきり目が覚めることができたんですね。  
>>> What time is it now   
12:43:41  
>>> 今何時  
12時43分51秒です。  
>>>  
```

## Running the program by REST interface
To start the program as a rest interface application, run the following command.

```
$ cd basic/script
$ export PYTHONPATH=PYTHONPATH=:../../src 
$ python3 -m programy.clients.restful.yadlan.sanic.client  --config ../config/config.yaml --cformat yaml --logging ../config/logging.yaml --stdoutlog True

```

After launching the interactive application, run [simple_request.py](https://github.com/cotobadesign/cotoba-agent-dialogue-engine/blob/master/dialogue-engine/basic/script/simple_request.py) on a different console.

### Dialogue processing by REST interface
When the [simple_request.py](https://github.com/cotobadesign/cotoba-agent-dialogue-engine/blob/master/dialogue-engine/basic/script/simple_request.py) starts, as with console applications, you can enter utterances to see the response statements in the scenario.

By launching the dialogue engine on the Internet, you can also be called from smartphone applications.

# License
This software is released under the MIT License, see [COPYRIGHT](https://github.com/cotobadesign/cotoba-agent-dialogue-engine/blob/master/dialogue-engine/COPYRIGHT.txt).

# Contact
* [Web site](https://cotoba.net)  
* [issue](https://github.com/cotobadesign/cotoba-agent-dialogue-engine/issues) Raise an issue directly  
