import configparser

def readConfigFile(cfgfile):
    parser = configparser.ConfigParser()
    parser.read(cfgfile)
    return parser

CONFIG = readConfigFile("../em2a.config")
