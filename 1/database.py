# -*- coding:utf8 -*- 

from MySQLdb import *
from classification import *
import sae.const

host = sae.const.MYSQL_HOST
user = sae.const.MYSQL_USER
password = sae.const.MYSQL_PASS
database=sae.const.MYSQL_DB

def User_add(Name,Addr,Tel):
	#添加用户,成功返回用户信息，失败返回1
	sql="insert into User values(uuid(),"+Name+",0,"+Addr+","+Tel+")"
	db = MySQLdb.connect(host,user,password,database,port=int(sae.const.MYSQL_PORT),charset='utf8')
	cursor = db.cursor()
	cursor.execute(sql)
	user_tmp=User()
	user_tmp.User_name=Name
	user_tmp.Addr=Addr
	user_tmp.Tel=Tel
	db.commit()
	db.close()
	return user_tmp

def User_alter(User_id,operator,Parameter):
	# 修改用户,成功返回用户信息，失败返回1
	# 	0：修改地址
	# 	1：修改收货人
	# 	2：修改电话
	return 0
	sql="select * from User where User_id='"+User_id+"'"
	db = MySQLdb.connect(host,user,password,database,port=int(sae.const.MYSQL_PORT),charset='utf8')
	return 0
	cursor = db.cursor()
	cursor.execute(sql)
	info=cursor.fetchone()
	if(type(info)==type(None)):
		return 1
	user_tmp=User()
	user_tmp.User_name=info[0]
	user_tmp.Addr=info[1]
	user_tmp.Tel=info[2]

	if(operator=="0"):
		sql="update User set Addr='"+Parameter+"' where User_id='"+User_id+"'"
		user_tmp.Addr=Parameter
	elif (operator=="1"):
		sql="update User set User_Name='"+Parameter+"' where User_id='"+User_id+"'"
		user_tmp.Name=Parameter
	elif (operator=="2"):
		sql="update User set Tel='"+Parameter+"' where User_id='"+User_id+"'"
		user_tmp.Tel=Parameter
	else:
		return 1

	cursor.execute(sql)
	db.commit()
	db.close()
	return user_tmp

def User_info(User_id):
	#查询用户信息,成功返回用户信息，失败返回1
	sql="select * from User where User_id='"+User_id+"'"
	db = MySQLdb.connect(host,user,password,database,port=int(sae.const.MYSQL_PORT),charset='utf8')
	cursor = db.cursor()
	cursor.execute(sql)
	info=cursor.fetchone()
	if(type(info)==type(None)):
		return 1
	else:
		user_tmp=User()
		user_tmp.User_name=info[1]
		user_tmp.count=info[2]
		user_tmp.Addr=info[3]
		user_tmp.Tel=info[4]
	db.close()
	return user_tmp

def goods_search(searchstr):
	#通过mysql like匹配搜索searchstr，并返回一个包含所有结果的Goods类列表
	sql="select * from Goods where Name like '%"+searchstr+"%' or Description like '%"+searchstr+"%'"
	db = MySQLdb.connect(host,user,password,database,port=int(sae.const.MYSQL_PORT),charset='utf8')
	cursor = db.cursor()
	cursor.execute(sql)
	result = cursor.fetchall()
	goods=[]
	for now in result:
		tmp=Goods()
		tmp.Goods_id=now[0]
		tmp.Name=now[1]
		tmp.Class_id=now[2]
		tmp.Price=now[3]
		tmp.Stock=now[4]
		tmp.Place=now[5]
		tmp.Image=now[6]
		tmp.Description=now[7]
		goods.append(tmp)
	db.close()
	return goods

def cart_creat(User_id):
	#创建新的购物车(不存在时),返回Cart_id
	try:
		sql="insert into Cart values(uuid(),'"+User_id+"',10,now())"
		db = MySQLdb.connect(host,user,password,database,port=int(sae.const.MYSQL_PORT),charset='utf8')
		cursor = db.cursor()
		cursor.execute(sql)
		db.commit()
	except IntegrityError,e:
		pass
	sql="select Cart_id from Cart where User_id='"+User_id+"'"
	db = MySQLdb.connect(host,user,password,database,port=int(sae.const.MYSQL_PORT),charset='utf8')
	cursor = db.cursor()
	cursor.execute(sql)
	Cart_id = cursor.fetchone()[0]
	db.commit()
	db.close()
	return Cart_id
	
