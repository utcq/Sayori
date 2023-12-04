class void:
    def __init__(self):
        pass

    def __repr__(self):
        return f"void"

class uint8_t:
    def __init__(self, value:int=0):
        self.value=value
    
    def __int__(self):
        return self.value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"{self.value}"

class uint16_t:
    def __init__(self, value:int=0):
        self.value=value
    
    def __int__(self):
        return self.value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"{self.value}"

class uint32_t:
    def __init__(self, value:int=0):
        self.value=value
    
    def __int__(self):
        return self.value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"{self.value}"

class uint64_t:
    def __init__(self, value:int=0):
        self.value=value
    
    def __int__(self):
        return self.value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"{self.value}"

class int8_t:
    def __init__(self, value:int=0):
        self.value=value
    
    def __int__(self):
        return self.value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"{self.value}"

class int16_t:
    def __init__(self, value:int=0):
        self.value=value
    
    def __int__(self):
        return self.value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"{self.value}"

class int32_t:
    def __init__(self, value:int=0):
        self.value=value
    
    def __int__(self):
        return self.value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"{self.value}"

class int64_t:
    def __init__(self, value:int=0):
        self.value=value
    
    def __int__(self):
        return self.value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"{self.value}"
    
class char:
    def __init__(self, value:str='\0'):
        self.value=value
    
    def __str__(self):
        return self.value

    def __repr__(self):
        return f"{self.value}"


class Define:
    def __init__(self, value:any):
        self.value=value


class TPointer:
    def __init__(self, val:any):
        self.val=val

class TReference:
    def __init__(self, val:any):
        self.val=val


class OPointer:
    def __init__(self, val:any):
        self.val=val

class OReference:
    def __init__(self, val:any):
        self.val=val