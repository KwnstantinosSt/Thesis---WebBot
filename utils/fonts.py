def getFontWeight(value):
    name = ""
    try:
        if (int(value) == 100):
            name = "Thin, Hairline, Ultra-light, Extra-light"
        elif (int(value) == 200):
            name = "Light"
        elif (int(value) == 300):
            name = "Book"
        elif (int(value) == 400):
            name = "Regular, Normal, Plain, Roman, Standard"
        elif (int(value) == 500):
            name = "Medium"
        elif (int(value) == 600):
            name = "Semi-bold, Demi-bold"
        elif (int(value) == 700):
            name = "Bold"
        elif (int(value) == 800):
            name = "Heavy, Black, Extra-bold"
        elif (int(value) == 900):
            name = "Ultra-black, Extra-black, Ultra-bold, Heavy-black, Fat, Poster"
        else:
            name = "No Data"
        return name
    except Exception as ex:
        print(ex)
