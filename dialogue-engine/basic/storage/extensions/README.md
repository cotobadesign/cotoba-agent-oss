
# How to handle variables in AIML

## conversation

The conversation state is included in the "conversation", which is obtained from the context.
First of all, get the conversation.
```
conversation = context.bot.get_conversation(context)
```

## AIML's "get" equivalent processing

The acquisition of variables created by AIML is divided for each variable type (var, data, name), and the value is acquired by the following implementation.

### <get var="key"/>
```
value = conversation.current_question().property("key")
```

### <get data="key"/>
```
value = conversation.data_property("key")
```

### <get name="key"/>
```
value = conversation.property("key")
```


## AIML's "set" equivalent processing

The method of passing the variable value in the extension to the variable of AIML is divided for each variable type (var, data, name), and the value is set in each implementation below.

### <set var="key">value</set>
```
conversation.current_question().set_property("key", "value")
```

### <set cata="key">value</set>
```
conversation.set_data_property("key", "value")
```

### <set name="key">value</set>
```
conversation.property("key", "value")
```


## AIML's "bot" equivalent processing
The value specified in "propaties/propaties.txt" is acquired by the following implementation.

### <bot name="app_version" />
```
value = context.bot.brain.properties.property("app_version")
```

## AIML's "json" equivalent processing

The acquisition method is different for each variable type, but it is acquired and set by the same method as get/set described above.
AIML handles all textual information. Therefore, the type of the input/output variable type is "str". After getting the value, convert it to "dict" type and perform the operation.


### <json name="key.name"/>
Since the contents of json are stored as text, after getting it, convert it to dict type with json.loads() and use the value.

```
value = conversation.property("key")
json_dict = json.loads(value)
result = json_dict["name"]
```

### <json name="key.name">Smith</json>
When handling the dict type changed in python in the json node of AIML, assign the dict type as text in json.dumps() with the same function as set.

```
value = conversation.property("key")
json_dict = json.loads(value)
json_dict["name"] = "Smith"
value = conversation.set_property("key", json.dumps(json_dict, ensure_ascii=False))
```

## Return value
The character string returned by "return" is the processing result as a node.
In other words, it will be the result of the extension node of AIML and will be used on the AIML side.