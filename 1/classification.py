# -*- coding:utf8 -*- 

class Goods(object):
	#商品属性
	def __init__(self,Goods_id=0,Name=0,Price=0,Stock=0,Description=0,Image=0,Place=0,Class_id=0):
		self.Goods_id=Goods_id
		self.Name=Name
		self.Price=Price
		self.Stock=Stock
		self.Description=Description
		self.Image=Image
		self.Place=Place
		self.Class_id=Class_id

class CartItem(object):
	#购物车详情
	def __init__(self,Cartitem_id=0,Count=0,Cart_id=0,Class_id=0,Money=0):
		self.Cartitem_id=Cartitem_id
		self.Count=Count
		self.Cart_id=Cart_id
		self.Class_id=Class_id
		self.Money=Money

class User(object):
	#用户类型
	def __init__(self,User_id=1,User_name=0,count=0,Addr=0,Tel=0):
		self.User_name=User_name
		self.User_id=User_id
		self.count=count
		self.Addr=Addr
		self.Tel=Tel