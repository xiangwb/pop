def format_response(data, msg, code, **kwargs):
    res = {
        "data": data,
        "msg": msg,
        "code": code
    }
    res.update(**kwargs)
    return res
