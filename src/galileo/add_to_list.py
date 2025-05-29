def append_lists(list_one: list[int], list_two: list[int]) -> list[int]:
    res_list = []
    for item in list_one:
        res_list.append(item)
    for item in list_two:
        res_list.append(item)
    return res_list