def cart_add(Goods_id,Count,User_id):
	#添加新的商品到购物车，成功返回0，失败返回1
	Cart_id=cart_creat(User_id)
	sql="select Count from CartItem where Cart_id='"+Cart_id+"' and Goods_id='"+Goods_id+"'"
	db = MySQLdb.connect(host,user,password,database,port=int(sae.const.MYSQL_PORT),charset='utf8')
	cursor = db.cursor()
	cursor.execute(sql)
	count=cursor.fetchone()
	if(type(count)==type(None)):
		sql="select Price from Goods where Goods_id='"+Goods_id+"'"
		cursor.execute(sql)
		Price=cursor.fetchone()
		if(type(Price)!=type(None)):
			sql="insert into CartItem values(uuid(),'"+Cart_id+"','"+Count+"','"+Goods_id+"','"+str(int(Price[0])*int(Count))+"')"
			cursor.execute(sql)
	else:
		sql="update CartItem set Count='"+str(int(count[0])+int(Count))+"' where Cart_id='"+Cart_id+"' and Goods_id='"+Goods_id+"'"
		cursor.execute(sql)
	db.commit()
	db.close()
	return 0

def cart_get(User_id):
	#获取购物车内商品，成功返回购物车，失败返回1
	sql="select Cart_id from Cart where User_id='"+User_id+"'"
	db = MySQLdb.connect(host,user,password,database,port=int(sae.const.MYSQL_PORT),charset='utf8')
	cursor = db.cursor()
	cursor.execute(sql)
	Cart_id=cursor.fetchone()
	if(type(Cart_id)==type(None)):
		return 1
	sql="select Name,Count,Money from CartItem natural join Goods where Cart_id='"+Cart_id[0]+"'"
	cursor.execute(sql)
	result=cursor.fetchall()
	cartlist=[]
	for now in result:
		tmp=CartItem()
		tmp.Goods_name=now[0]
		tmp.Count=now[1]
		tmp.Money=now[2]
		cartlist.append(tmp)
	db.close()
	return cartlist

def cart_del(Goods_id,Count,User_id):
	#修改购物车内商品数量，成功返回其余商品，失败返回1
	sql="select Cart_id from Cart where User_id='"+User_id+"'"
	db = MySQLdb.connect(host,user,password,database,port=int(sae.const.MYSQL_PORT),charset='utf8')
	cursor = db.cursor()
	cursor.execute(sql)
	Cart_id=cursor.fetchone()
	if(type(Cart_id)==type(None)):
		return 1
	sql="select Count from CartItem where Cart_id='"+Cart_id[0]+"' and Goods_id='"+Goods_id+"'"
	cursor.execute(sql)
	count=cursor.fetchone()
	if(type(count)!=type(None)):
		sql="update CartItem set Count='"+str(int(count[0])-int(Count))+"'where Cart_id='"+Cart_id[0]+"'and Goods_id='"+Goods_id+"'"
		cursor.execute(sql)
		db.commit()
	db.close()
	return cart_get(User_id)

def cart_buy(User_id,Note):
	#将购物车内商品添加到订单，并下单,记录此次交易详情。成功返回0,失败返回1
	cartlist=cart_get(User_id)
	Money=0
	for now in cartlist:
		Money+=now.Money
	sql="insert into Orderinfo values(uuid(),'"+User_id+"',now(),'"+str(Money)+"','"+Note+"',"+"false)"
	db = MySQLdb.connect(host,user,password,database,port=int(sae.const.MYSQL_PORT),charset='utf8')
	cursor = db.cursor()
	cursor.execute(sql)

	sql="insert into CartRecord select * from Cart where User_id='"+User_id+"'"
	cursor.execute(sql)

	Cart_id=cart_creat(User_id)
	sql="select Count,Name,Money,Place,Image,Description from Goods natural join(select Count,Goods_id,Money from CartItem where Cart_id='"+Cart_id+"') as A "
	print sql
	cursor.execute(sql)
	result=cursor.fetchall()
	for now in result:
		sql="insert into CartItemRecord values(uuid(),'"+Cart_id+"',"+str(now[0])+",'"+now[1]+"',"+str(now[2])+",'"+now[3]+"','"+now[4]+"','"+now[5]+"')"
		print sql
		cursor.execute(sql)
	db.commit()
	db.close()
	return 0

cart_buy("1bcbbf3d-6e15-11e4-8d74-f46d0489f16d","zhang")