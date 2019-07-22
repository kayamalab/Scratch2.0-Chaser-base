
# coding: utf-8

import socket

class client:
    def connection_to_server(self,host,port,team):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         #通信オブジェクトの作成をします
        self.client.connect((host, port))                                       #これでサーバーに接続します
        self.client.send(team.encode("UTF-8")+b"\r\n")                          #
    def get_ready(self):
        response = self.client.recv(4096)                                       #仕様書だと＠が入る（何が何でも＠なのでゴミ箱行き）
        self.client.send(b"gr\r\n")
        response = self.client.recv(4096)
        return self.game_check(response)
    def walk(self,direction):
        if direction=="up":
            self.client.send(b"wu\r\n")
        elif direction=="right":
            self.client.send(b"wr\r\n")
        elif direction=="left":
            self.client.send(b"wl\r\n")
        elif direction=="down":
            self.client.send(b"wd\r\n")
        response = self.client.recv(4096)
        self.client.send(b"#\r\n")
        return self.game_check(response)
    def look(self,direction):
        if direction=="up":
            self.client.send(b"lu\r\n")
        elif direction=="right":
            self.client.send(b"lr\r\n")
        elif direction=="left":
            self.client.send(b"ll\r\n")
        elif direction=="down":
            self.client.send(b"ld\r\n")
        response = self.client.recv(4096)
        self.client.send(b"#\r\n")
        return self.game_check(response)
    def search(self,direction):
        if direction=="up":
            self.client.send(b"su\r\n")
        elif direction=="right":
            self.client.send(b"sr\r\n")
        elif direction=="left":
            self.client.send(b"sl\r\n")
        elif direction=="down":
            self.client.send(b"sd\r\n")
        response = self.client.recv(4096)
        self.client.send(b"#\r\n")
        return self.game_check(response)
    def put(self,direction):
        if direction=="up":
            self.client.send(b"pu\r\n")
        elif direction=="right":
            self.client.send(b"pr\r\n")
        elif direction=="left":
            self.client.send(b"pl\r\n")
        elif direction=="down":
            self.client.send(b"pd\r\n")
        response = self.client.recv(4096)
        self.client.send(b"#\r\n")
        return self.game_check(response)
    def game_check(self,response):
        response=response.decode("UTF-8")[:-2]
        if 0==int(response[0]):
            print("サーバーからゲームの終了通知を受けました")
            self.client.send(b"#\r\n")
            return 0
        else :
            response=response[1:]
            result=[]
            for i in response:
                result.append(int(i))
            return result



# In[22]:


#robot=client()


# In[23]:


#robot.connection_to_server()
