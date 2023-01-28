import configparser

config = configparser.ConfigParser()
config.read("config.ini")

MainConfig = config["KYPEde"]
