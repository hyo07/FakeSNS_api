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
.venvファイルのある階層で仮想環境を起動。  

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


## ローカルwebサーバー立ち上げ手順

### 初期設定
```commandline
python manage.py makemigrations
```  
~~マイグレーションファイル作成~~    
もしも次に行うマイグレートに失敗した場合に上記を実行してみてください。


```commandline
python manage.py migrate
```  
マイグレート実行  

```commandline
python manage.py createsuperuser
```  
スーパーユーザー作成  
（スーパーユーザー作成の時だけメールアドレスを求められる）

### ローカルWebサーバー立ち上げ
```commandline
python manage.py runserver
```
ローカルサーバーを起動


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