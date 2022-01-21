# COTOBA Agent dialogue engine

COTOBA Agent dialogue engineは、Python3で記述されたAIML対話記述言語処理エンジンです。  
Artificial Intelligence Markup Language（AIML）を使用して独自の対話処理を構築するためのプログラムが含まれています。  
COTOBA Agent dialogue engineは、対話処理言語AIML2.0で定義されたタグをサポートしています。  
また、独自に拡張を行った、jsonを取り扱うタグ、RESTインタフェースを呼び出すタグ、高度意図解釈の結果を利用するタグ等の拡張を行っています。  
対話記述言語は多言語の入力に対応することができ、プログラムでは日本語、英語に対応しており、独自の分かち書き処理を追加することで複数の言語に対応することが可能です。  
COTOBA Agent dialogue engine、その機能、詳細については、[ドキュメントサイト](https://cotoba-agent-oss-docs-ja.readthedocs.io/en/latest/)を参照してください。  



# システム要件

COTOBA Agent dialogue engineはMac OSX,Linux,Windowsのクロスプラットフォームで動作します。  
プログラムはPython3で記述されており、バージョンは3.7および3.8で動作確認をしています。


# クイックスタート

## 事前準備
日本語の分かち書きを行うために、[mecab](https://taku910.github.io/mecab/)をインストールする必要があります。


### macOS
```
        $brew install mecab
        $brew install mecab-ipadic
```

### Linux (Ubuntu)
```
        $sudo apt install mecab
        $sudo apt install libmecab-dev
        $sudo apt install mecab-ipadic-utf8
```

### Windows (Windows 10)
WSL (Windows Subsystem for Linux) の Ubuntu をインストールして上記の Linux(Ubuntu)と同じ手順で mecab をセットアップしてください。

WSL インストールの参考サイト: https://qiita.com/matarillo/items/61a9ead4bfe2868a0b86

## インストール

```
$ git clone https://github.com/cotobadesign/cotoba-agent-oss.git
$ cd cotoba-agent-oss/dialogue-engine/
$ pip3 install -r requirements.txt
```

## コンソールアプリケーションとしての起動方法
コンソールアプリケーションとしてプログラムを実行するには以下の手順でプログラムを起動します。

```
$ cd basic/script
$ export PYTHONPATH=PYTHONPATH=:../../src 
$ python3 -m programy.clients.events.console.client --config ../config/config.yaml --cformat yaml --logging ../config/logging.yaml
```

### コンソールアプリケーションの操作方法
プログラムが起動すると、以下のようにプロンプトが表示されるので文章を入力してください。
basic/storage/categories/にあるAIMLで記載されたシナリオが動作します。

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

## RESTインターフェースとしての起動方法
RESTインタフェースのプログラムを実行するには以下の手順でプログラムを起動します。
プログラムが起動すると、RESTアクセスの待ち受け状態になります。

```
$ cd basic/script
$ export PYTHONPATH=PYTHONPATH=:../../src 
$ python3 -m programy.clients.restful.yadlan.sanic.client  --config ../config/config.yaml --cformat yaml --logging ../config/logging.yaml --stdoutlog True --stderrlog True

```

別途クライアントアプリケーション、 [simple_request.py](https://github.com/cotobadesign/cotoba-agent-oss/blob/master/dialogue-engine/basic/script/simple_request.py)を実行して、RESTアクセス待ちを行っている対話エンジンにアクセスを行ってください。

### RESTインタフェースアクライアントプリケーションの使用方法
[simple_request.py](https://github.com/cotobadesign/cotoba-agent-oss/blob/master/dialogue-engine/basic/script/simple_request.py) が起動すると、コンソールアプリ同様プロンプトが表示されるので、文章を入力してください。

対話エンジンをインターネットサーバ上で起動することで、スマートフォン用アプリケーションなどからも呼び出すことができます。

# ライセンス
本ソフトウェアはMITライセンスです。詳細は[COPYRIGHT](https://github.com/cotobadesign/cotoba-agent-oss/blob/master/dialogue-engine/COPYRIGHT.txt)を参照してください。

# Contact
* [Web site](https://www.cotoba.net)
* [issue](https://github.com/cotobadesign/cotoba-agent-oss/issues) Raise an issue directly  
