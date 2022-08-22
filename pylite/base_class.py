# -*- coding: utf-8 -*-
"""
	pylite
	~~~~~~~~~
	:copyright: (c) 2014 by Dariush Abbasi.
	:license: MIT, see LICENSE for more details.
"""

def __init__():
	__version__ = "0.1.0"



from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from _typeshed import StrOrBytesPath
import sqlite3
from sqlite3.dbapi2 import Cursor

class Pylite:
	'''
	Intract with sqlite3 in python as simple as it can be.
	'''

	def __init__(self,db_name:'StrOrBytesPath',default_table:str = ..., **columns):
		'''
		first argument is name of database that store in same name file on disk
		'''
		self.db_name = db_name
		self.db = sqlite3.connect(db_name)
		self.default_table = default_table

		if self.default_table is not Ellipsis and columns:
			self.add_table(default_table, **columns)

	def default(self, table_name:str) -> str:
		if table_name is Ellipsis or table_name is None:
			if self.default_table is not Ellipsis and self.default_table is not None:
				return self.default_table
			else:
				raise ValueError('`table_name` must be set if `default_table` is not set')
		else:
			return table_name

	def add_table(self,table_name:str,**columns:str) -> None:
		'''
		Add table
		- first argument is table name.
		- other arguments have to be labled names equal to data type.for example title="text" or id="int"
		'''

		cols = ",".join(f"{col_name} {col_type}" for col_name,col_type in columns.items())

		self.db.execute(f"CREATE TABLE IF NOT EXISTS {table_name}({cols})")


	def insert(self, *data:int|str|float|tuple[int|str|float], table_name:str=...) -> None:
		'''
		insert data into table or default table
		'''

		table_name = self.default(table_name)

		match data:
			case [int()|str()|float()]:
				values = '('+', '.join(f"'{value}'" if isinstance(value, str) else str(value) for value in data)+')'
			case [tuple()]:
				values = ', '.join('('+ ', '.join(f'\'{value}\'' if isinstance(value, str) else str(value) for value in values) +')' for values in data)
			case [int()|str()|float()|tuple()]:
				raise ValueError('received mix of tuples and values')
			case _:
				raise TypeError('received invalid types: '+', '.join(type(item).__name__ for item in data))

		self.db.execute(f"INSERT INTO {table_name} values{values}")
		self.db.commit()


	def add(self,insertion_type:str,table_name:str=..., *data:str|int|float|tuple[int|str|float],**columns:str):

		'''
		add table to database, or data to table
		- insertion type : 'table' or 'data'
		'''

		table_name = self.default(table_name)

		match insertion_type:
			case 'table':
				cols = ",".join(f"{col_name} {col_type}" for col_name,col_type in columns.items())

				self.db.execute(f"CREATE TABLE IF NOT EXISTS {table_name}({cols})")

			case 'data':
				self.insert()

	def remove(self,table_name:str =...,where:str ='0'):
		'''
		remove items from table
		- second argument defaults to 0 for safety
		'''

		table_name = self.default(table_name)

		self.db.execute(f"DELETE FROM {table_name} WHERE {where}")
		self.db.commit()

	def update(self,table_name:str =...,where:str ='0',**columns):
		'''
		update items values
		- third argument is dictionaury of table column names and values
		'''
		table_name = self.default(table_name)

		cols = ",".join(f"{col_name} {col_type}" for col_name,col_type in columns.items())

		self.db.execute(f"UPDATE {table_name} SET {cols} where {where}")


	def get_items(self,table_name:str =...,where:int|int=1):
		'''
		get items from db
		param table name
		second argument is condition
		'''
		table_name = self.default(table_name)

		if(table_name!=1) :
			return self.db.execute(f"SELECT * FROM {table_name} WHERE {where}")
		else :
			return Cursor()

	def get_tables(self):
		'''
		return list of tables
		'''
		self.tables = self.db.execute("SELECT name FROM sqlite_master")
		return list(self.tables)

	def query(self,query_string:str):
		'''
		execute sqlite queries
		'''
		self.db.execute(query_string);
		self.db.commit()

	def close_connection(self):
		'''
		close database connection
		'''
		self.db.close()
	
	def __del__(self):
		self.close_connection()
