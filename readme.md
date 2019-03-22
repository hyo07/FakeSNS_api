# 簡易 短文投稿SNS

## 環境
- Mac
- Python 3.6.5
- Django 2.1.7

## 実装した機能
- アカウント作成
- ログイン、ログアウト
- 記事一覧、投稿、編集、削除
- ユーザーページ
- プロフィール登録、編集
- ブラックリスト登録、削除
- いいね追加、削除
- パスワード変更
- いいね一覧
- 投稿した記事一覧

スーパーユーザーは、自分以外のユーザーが投稿した文書も編集・削除が可能です。

## 環境構築
```commandline
brew install pyenv
brew install pipenv 
```
まずpyenvとpipenvをインストールします  

```commandline
cd ~/FakeSNS
pipenv shell
```
その後アプリケーションのあるディレクトリに移動したあと、  
.venvファイルのある階層で仮想環境を起動。.venvから仮想環境を読み込みます。  

すると
```commandline
.venv ❯
```
といった状態になれば、仮想環境の起動に成功しています。  
この状態で
```commandline
.venv ❯ python --version
```
とコマンドを入力し、**Python 3.6.5** と結果が出力されることで確認が出来ます。  

また、仮想環境から脱出する場合は、
```commandline
.venv ❯ exit
```
で抜けることができます。  
<br>

もし、別の手法でPython3.6.5を用意した場合
```commandline
pip install -r requirements.txt
```
とすることで必要なモジュールをインストールすることも可能です。


## ローカルwebサーバー立ち上げ手順

### 初期設定
```commandline
.venv ❯ python manage.py makemigrations
```  
~~マイグレーションファイル作成~~    
もしも次に行うマイグレートに失敗した場合に上記を実行してみてください。


```commandline
.venv ❯ python manage.py migrate
```  
マイグレート実行  

```commandline
.venv ❯ python manage.py createsuperuser
```  
スーパーユーザー作成  
（スーパーユーザー作成の時だけメールアドレスを求められる）

### ローカルWebサーバー立ち上げ
```commandline
.venv ❯ python manage.py runserver
```
ローカルWebサーバーを起動


## テスト実行方法
~/FakeSNS の階層で、  

```commandline
.venv ❯ python manage.py test
```
全てのアプリを一括でテストする場合  

```commandline
.venv ❯ python manage.py test app
.venv ❯ python manage.py test acounts
```
各アプリのテストを実行する場合  
  
とすることでテストを実行可能


## WebAPI エンドポイントまとめ
CURLコマンド以外にもブラウザでGET,POST等をリクエストする機能あり。ブラウザからURLにアクセスするのみ。（こちらのが手間がなく簡単）  
また、ログイン、ログアウト、サインアップ以外の全てのAPIには利用するのにログイン(トークン)が必要です。  
トークンの付与は、
`curl -H "Authorization: Token <TOKEN>"  http://localhost:8000/api/article/`  
の<TOKEN>に値を代入することで可能  
　　

`http://localhost:8000/`  
URL  

`api/rest-auth/login/`  
POST:ログイン(成功するとトークン発行)  
リクエスト:{"username": "", "password": ""}  
認証に成功すると、トークンがレスポンスされます。  

`api/rest-auth/logout/`  
POST:ログアウト  

`api/rest-auth/registration/`  
POST:サインアップ(成功するとトークン発行)  
リクエスト:{"username": "", "password1": "", "password2": ""}  

`api/article/`  
GET:投稿一覧(ブラックリストに追加されたものは表示しない), POST:新規投稿  
リクエスト:{"text": "", "author": <user_id>}  

`api/article/<article_id>/`  
GET:各投稿の個別取得, PUT:編集, DELETE:削除  
リクエスト:{"id": "<article_id>", "text": "", "author": <user_id>}  

`<user_id>/article/`  
GET:各ユーザーごとの投稿一覧  

`api/profile/`  
GET:ユーザー情報一覧, POST:新規ユーザー情報登録（既に登録している場合は不可）  
リクエスト:{"introduction": "", "sex": <1:女性, 2:男性>}  

`api/profile/<user_id>/`  
GET:各ユーザー情報を個別取得, PUT:ユーザー情報の編集（自身の情報のみ編集可）  
リクエスト:{"introduction": "", "sex": <1:女性, 2:男性>}  

`api/blacklist/`  
GET:自身の追加したブラックリスト一覧, POST:ブラックリストへの追加と削除  
リクエスト:{"add_user_id": <追加したいuser_id>, "del_user_id": <追加したいuser_id>}  

`api/like/`  
GET:自身が追加したいいね一覧  

`api/like/add/`  
GET:投稿一覧, POST:いいね追加  

`api/like/<like_id>/`  
GET:いいねを個別取得, DELETE:いいねから削除  

`api/users/`  
GET:ユーザー一覧
