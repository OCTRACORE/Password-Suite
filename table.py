class Table(): #class for storing the passwords with their description
    count  = 1
    def __init__(self,passwd,desc):
        self.passwd = passwd
        self.desc = desc
        self.id = Table.count
        Table.count += 1
    def count_init(self):
        Table.count  = 1 