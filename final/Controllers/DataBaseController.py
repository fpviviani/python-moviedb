# import MySQLdb

# class DataBaseController(): 
#     def __init__(self, mainController, dataJson):  
#         self.mainController = mainController
#         self.dataJson = dataJson
#         self.initialCommit()

#     def initialCommit(self):
#         connection = MySQLdb.connect(host='localhost',user='root',passwd='')
#         connection.select_db('projeto_final')
        
#         cursor = connection.cursor()
        
#         cursor.execute("INSERT INTO sua_tabela (nome) VALUES(%s)", (nomep))
#         connection.commit()