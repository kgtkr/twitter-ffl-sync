import os
import tweepy

# 環境変数取得
ck = os.environ["CK"]
cs = os.environ["CS"]
tk = os.environ["TK"]
ts = os.environ["TS"]
list_name = os.environ["LIST_NAME"]

# 認証
auth = tweepy.OAuthHandler(ck, cs)
auth.set_access_token(tk, ts)
api = tweepy.API(auth)

# リストを検索
list_id = None
for x in api.lists_all():
    if x.name == list_name:
        list_id = x.id

# 存在しない場合は作る
if list_id == None:
    list_id = api.create_list(name=list_name, mode="private").id

# フォローユーザー一覧とリストユーザー一覧取得
friends = set(
    list(tweepy.Cursor(api.friends_ids, user_id=api.me().id).items()))
members = set([x.id for x in tweepy.Cursor(
    api.list_members, list_id=list_id).items()])

# リストに追加
for id in friends-members:
    api.add_list_member(list_id=list_id, user_id=id)

# リストから削除
for id in members-friends:
    api.remove_list_member(list_id=list_id, user_id=id)
