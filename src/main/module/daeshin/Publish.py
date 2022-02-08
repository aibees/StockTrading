class DSPublish:
    def __init__(self, name, service):
        self.name = name
        self.obj = service
        self.flag = False

    def Subscribe(self, var, caller):
        if self.flag:
            self.Unsubscribe()

        if(len(var) > 0):
            self.obj.SetInputValue(0, var)
