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
                self.connect(mysql_insert_row_query, mysql_insert_row_values, True, False)
                i = i + 1
            return self.data
    def find_inv_count(self, char_id):
        mysql_insert_row_query = (f"SELECT COUNT(*) FROM inventory WHERE char_id = {char_id}")
        self.connect(mysql_insert_row_query, 0, False, False)
        return self.data
    def show_inv(self, char_id):
        mysql_insert_row_query = (f"SELECT Inventory FROM inventory WHERE char_id = {char_id}")
        self.connect(mysql_insert_row_query, 0, False, True)
        return self.data
    def find_item_id(self, name):
        mysql_insert_row_query = (f"SELECT id FROM items WHERE Items = '{name}'")
        self.connect(mysql_insert_row_query, 0, False, False)
        return self.data
    def find_item_in_char(self, name, char_id):
        mysql_insert_row_query = (f"SELECT Inventory FROM inventory WHERE Inventory = '{name}' AND char_id = '{int(char_id)}'")
        self.connect(mysql_insert_row_query, 0, False, False)
        return self.data
    def remove_item(self, name, char_id):
        mysql_insert_row_query = (f"DELETE FROM inventory WHERE Inventory = '{name}' AND char_id = {int(char_id)} ORDER BY instance_id DESC LIMIT 1;")
        self.connect(mysql_insert_row_query, 0, True, False)
    def add_text(self, use, drop, text, id):
        if (use):
            mysql_insert_row_query = ("INSERT INTO use_flavor_text VALUES (%s, %s)")
            mysql_insert_row_values = (text, id)
            self.connect(mysql_insert_row_query, mysql_insert_row_values, True, False)
        elif(drop):
            mysql_insert_row_query = ("INSERT INTO drop_flavor_text VALUES (%s, %s)")
            mysql_insert_row_values = (text, id)
            self.connect(mysql_insert_row_query, mysql_insert_row_values, True, False)
    def print_text(self, use, drop, id):
        if (use):
            mysql_insert_row_query = (f"SELECT text FROM use_flavor_text WHERE item_id = {int(id)}")
            self.connect(mysql_insert_row_query, 0, False, False)
            return self.data
        elif (drop):
            mysql_insert_row_query = (f"SELECT text FROM drop_flavor_text WHERE item_id = {int(id)}")
            self.connect(mysql_insert_row_query, 0, False, False)
            return self.data