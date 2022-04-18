import abc
#https://realpython.com/python-interface/

# method_list = ['create','read','update','delete']
method_list = ["get_battery_sorted_by_cell_diff"]

class DbInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        finalBool = True
        for method in method_list:
            finalBool = finalBool and (
                hasattr(subclass, method) and
                callable(subclass[method])
            )
        return finalBool or NotImplemented

    @abc.abstractmethod
    def get_battery_sorted_by_cell_diff():
        raise NotImplementedError

    # @abc.abstractmethod
    # def read():
    #     raise NotImplementedError


    # @abc.abstractmethod
    # def update():
    #     raise NotImplementedError

    # @abc.abstractmethod
    # def delete():
    #     raise NotImplementedError