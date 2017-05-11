from time import asctime

class Logger():

    def __init__(self):
        self.logs = None

    def log(self, message):

        file = open('bin/logs', 'w')

        line = '{}    <{}>\n'.format(message, asctime())
        file.write(line)
        file.close()
        return 'Message logged to file'


    def see_logs(self):
        file = open('../bin/{}','r')
        message = file.readlines(-1)
        file.close()
        return message
