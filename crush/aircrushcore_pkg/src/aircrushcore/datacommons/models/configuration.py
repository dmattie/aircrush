import configparser

class CommonsConfiguration():
    self.commons_path=""
    self.staging_path=""
    

    def __init__(self):

        config = configparser.ConfigParser()
        config.read('../../../../crush.ini')
        self.commons_path = config['COMMONS']['commons_path']
        self.staging_path = config['COMMONS']['staging_path']
