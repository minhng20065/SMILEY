import mysql.connector
class Inventory:
    data = ""
    def connect(self, query, values, write, col):
        """This function connects to the mySQL database, executing queries and returning True
        if the queries went through, and False if they did not. It can read and write to the
        database, storing any data in a data tuple."""
        try:
            connection = mysql.connector.connect(host='localhost',
                                              database = 'inventory',
                                              user = 'root',
                                              password = 'root')
            cursor = connection.cursor(buffered=True)
            if write:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
                if col:
                    self.data = cursor.fetchall()
                else:
                    self.data = cursor.fetchone()
            connection.commit()
            return True
        except mysql.connector.Error as error:
            print(f"Database error: {error}")
            cursor.close()
            connection.close()
            return False
    def add_item(self, item):
        mysql_insert_row_query = "INSERT INTO items (Items) VALUES (%s)"
        mysql_insert_row_values = (item,)
        self.connect(mysql_insert_row_query, mysql_insert_row_values, True, False)
    def find_item(self, name, id, items):
        i = 0
        mysql_insert_row_query = (f"SELECT * FROM items WHERE id = {id}")
        self.connect(mysql_insert_row_query, 0, False, False)
        if self.data is None:
            return self.data
        else:
            mysql_insert_row_query = "INSERT INTO inventory (Inventory, id, char_id) VALUES (%s, %s, %s)"
            mysql_insert_row_values = (self.data[0], self.data[1], name)
            for i in range(items):
                print("sex")
                self.connect(mysql_insert_row_query, mysql_insert_row_values, True, False)
                i = i + 1
            return self.data
