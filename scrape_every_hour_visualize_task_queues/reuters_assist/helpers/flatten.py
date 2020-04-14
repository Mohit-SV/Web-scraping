output = {}


def flat(x, input):
    global output
    for i in x:
        if not isinstance(x.get(i), dict):
            this_key = (input+'.'+i).split('.',1)[1]
            val = x.get(i)
            output[this_key] = {
                                "end_key_type": type(i),
                                "value": val,
                                "value_type": type(val)
                                }
        else:
            flat(x.get(i), input+'.'+i)


def flatten(x):
    flat(x, "")
    return output


