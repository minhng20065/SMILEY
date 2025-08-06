import mysql.connector
class NPC:
    '''This class handles connecting, reading, and writing from the Inventory database.'''
    data = ""
    def connect(self, query, values, write, col):
        """This function connects to the mySQL database, executing queries and returning True
        if the queries went through, and False if they did not. It can read and write to the
        database, storing any data in a data tuple."""
        try:
            connection = mysql.connector.connect(host='localhost',
                                              database = 'npcs',
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
    def register_npcs(self, name, enemy):
        if (enemy):
            mysql_insert_row_query = "INSERT INTO enemies (Name) VALUES (%s)"
            mysql_insert_row_values = (name,)
            self.connect(mysql_insert_row_query, mysql_insert_row_values, True, False)
            mysql_insert_row_query = ("INSERT INTO enemy_stats (HP, DAM, PRO, MOV) VALUES (DEFAULT, DEFAULT, DEFAULT, DEFAULT)")
            self.connect(mysql_insert_row_query, 0, True, False)
        else:
            mysql_insert_row_query = "INSERT INTO npc (Name) VALUES (%s)"
            mysql_insert_row_values = (name,)
    def get_npc_id(self, name, enemy):
        if (enemy):
            mysql_insert_row_query = f"SELECT npc_id FROM enemies WHERE Name = '{name}'"
            self.connect(mysql_insert_row_query, 0, False, False)
            return self.data
        mysql_insert_row_query = f"SELECT npc_id FROM npc WHERE Name = '{name}'"
        self.connect(mysql_insert_row_query, 0, False, False)
        return self.data
    def add_stats(self, args, npc_id):
        mysql_insert_row_query = ("UPDATE enemy_stats SET HP = %s, DAM = %s, PRO = %s, MOV = %s WHERE npc_id = %s")
        mysql_insert_row_values = (int(args[0]), int(args[1]), int(args[2]), int(args[3]), int(npc_id))
        self.connect(mysql_insert_row_query, mysql_insert_row_values, True, False)

    def add_dialogue(self, dialogue, npc_id):
        mysql_insert_row_query =  "INSERT INTO dialogue (dialogue, npc_id) VALUES (%s, %s)"
        mysql_insert_row_values = (dialogue, npc_id)
        self.connect(mysql_insert_row_query, mysql_insert_row_values, True, False)
    def talk_to(self, npc_id):
        mysql_insert_row_query = f"SELECT dialogue FROM dialogue WHERE npc_id = '{npc_id}'"
        self.connect(mysql_insert_row_query, 0, False, False)
        return self.data
    def remove_npc(self, npc_id, enemy):
        if (enemy):
            mysql_insert_row_query = "DELETE FROM enemies WHERE npc_id = %s"
            mysql_insert_row_values = (npc_id,)
            self.connect(mysql_insert_row_query, mysql_insert_row_values, True, False)
            mysql_insert_row_query = "DELETE FROM enemy_stats WHERE npc_id = %s"
            mysql_insert_row_values = (npc_id,)
            self.connect(mysql_insert_row_query, mysql_insert_row_values, True, False)
        else:
            mysql_insert_row_query = "DELETE FROM npc WHERE npc_id = %s"
            mysql_insert_row_values = (npc_id,)
            self.connect(mysql_insert_row_query, mysql_insert_row_values, True, False)
            mysql_insert_row_query = "DELETE FROM dialogue WHERE npc_id = %s"
            mysql_insert_row_values = (npc_id,)
            self.connect(mysql_insert_row_query, mysql_insert_row_values, True, False)