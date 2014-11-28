# -*- coding:utf8 -*- 
from classification import *

def User_add(Openid,Name,Addr,Tel,cursor):
	#添加用户,成功返回用户信息，失败返回1
    sql="insert into User values('"+str(Openid)+"','"+str(Name)+"',0,'"+ str(Addr)+"','"+ str(Tel)+"')"
    cursor.execute(sql)
    return 0
def User_alter(User_id,operator,Parameter,g):
	# 修改用户,成功返回用户信息，失败返回1
	# 	0：修改地址
	# 	1：修改收货人
	# 	2：修改电话
	cursor = g.db.cursor()
	
	if(operator=="0"):
		sql="update User set Addr='"+Parameter+"' where User_id='"+User_id+"'"
	elif (operator=="1"):
		sql="update User set User_name='"+Parameter+"' where User_id='"+User_id+"'"
	elif (operator=="2"):
		sql="update User set Tel='"+Parameter+"' where User_id='"+User_id+"'"
	else:
		return 1
	cursor.execute(sql)
	g.db.commit()
	return 0
def User_info(User_id,cursor):
	#查询用户信息,成功返回用户信息，用户不存在返回1
	sql="select User_name,count,Addr,Tel from User where User_id='"+User_id+"'"
	cursor.execute(sql)
	info = cursor.fetchone()
	if(type(info)==type(None)):
		return 1
	else:
		return '用户名：' + info[0].encode('utf8') + '\n用户购物次数：' + str(info[1]) + '\n用户地址：' + info[2].encode('utf8') + '\n用户电话：' + info[3].encode('utf8') + '\n'
def goods_search(searchstr,cursor):
	#通过mysql like匹配搜索searchstr，并返回一个包含所有结果的Goods类列表
	sql="select * from Goods where Name like '%"+searchstr+"%' or Description like '%"+searchstr+"%'"
	cursor.execute(sql)
	result = cursor.fetchall()
	ret = '没有搜索到该商品哦>_<'
	for now in result:
		tmp = '货物id: ' + str(now[0])+' 商品名: ' + str(now[1]) + ' 类别id:' + str(now[2]) + ' 价格:' + str(now[3]) + ' 库存:' + str(now[4]) + ' 产地:' + now[5].encode('utf8') + ' 描述:' + now[7].encode('utf8') + '\n'
		return tmp
		ret += tmp
	return ret
def cart_creat(User_id,g):
	#创建新的购物车(不存在时),返回Cart_id
	cursor = g.db.cursor()
	try:
		sql="insert into Cart values(uuid(),'"+User_id+"',10,now())"
		cursor.execute(sql)
		# return 'in'
		g.db.commit()
	except:
		sql="select Cart_id from Cart where User_id='"+User_id+"'"
		cursor.execute(sql)
		Cart_id = cursor.fetchone()[0]
		return Cart_id
	sql="select Cart_id from Cart where User_id='"+User_id+"'"
	cursor.execute(sql)
	Cart_id = cursor.fetchone()[0]
	return Cart_id
def cart_add(Goods_id,Count,User_id,g):
	#添加新的商品到购物车，成功返回0，失败返回1
	cursor = g.db.cursor()
	sql = "select Price from Goods where Goods_id= " + Goods_id
	cursor.execute(sql)
	money = cursor.fetchone()[0]

	Cart_id=cart_creat(User_id,g)
	sql="select Count from CartItem where Cart_id='"+Cart_id+"' and Goods_id='"+Goods_id+"'"
	cursor.execute(sql)
	fet=cursor.fetchone()
	if type(fet) == type(None):
		sql="select Price from Goods where Goods_id="+Goods_id
		cursor.execute(sql)
		Price=cursor.fetchone()
		if type(Price) != type(None):
			sql="insert into CartItem values(uuid(),'"+Cart_id+"',"+ str(Count)+","+ str(Goods_id) +","+ str(float(Price[0])*float(Count))+")"
			cursor.execute(sql)
	else:
		sql="update CartItem set Count="+str(int(fet[0])+Count)+" where Cart_id='"+Cart_id+"' and Goods_id="+ str(Goods_id)
		cursor.execute(sql)
		cnt = int(fet[0]) + Count
		sql = "update CartItem set Money=" + str(cnt*float(money)) + " where Cart_id='"+Cart_id+"' and Goods_id="+ str(Goods_id)
	g.db.commit()
	return 0
