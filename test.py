from run import getHospitalWaitTimes

def getHTML(data):
    html = ["< table id = 'Wait_times' >"]

    for key, value in data.items():
        html.append("< tr >")
        html.append("< td > {0} < / td >".format(key))
        html.append("< td > {0} < / td >".format(value))
        html.append("< / tr >")

    html.append("< / table >")

    return "\n".join(html)


if __name__ == "__main__":
    data = getHospitalWaitTimes()
    htmlcode = getHTML(data)
    print (htmlcode)