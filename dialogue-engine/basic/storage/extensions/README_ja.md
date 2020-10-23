
# AIMLの編集操作方法

## conversation

対話状態はcontextから取得する、conversationに含まれています。  
まず最初に、conversationを取得します。

```
conversation = context.bot.get_conversation(context)
```

## AIMLの"get"ノードと同等の実装
AIMLで作成した変数の取得は、変数タイプ(var,data,name)毎に分かれており各々以下の実装で値を取得します。

### \<get var="key"/>

```
value = conversation.current_question().property("key")
```

### \<get data="key"/>
```
value = conversation.data_property("key")
```

### \<get name="key"/>
```
value = conversation.property("key")
```


##  AIMLの"set"ノードと同等の実装
extensionでの変数値をAIMLの変数に受け渡す方法は、変数タイプ(var,data,name)毎に分かれており各々以下の実装で値を設定します。

### \<set var="key">value\</set>
```
conversation.current_question().set_property("key", "value")
```

### \<set cata="key">value\</set>
```
conversation.set_data_property("key", "value")
```

### \<set name="key">value\</set>
```
conversation.property("key", "value")
```


## AIMLの"bot"ノードと同等の実装
propaties/propaties.txtで指定した内容は、以下の実装で取得します。

### \<bot name="app_version" />
```
value = context.bot.brain.properties.property("app_version")
```

## AIMLの"json"ノードと同等の実装
変数タイプ毎に取得方法が分かれますが、前述のgetおよびsetと同様の方法で取得、設定するします。  
AIMLでは全てテキスト化した情報を取り扱うため、入出力される変数の型はstrで、取得後dictに変換し操作を行います。

### \<json name="key.name"/>
jsonの内容はテキスト化し保持しているため、取得後json.loads()でdict型に変換し値を利用します。

```
obj = conversation.property("key")
json_dict = json.loads(obj)
value = json_dict["name"]
```

### \<json name="key.name">Smith\</json>
pythonで変更したdict型をAIMLのjsonノードで取り扱う場合、dict型をjson.dumps()でテキスト化した情報をsetと同じ関数で設定します。
```
obj = conversation.property("key")
json_dict = json.loads(obj)
json_dict["name"] = "Smith"
conversation.set_property("key", json.dumps(json_dict, ensure_ascii=False))
```

## 戻り値
returnで返す文字列がノードとしての処理結果となります。  
つまりreturn値がAIMLのextensionノードの結果となり、AIML側で利用されるます。