def cart_get(User_id,cursor):
	#获取购物车内商品，成功返回购物车，失败返回1
	sql="select Cart_id from Cart where User_id='"+User_id+"'"
	cursor.execute(sql)
	Cart_id=cursor.fetchone()
	if type(Cart_id) == type(None):
		return 1
	sql="select Name,Count,Money from CartItem natural join Goods where Cart_id='"+Cart_id[0]+"'"
	cursor.execute(sql)
	result=cursor.fetchall()
	ret = ''
	for x in result:
		ret += str(x[0]) + ' ' + str(x[1]) + ' ' + '价格：' + str(x[2]) + '\n'
	return ret
def cart_del(Goods_id,Count,User_id,g):
	#修改购物车内商品数量，失败返回1
	cursor = g.db.cursor()
	sql = "select Price from Goods where Goods_id= " + Goods_id
	cursor.execute(sql)
	money = cursor.fetchone()[0]

	sql="select Cart_id from Cart where User_id='"+User_id+"'"
	cursor.execute(sql)
	Cart_id=cursor.fetchone()

	if type(Cart_id) == type(None):
		return 1
	sql="select Count from CartItem where Cart_id='"+Cart_id[0]+"' and Goods_id="+Goods_id
	cursor.execute(sql)
	count=cursor.fetchone()
	if type(count) != type(None):
		sql="update CartItem set Count= "+str(int(count[0]) - int(Count))+" where Cart_id='"+Cart_id[0]+"' and Goods_id="+str(Goods_id)
		cursor.execute(sql)
		cnt = int(count[0]) - int(Count)
		sql = "update CartItem set Money=" + str(cnt*float(money)) + " where Cart_id='"+Cart_id[0]+"' and Goods_id="+ Goods_id
		cursor.execute(sql)
		g.db.commit()
	return 0

def cart_buy(User_id,Note,g):
	#将购物车内商品添加到订单，并下单,记录此次交易详情。成功返回0,失败返回1
	cursor = g.db.cursor()		
	sql = "select Cart_id from Cart where User_id='" + User_id + "'"
	cursor.execute(sql)
	cart_id = cursor.fetchone()[0]
	sql = "select sum(Money) from CartItem where Cart_id ='" + cart_id + "'"
	cursor.execute(sql)
	Money=cursor.fetchone()[0]
	sql="insert into Orderinfo values(uuid(),'"+User_id+"',now(),"+ str(Money) +",'"+ Note+"',"+"false)"
	cursor.execute(sql)

	try:
		sql="insert into CartRecord select * from Cart where User_id='"+User_id+"'"
		# return sql
		cursor.execute(sql)
	except:
		return 'error'
	Cart_id=cart_creat(User_id,g)
	sql="select Count,Name,Money,Place,Image,Description from Goods natural join(select Count,Goods_id,Money from CartItem where Cart_id='"+Cart_id+"') as A "
	cursor.execute(sql)

	result=cursor.fetchall()
	for now in result:
		return now[3]
		sql="insert into CartItemRecord values(uuid(),'"+Cart_id+"',"+str(now[0])+",'"+str(now[1])+"',"+str(now[2])+",'"+str(now[3])# +"','"+now[4].encode('utf8') +"','"+now[5].encode('utf8') +"')"
		return sql
		cursor.execute(sql)

	sql = "delete from CartItem where Cart_id = '" + cart_id + "'"
	cursor.execute(sql)
	sql = "delete from Cart where User_id = '" + User_id + "'"
	cursor.execute(sql)
	g.db.commit()
	return 0
