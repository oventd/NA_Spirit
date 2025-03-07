class Singleton(object):
    def __new__(cls):
        if not hasattr(cls,'instance'):
            print('create')
            cls.instance = super(Singleton, cls).__new__(cls)
        else:
            print('recycle')
        return cls.instance
 
print('1번째 생성')
s1 = Singleton() # create
print('2번째 생성')
s2 = Singleton() # recycle
print('s1 == s2')
print(s1==s2) # true
