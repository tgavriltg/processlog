import ConfigParser
def covertListToDict(configFile):
    cf = ConfigParser.ConfigParser()
    cf.read(configFile)
    sectionsList = cf.sections()
    retDict = {}
    for key in sectionsList:
        retDict[key] = dict(cf.items(key))
    return retDict