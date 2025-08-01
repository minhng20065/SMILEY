'''This module contains all the functtionality to connect and
modify tables in the Inventory database, managing items and 
inventories.'''
import mysql.connector
class Inventory:
    '''This class handles connecting, reading, and writing from the Inventory database.'''
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
        '''This method adds items to the database, taking in the item name.'''
        mysql_insert_row_query = "INSERT INTO items (Items) VALUES (%s)"
        mysql_insert_row_values = (item,)
        self.connect(mysql_insert_row_query, mysql_insert_row_values, True, False)

    def add_weapon(self, item, item_id, atk, weapon):
        '''This method adds an equippable item to the database, taking in the item name, the item
        id, whether or not it is a weapon or armor, and its modifier value.'''
        if weapon:
            mysql_insert_row_query = "INSERT INTO weapons (Weapon, id, ATK) VALUES (%s, %s, %s)"
            mysql_insert_row_values = (item, item_id, atk)
            self.connect(mysql_insert_row_query, mysql_insert_row_values, True, False)
        else:
            mysql_insert_row_query = "INSERT INTO armor (Armor, id, DEF) VALUES (%s, %s, %s)"
            mysql_insert_row_values = (item, item_id, atk)
            self.connect(mysql_insert_row_query, mysql_insert_row_values, True, False)

    def add_weapon_to_sheet(self, name, item_id, char_id, atk):
        '''This method adds a weapon as an equippable, taking in the name of the weapon,
        the item id, the character id of the character who equips it, and the atk value.'''
        mysql_insert_row_query = ("INSERT INTO equippable_items (Type, Name, id, char_id, " +
        "Modifier, Damage, Equipped) VALUES (%s, %s, %s, %s, %s, %s, %s)")
        mysql_insert_row_values = ('Weapon', name, int(item_id), int(char_id), int(atk), 0, 0)
        self.connect(mysql_insert_row_query, mysql_insert_row_values, True, False)

    def add_armor_to_sheet(self, name, item_id, char_id, defe):
        '''This method adds a armor as an equippable, taking in the name of the armor,
        the item id, the character id of the character who equips it, and the def value.'''
        mysql_insert_row_query = ("INSERT INTO equippable_items (Type, Name, id, char_id, " +
            "Modifier, Damage, Equipped) VALUES (%s, %s, %s, %s, %s, %s, %s)")
        mysql_insert_row_values = ('Armor', name, int(item_id), int(char_id), int(defe), 0, 0)
        self.connect(mysql_insert_row_query, mysql_insert_row_values, True, False)

    def equip_weapon(self, item_id, char, weapons):
        '''This method allows a character to equip a weapon, by taking it's id, the character
        id of the character equipping, and whether or not it is a weapons.'''
        if weapons:
            # unequips the previous item before equipping the current item.
            mysql_insert_row_query = ("UPDATE equippable_items SET Equipped = %s WHERE id = %s " +
            "AND char_id = %s AND Equipped = %s AND Type = %s")
            mysql_insert_row_values = (0, item_id, char, 1, 'Weapons')
            self.connect(mysql_insert_row_query, mysql_insert_row_values, True, False)
            mysql_insert_row_query = "UPDATE equippable_items SET Equipped = %s WHERE id = %s"
            mysql_insert_row_values = (1, item_id)
            self.connect(mysql_insert_row_query, mysql_insert_row_values, True, False)
        else:
            mysql_insert_row_query = ("UPDATE equippable_items SET Equipped = %s WHERE id = %s " +
            "AND char_id = %s AND Equipped = %s AND Type = %s")
            mysql_insert_row_values = (0, item_id, char, 1, 'Armor')
            self.connect(mysql_insert_row_query, mysql_insert_row_values, True, False)
            mysql_insert_row_query = ("UPDATE equippable_items SET Equipped = %s " +
            "WHERE id = %s AND char_id = %s")
            mysql_insert_row_values = (1, item_id, char)
            self.connect(mysql_insert_row_query, mysql_insert_row_values, True, False)

    def find_item(self, name, item_id, items):
        '''This method finds an item in the database, and if it does, add
        it to a character's inventory, taking in the character's id, the item id,
        and the number of items inserted.'''
        i = 0
        mysql_insert_row_query = f"SELECT * FROM items WHERE id = {item_id}"
        self.connect(mysql_insert_row_query, 0, False, False)
        if self.data is None:
            return self.data
        mysql_insert_row_query = ("INSERT INTO inventory (Inventory, id, char_id) " +
        "VALUES (%s, %s, %s)")
        mysql_insert_row_values = (self.data[0], self.data[1], name)
        for i in range(items):
            self.connect(mysql_insert_row_query, mysql_insert_row_values, True, False)
            i = i + 1
        return self.data

    def find_atk(self, item_id, weapon):
        '''This function reads the modifier values for equippable items, given
        the item id and whether or not the item is weapon or armor.'''
        if weapon:
            mysql_insert_row_query = f"SELECT ATK FROM weapons WHERE id = {item_id}"
            self.connect(mysql_insert_row_query, 0, False, False)
            return self.data
        mysql_insert_row_query = f"SELECT DEF FROM armor WHERE id = {item_id}"
        self.connect(mysql_insert_row_query, 0, False, False)
        return self.data
    def find_inv_count(self, char_id):
        '''This method counts the amount of items in a character's inventory, given
        the character's id.'''
        mysql_insert_row_query = f"SELECT COUNT(*) FROM inventory WHERE char_id = {char_id}"
        self.connect(mysql_insert_row_query, 0, False, False)
        return self.data
    def show_inv(self, char_id):
        '''This function returns the entire inventory for one character, given that character's
        id.'''
        mysql_insert_row_query = f"SELECT Inventory FROM inventory WHERE char_id = {char_id}"
        self.connect(mysql_insert_row_query, 0, False, True)
        return self.data

    def find_item_id(self, name):
        '''This method finds the id of an item, given the item's name.'''
        mysql_insert_row_query = f"SELECT id FROM items WHERE Items = '{name}'"
        self.connect(mysql_insert_row_query, 0, False, False)
        return self.data

    def find_item_in_char(self, name, char_id):
        '''This method finds an item in the character's inventory, given the item's name
        and the character's id.'''
        mysql_insert_row_query = (f"SELECT Inventory FROM inventory WHERE Inventory = '{name}' " +
                                  f"AND char_id = '{int(char_id)}'")
        self.connect(mysql_insert_row_query, 0, False, False)
        return self.data

    def remove_item(self, name, char_id):
        '''This function removes an item from a character's inventory, given the item's name
        and the character's id.'''
        mysql_insert_row_query = (f"DELETE FROM inventory WHERE Inventory = '{name}' AND " +
                                  f"char_id = {int(char_id)} ORDER BY instance_id DESC LIMIT 1;")
        self.connect(mysql_insert_row_query, 0, True, False)

    def add_text(self, use, drop, text, item_id):
        '''This method adds flavor text for non-equippable items, taking in whether
        the text is for using or dropping, the text, and the item id.'''
        if use:
            mysql_insert_row_query = "INSERT INTO use_flavor_text VALUES (%s, %s)"
            mysql_insert_row_values = (text, item_id)
            self.connect(mysql_insert_row_query, mysql_insert_row_values, True, False)
        elif drop:
            mysql_insert_row_query = "INSERT INTO drop_flavor_text VALUES (%s, %s)"
            mysql_insert_row_values = (text, item_id)
            self.connect(mysql_insert_row_query, mysql_insert_row_values, True, False)
        else:
            mysql_insert_row_query = "INSERT INTO equip_flavor_text VALUES (%s, %s)"
            mysql_insert_row_values = (text, item_id)
            self.connect(mysql_insert_row_query, mysql_insert_row_values, True, False)

    def add_equippable_text(self, text, item_id):
        '''This method adds flavor text for equpping items, taking in the text
        and the item id.'''
        mysql_insert_row_query = "INSERT INTO equippable_flavor_text VALUES (%s, %s)"
        mysql_insert_row_values = (text, item_id)
        self.connect(mysql_insert_row_query, mysql_insert_row_values, True, False)

    def print_text(self, use, drop, equip, item_id):
        '''This method prints out the flavor text, taking in whether
        if the text is use text, drop text, or equipping text, and the
        item id of the text.'''
        if use:
            mysql_insert_row_query = ("SELECT text FROM use_flavor_text WHERE " +
            f"item_id = {int(item_id)}")
            self.connect(mysql_insert_row_query, 0, False, False)
            return self.data
        if drop:
            mysql_insert_row_query = ("SELECT text FROM drop_flavor_text WHERE " +
            f"item_id = {int(item_id)}")
            self.connect(mysql_insert_row_query, 0, False, False)
            return self.data
        if equip:
            mysql_insert_row_query = ("SELECT text FROM equip_flavor_text WHERE " +
            f"item_id = {int(item_id)}")
            self.connect(mysql_insert_row_query, 0, False, False)
            return self.data
        mysql_insert_row_query = ("SELECT text FROM equippable_flavor_text WHERE " +
        f"item_id = {int(item_id)}")
        self.connect(mysql_insert_row_query, 0, False, False)
        return self.data

    def remove_all_item(self, item_id):
        '''This method removes items from the database, removing them
        from the inventory and all its associated flavor text. It 
        just takes the item's id.'''
        mysql_insert_row_query = "DELETE FROM items WHERE id = %s"
        mysql_insert_row_values = (item_id,)
        self.connect(mysql_insert_row_query, mysql_insert_row_values, True, False)
        mysql_insert_row_query = "DELETE FROM drop_flavor_text WHERE item_id = %s"
        mysql_insert_row_values = (item_id,)
        self.connect(mysql_insert_row_query, mysql_insert_row_values, True, False)
        mysql_insert_row_query = "DELETE FROM equip_flavor_text WHERE item_id = %s"
        mysql_insert_row_values = (item_id,)
        self.connect(mysql_insert_row_query, mysql_insert_row_values, True, False)
        mysql_insert_row_query = "DELETE FROM inventory WHERE id = %s"
        mysql_insert_row_values = (item_id,)
        self.connect(mysql_insert_row_query, mysql_insert_row_values, True, False)
        mysql_insert_row_query = "DELETE FROM use_flavor_text WHERE item_id = %s"
        mysql_insert_row_values = (item_id,)
        self.connect(mysql_insert_row_query, mysql_insert_row_values, True, False)
