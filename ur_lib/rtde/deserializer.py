import sys
sys.path.append('..')

from rtde import serialize

class Deserializer(object):
    
    def __init__(self, names, types):
        if len(names) != len(types):
            raise ValueError('List sizes are not identical.')
        self.__names = names
        self.__types = types
        self.__header_names = []
        self.__columns = 0
        for i in range(len(self.__names)):
            size = serialize.get_item_size(self.__types[i])
            self.__columns += size
            if size > 1:
                for j in range(size):
                    name = self.__names[i]+'_'+str(j)
                    self.__header_names.append(name)
            else:
                name = self.__names[i]
                self.__header_names.append(name)
    
    def print_header(self):
        print(self.__header_names)
    
    def deserialize(self, data_object) -> list:
        data = []
        for i in range(len(self.__names)):
            size = serialize.get_item_size(self.__types[i])
            value = data_object.__dict__[self.__names[i]]
            if size > 1:
                data.extend(value)
            else:
                data.append(value)
        return data
    