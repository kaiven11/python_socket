#coding=utf-8

step1=2**0
step2=2**1
step3=2**2
step4=2**3

step_all=(step1|step2|step3|step4)


class testevent():
    def __init__(self):
        self._listener=[]

    def add_listener(self,method,mask):
        self._listener.append((method,mask))

    def print_step1(self):
        self.dispatch_event(step1)

    def print_step2(self):
        self.dispatch_event(step2)

    def print_step3(self):
        self.dispatch_event(step3)

    def print_step4(self):
        self.dispatch_event(step4)

    def dispatch_event(self,event):
        for cb,mask in self._listener:
            if event&mask:
                cb(event)

def mymethod(e):
    print("this is step:%s"%e)


if __name__ == '__main__':
    m=testevent()
    m.add_listener(mymethod,step4|step3)
    m.print_step1()
    m.print_step2()
    m.print_step3()
    m.print_step4()

