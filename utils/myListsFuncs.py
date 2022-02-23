def groupByList(mylist=[]):
    newList = []
    for i in range(len(mylist)):
        if mylist[i] not in newList:
            newList.append(mylist[i])
    return newList


def countItems(mylist=[]):
    groupedList = groupByList(mylist)
    items = {}
    for i in range(len(groupedList)):
        items.update({f"Depth {i}": mylist.count(i)})
    return items
