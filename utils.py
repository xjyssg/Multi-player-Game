class Request_Message:
    def __init__(self, version="1.0", delimiter='\n'):
        self.version = version
        self.delimiter = delimiter

    def generate_message(self, method, content):
        message = self.version + self.delimiter + method + self.delimiter + content
        encoded = message.encode("ascii")
        return encoded

    def resolve_message(self, message):
        decoded = message.decode("ascii")
        fields = decoded.split(self.delimiter)
        return fields
        

class Response_Message:
    def __init__(self, version="1.0", delimiter='\n'):
        self.version = version
        self.delimiter = delimiter

    def generate_message(self, status, content):
        message = self.version + self.delimiter + status + self.delimiter + content
        encoded = message.encode("ascii")
        return encoded

    def resolve_message(self, message):
        decoded = message.decode("ascii")
        fields = decoded.split(self.delimiter)
        return fields




