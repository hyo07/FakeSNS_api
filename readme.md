# 簡易 多分投稿SNS webアプリ

## 環境
- Python 3.6.5
- Mac
- Django 2.1.7

## 初期設定
### マイグレーション
`python manage.py makemigrations`  
マイグレーションファイル作成  
`python manage.py migrate`  
マイグレート実行
`python manage.py createsuperuser`  
スーパーユーザー作成  
（スーパーユーザー作成の時だけメールアドレスを求められる）

## 実装した機能
- アカウント作成
- ログイン、ログアウト
- 記事一覧、投稿、編集、削除
- ユーザーページ
- プロフィール登録、編集
- ブラックリスト登録、削除
- いいね追加、削除
- パスワード変更