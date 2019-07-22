from aiohttp import web
import pyclient as pyclient
import time
import os
import subprocess

class Scratch_ex:

    ###初期設定
    def __init__(self):
        self.matrices=0
        self.gamestatus=0
        self.getreadyok=0
        self.port=2009
        self.ip="127.0.0.1"
        self.teamname="team"
        self.session=pyclient.client()
        self.busy=0
        self.skipmessagecount=0
    ###関数
    def direction_convert_jp(self,direction):
        if direction=="up":
            return "上"
        elif direction=="right":
            return "右"
        elif direction=="left":
            return "左"
        elif direction=="down":
            return "下"
    def act(self,mode,direction):
        if self.gamestatus!=1:
            print("サーバに接続されていません。")
        elif self.getreadyok==0:
            print("準備がされていません　スキップします")
        else:
            try:
                if mode =="walk":
                    self.matrices=self.session.walk(direction)
                elif mode=="look":
                    self.matrices=self.session.look(direction)
                elif mode=="search":
                    self.matrices=self.session.search(direction)
                elif mode=="put":
                    self.matrices=self.session.put(direction)
            except :
                print("コネクションが切断されました。")
                print("ゲームの状態はリセットするまで2になります")
                self.session=pyclient.client()
                self.gamestatus=2
                return 
            if self.matrices==0:
                print("コネクションを切断します。")
                print("ゲームの状態はリセットするまで2になります")
                self.session=pyclient.client()
                self.gamestatus=2
                return 
            if mode =="walk":
                print(self.direction_convert_jp(direction),"に移動")
            elif mode=="look":
                print(self.direction_convert_jp(direction),"の周りを見る")
            elif mode=="search":
                print(self.direction_convert_jp(direction),"の遠くを見る")
            elif mode=="put":
                print(self.direction_convert_jp(direction),"にブロックを設置")
            self.getreadyok=0
            print()
        return
            
    ###変数・通信設定
    async def handle_serverip(self, request):
        self.busy = request.match_info['busyid']
        self.ip = request.match_info['ip']
        print("次のIPアドレスが設定されました",self.ip)
        self.busy=0
        return web.Response(text="OK")

    async def handle_serverport(self, request):
        self.busy = request.match_info['busyid']
        self.port = request.match_info['port']
        print("次のportが設定されました",self.port)
        self.busy=0
        return web.Response(text="OK")
    
    async def handle_teamname(self, request):
        self.busy = request.match_info['busyid']
        self.teamname = request.match_info['team']
        print("次のチーム名が設定されました",self.teamname)
        self.busy=0
        return web.Response(text="OK")

    async def handle_server(self, request):
        self.busy = request.match_info['busyid']
        if self.gamestatus==1:
            print("接続済みです。")
        else:
            print("IPアドレス:",self.ip," port:",self.port,"に接続します。")
            print("チーム名は",self.teamname,"です。")
            try:
                self.session.connection_to_server(self.ip,int(self.port),self.teamname)
                self.gamestatus=1
            except :
                print("サーバー接続に失敗しました。")
                self.gamestatus=0
            if self.gamestatus==1:
                print("サーバーに接続しました。")
        self.busy=0
        return web.Response(text="OK")

    async def handle_reset(self, request):
        self.busy = request.match_info['busyid']
        os.system('cls')
        self.matrices=0
        self.gamestatus=0
        self.getreadyok=0
        self.port=2009
        self.ip="127.0.0.1"
        self.teamname="team"
        self.session=pyclient.client()
        self.busy=0
        self.skipmessagecount=0
        print("リセットが完了しました。")
        return web.Response(text="OK")



    ###スクラッチ動作部
    async def handle_poll(self,request):
        text = "matrices " + str(self.matrices) + "\n"
        text =text+"gamestatus " + str(self.gamestatus) + "\n"
        if type(self.matrices) is list:
            for i in range(9):
                text =text+"block"+str(i+1)+" "+str(self.matrices[i])+ "\n"
        else:
            for i in range(9):
                text =text+"block"+str(i+1)+" "+str(0)+ "\n"

        if self.busy!=0:
            text = text+"_busy "+str(self.busy)
        return web.Response(text=text)

    async def handle_getready(self, request):
        
        self.busy = request.match_info['busyid']
        if self.gamestatus!=1:
            print("サーバに接続されていません。")
        elif self.getreadyok==1:
            print("すでにこちらのターンです")
        else :
            print("準備を開始")
            try:
                self.matrices=self.session.get_ready()
            except :
                print("コネクションが切断されました。")
                print("ゲームの状態はリセットするまで2になります")
                self.session=pyclient.client()
                self.gamestatus=2
            if self.matrices==0:
                print("コネクションを切断します。")
                print("ゲームの状態はリセットするまで2になります")
                self.gamestatus=2
                self.session=pyclient.client()
                self.busy=0
                return web.Response(text="OK")
            print("準備が完了しました。こちらのターンです。")
            self.getreadyok=1
        self.busy=0
        return web.Response(text="OK")

    async def handle_walk(self, request):
        self.busy = request.match_info['busyid']
        self.act("walk",request.match_info['direction'])
        self.busy=0
        return web.Response(text="OK")

    async def handle_look(self, request):
        self.busy = request.match_info['busyid']
        self.act("look",request.match_info['direction'])
        self.busy=0
        return web.Response(text="OK")

    async def handle_search(self, request):
        self.busy = request.match_info['busyid']
        self.act("search",request.match_info['direction'])
        self.busy=0
        return web.Response(text="OK")

    async def handle_put(self, request):
        self.busy = request.match_info['busyid']
        self.act("put",request.match_info['direction'])
        self.busy=0
        return web.Response(text="OK")
    async def handle_start_server(self,request):
        self.busy = request.match_info['busyid']
        try:
            subprocess.Popen(r'.\Procon-Server\Procon-Server.exe')
        except:
            print("プロコンサーバーを見つけられませんでした。")
            print(".\Procon-Server\Procon-Server.exe not find")
        self.busy=0
        return web.Response(text="OK")
    #######help
    async def handle_help(self, request):
        self.busy = request.match_info['busyid']
        helpmode=1
        while helpmode!=0:
            os.system('cls')
            print("#"*30)
            
            print("次から見たいhelpを数字で指定してください")
            print()
            print("get help Agent block     =2")
            print("set server ip            =3")
            print("set server port          =4")
            print("set team name            =5")
            print("connect to server        =6")
            print("connection reset         =7")
            print("getready                 =8")
            print("walk to 向き             =9")
            print("look to 向き             =10")
            print("search to 向き           =11")
            print("put to   向き            =12")
            print("get game status          =13")
            print("get matrices             =14")
            print("1~9block data            =15")
            print("ヘルプを終了します          =0")
            temp=input("=")
            if temp=="":
                temp="hoge"
            try:
                helpmode=int(temp)
            except :
                print("整数を入力してください　全角ではありませんか？")
                helpmode=1
            if(helpmode==2):
                print("helpモードを起動します")
            if(helpmode==3):
                print("プロコンサーバーのIPアドレスを指定します。ローカルでは[127.0.0.1]です。対戦を行う場合は変更が必要になります。")
            if(helpmode==4):
                print("プロコンサーバーのポート番号を指定します。coolは2009 hotは2010 が初期値です。")
            if(helpmode==5):
                print("プロコンサーバーに通知するチーム名を指定します。お好きにどうぞ、と言いたいところですが、日本語はうまく表示できないようです。")
            if(helpmode==6):
                print("設定されたIPとポートを使用し、プロコンサーバーに接続を行います。初期値が内部で設定されているため、IPとポートを設定しなくても、プロコンサーバーに接続できることがあります。")
            if(helpmode==7):
                print("プロコンサーバーとの接続を終了し、リセットを行います。基本的にはゲーム終了後に、この実行ファイルを再度起動する手間を省くためのものです。")
            if(helpmode==8):
                print("プロコンサーバーに対して、「getready」を送信します。プロコンサーバーに接続されていなければ処理はスキップされます。ターン中に実行した場合、処理をスキップする保護機能があります。")
            if(helpmode==9):
                print("プロコンサーバーに対して、「walk」を送信します。プロコンサーバーに接続されていなければ処理はスキップされます。ターン外に実行した場合、処理をスキップする保護機能があります。")
            if(helpmode==10):
                print("プロコンサーバーに対して、「look」を送信します。プロコンサーバーに接続されていなければ処理はスキップされます。ターン外に実行した場合、処理をスキップする保護機能があります。")
            if(helpmode==11):
                print("プロコンサーバーに対して、「search」を送信します。プロコンサーバーに接続されていなければ処理はスキップされます。ターン外に実行した場合、処理をスキップする保護機能があります。")
            if(helpmode==12):
                print("プロコンサーバーに対して、「put」を送信します。プロコンサーバーに接続されていなければ処理はスキップされます。ターン外に実行した場合、処理をスキップする保護機能があります。")
            if(helpmode==13):
                print("現在のゲームの状態が示されます。ゲーム開始前=0 ゲーム中=1 ゲーム終了=2　となります")
            if(helpmode==14):
                print("各行動によって得られた周辺情報が示されます。配列の形式が好きな方はこちらを利用してください。[,]も一文字となりますので、１マス目は２、５マス目は１０　といったように、マス目の２倍を指定する必要があります。")
            if(helpmode==15):
                print("各行動によって得られた周辺情報が示されます。それぞれがマス目の状態なのでそのまま使うことができます。")
            input("続けるにはなにかキーを入力してください。")
        print("helpを終了します。")
        self.busy=0
        return web.Response(text="OK")
    def main(self):
        """ Main routine """
        app = web.Application()
        app.router.add_get('/poll', self.handle_poll)


        app.router.add_get('/start_server/{busyid}', self.handle_start_server)
        app.router.add_get('/server/{busyid}', self.handle_server)
        app.router.add_get('/help/{busyid}', self.handle_help)
        app.router.add_get('/reset/{busyid}', self.handle_reset)
        app.router.add_get('/serverip/{busyid}/{ip}', self.handle_serverip)
        app.router.add_get('/serverport/{busyid}/{port}', self.handle_serverport)
        app.router.add_get('/teamname/{busyid}/{team}', self.handle_teamname)

        app.router.add_get('/getready/{busyid}', self.handle_getready)
        app.router.add_get('/walk/{busyid}/{direction}', self.handle_walk)
        app.router.add_get('/look/{busyid}/{direction}', self.handle_look)
        app.router.add_get('/search/{busyid}/{direction}', self.handle_search)
        app.router.add_get('/put/{busyid}/{direction}', self.handle_put)
        web.run_app(app, host='127.0.0.1', port=12345)

if __name__ == '__main__':
    s2extest = Scratch_ex()
    s2extest.main()
    