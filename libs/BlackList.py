# 読み込み
def read_bl(text):
    if text == "":
        return []
    else:
        tl = text.split(",")
        del tl[-1]
        return tl


# 追加
def add_bl(text, user_id):
    tl = text.split(",")
    del tl[-1]
    if user_id in tl:
        return text
    else:
        return text + "{},".format(user_id)


# 削除
def delete_bl(text, user_id):
    tl = text.split(",")
    del tl[-1]
    if user_id in tl:
        tl.remove(user_id)
        if len(tl) == 0:
            return ""
        else:
            added_tl = ",".join(tl)
            return added_tl + ","
    else:
        return text


# 読み込んだリストを数値に変換
def str_to_int(s_list):
    i_list = []
    for s in s_list:
        try:
            i_list.append(int(s))
        except ValueError:
            pass
    return i_list
