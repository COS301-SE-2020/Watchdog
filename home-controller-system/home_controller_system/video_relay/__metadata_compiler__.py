from datetime import datetime
import json


class __MetaDataCompiler:
    def __init__(self, tag, IP_address):
        self.tag = tag
        self.DateTime = datetime.now()
        self.IP_address = IP_address

    def BufferIDSystem(self):
        TagList = ["random", "movement"]
        if TagList.__contains__(self.tag):
            x = {

                "timestamp": str(self.DateTime)[0:19],
                "ip_address": self.IP_address,
                "hash_id": hash(str(self.DateTime) + self.IP_address),
                "tag": self.tag
            }
            MetaData = json.dumps(x)
            # print(x)
            return MetaData


p1 = __MetaDataCompiler("random", "127.0.0.1")
print(p1.BufferIDSystem())
