class ImproperBillingConfig(Exception):
    def __init__(self, err):
        self.err = err

class ImproperProductConfig(Exception):
    def __init__(self, err):
        self.err = err

class ImproperSettingsConfig(Exception):
    def __init__(self, err):
        self.err = err

class ImproperJobsConfig(Exception):
    def __init__(self, err):
        self.err = err
