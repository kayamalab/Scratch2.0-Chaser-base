# Scratch2.0-Chaser-base
# フォルダの説明
* Procon-Server       ゲームサーバ一式
* Scratchセーブデータ  スクリプト保存先
* logs                ゲームサーバによって利用されるフォルダ
* source code         procon.exeのソースコード
* マップ               ゲームサーバにで利用できるマップ
* IPアドレスをたしかめる.exe localhostのIPアドレスを表示
* NaganoProconClient.exe コンパイル済みのbot
* Procon-Server.exe.lnk ゲームサーバのショートカット
* Scratchサーバー起動.bat procon.exeを最小化で起動するスクリプト
* procon.exe http to Socket
* プロコン拡張パッチ日本語版 HTTP Extensions のブロック情報
# 使い方
Scratchで書かれたbotとC#のbotの対戦は、以下の通りに動作します。
COOLとHOTの接続方法は、Chaserの仕様書を確認してください。
![demo](https://raw.githubusercontent.com/kayamalab/Scratch2.0-Chaser-base/master/image/howtouse.gif)

# Scratchに追加されるブロック
## スタックブロック
* ゲームサーバーを起動する
* IPアドレスの設定をする
* ポート番号の設定をする
* チーム名の設定をする
* ゲームサーバーに接続する
* リセットをする
* 自分のターンを待つ
*  に移動する
*  の周りを見る
*  の遠くまで見る
*  にブロックを置く
## 値ブロック
* ゲームの状態   
* 1 マス目
* 2 マス目
* 3 マス目
* 4 マス目
* 5 マス目
* 6 マス目
* 7 マス目
* 8 マス目
* 9 マス目
* 全てのマス目

# プログラムについて
Chaserに準拠した順序でスタックブロックや値ブロックを組み合わせ通信を行います。
procon.exeは12345ポートでhttpリクエストをlistenします。起動できはい場合はポートが他のプログラムによってlistenされていないことを確認してください。
IPアドレスの初期値は127.0.0.1
ポートは2009です。
「IPアドレスの設定をする」「ポート番号の設定をする」を実行することで変更する事ができます。
# 対戦について
procon.exeはPC1台につき1プロセスしか動作しません。
よってScratchとScratchの対戦はPCが2台必要になることを注意してください。
その際接続がうまく行かない場合は、IP及びポート番号、windowsのファイアウォールの設定が正しくできているかを確認してください。
