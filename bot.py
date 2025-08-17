# bot.py
'''
This module sets up the discord bot and contains all the commands 
and their logic needed to function.
'''
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
import sheet
from sheet import Sheet
from errors import Error
from select1 import Select
from inventory import Inventory
from npcs import NPC
from grid import Grid
import config



load_dotenv()
# enables all intents for the bot
intents = discord.Intents.all()
intents.message_content = True
# specifies that commands will begin with !, and allows all intents
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    '''This method executes as soon as the bot is activated, showing
    the bot's name and ID.'''
    print('logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-----')

# initializes the objects for each file
sheet = Sheet()
error = Error()
select = Select()
inventory = Inventory()
npc = NPC()
grid = Grid(7, 10)

@bot.command()
async def register(ctx, *args):
    '''This method defines a command to register a new character to the database. It
    takes the character's characteristics provided in a user submission, and passes
    them to an SQL function in the sheet.py file.'''

    # if there are less than 7 arguments, the command is invalid.
    if len(args) != 7:
        await ctx.send('Invalid amount of arguments! Try again.')
        return

    # roles and ages should be these values, or they are invalid.
    if args[3].lower() != 'transposed' and args[3].lower() != 'established':
        await ctx.send("Error, invalid role input.")
        return
    if (args[5].lower() != 'alive' and args[5].lower() != 'dead'):
        await ctx.send("Error, invalid status input.")
        return
    # if the age is not a numerical value, it is invalid.
    if error.verify_numeric(args[1]):
        sheet.register_char(args)
    else:
        await ctx.send("Error, invalid age input.")
        return
    await ctx.send("stored!")
@bot.command()
async def get_id(ctx, name):
    '''This function retrieves the ID of a requested character from their name.'''
    id_char = sheet.get_id(name)
    # if the id exists, print it out
    if id_char != 'None':
        await ctx.send(name + "'s ID is " + id_char)
    else:
        await ctx.send("This character is not registered!")
@bot.command()
async def primary(ctx, *args):
    '''This method registers the primary stats for a character. It takes
    the primary stat values and passes them on to an SQL function in the sheet.py file'''
    if len(args) != 6:
        await ctx.send('Invalid amount of arguments! Try again.')
        return
    for i in range(0, 6):
        if error.verify_numeric(args[i]) is False:
            await ctx.send("One of your arguments is invalid! Please try again.")
            return
    await ctx.send("What character should these stats be assigned to?")
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    try:
        reply = await bot.wait_for('message', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send('Timeout occurred')
    else:
        char_id = sheet.get_id(reply.content)
        if sheet.verify_id(char_id) is False:
            await ctx.send("Character not found!")
        else:
            await primary_char(ctx, args, char_id)


async def primary_char(ctx, args, char_id):
    '''This function recieves the character id of a character and their inputted
    primary stats, insering those stats into the database.'''
    new_args = args + (char_id,)
    sheet.register_prim(new_args)
    await ctx.send("stored! Secondary stats have been calculated.")

@bot.command()
async def levelup(ctx, name):
    '''This function levels up a character given their id. It prompts the user to increment
    a primary stat by one, and executes a function that does that in the sheet file.'''
    char_id = sheet.get_id(name)
    if sheet.verify_id(char_id) is False:
        await ctx.send("This character is not registered!")
        return
    await ctx.send("Congratulations on leveling up! What stat would you like to increase?")
    # checks if the author sent that message and it's in the same channel
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    try:
        # recieves the user reply
        reply = await bot.wait_for('message', timeout=60.0, check=check)
    # if the user waits too long to reply, a timeout is issued
    except asyncio.TimeoutError:
        await ctx.send('Timeout occurred')
    else:
        if sheet.level_up(str(reply.content), char_id) is False:
            await ctx.send("Failed! Invalid stat name!")
        else:
            await ctx.send("Upgrade Successful!")
@bot.command()
async def editcharacter(ctx, name):
    '''Prompts the user to edit the character values of a given character, and calls another
    function to ask for value.'''
    char_id = sheet.get_id(name)
    if sheet.verify_id(char_id) is False:
        await ctx.send("This character is not registered!")
        return
    await ctx.send("Which characteristic would you like to change?")
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    try:
        reply = await bot.wait_for('message', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send('Timeout occurred')
    else:
        await edit_char_val(ctx, char_id, str(reply.content))

async def edit_char_val(ctx, char_id, column):
    '''This function is called by the previous editcharacter command, and prompts
    the user for the value they want the characteristic to be changed to. Then, it calls
    a method in the sheet file to edit the value in the database.'''
    await ctx.send("And what would you like the value to be?")
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    try:
        reply = await bot.wait_for('message', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send('Timeout occurred')
    else:
        if sheet.edit_char(column, char_id, reply.content) is False:
            await ctx.send("Update failed! Your values are invalid.")
        else:
            await ctx.send("Sucessfully edited the character's " + column)
@bot.command()
async def edit_primary(ctx, char_id):
    """This method prompts the user to choose a primary stat to change from a character's ID."""
    if sheet.verify_id(char_id) is False:
        await ctx.send("This character is not registered!")
        return
    await ctx.send("Which primary stat would you like to change?")
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    try:
        reply = await bot.wait_for('message', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send('Timeout occurred')
    else:
        await edit_primary_val(ctx, char_id, str(reply.content))

async def edit_primary_val(ctx, char_id, column):
    """This method prompts the user for the new value of their previously inputted primary stat.
    It takes in the stat recorded previously, and Then, it calls
    a method in the sheet file to edit the value in the database."""
    await ctx.send("And what would you like the value to be?")
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    try:
        reply = await bot.wait_for('message', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send('Timeout occurred')
    else:
        if sheet.edit_prim(column, char_id, reply.content) is False:
            await ctx.send("Update failed! Your values are invalid.")
        else:
            await ctx.send("Sucessfully edited the character's " + column)

@bot.command()
async def print_sheet(ctx, name):
    """"This method prints out the character sheet by calling print functions from the sheet file.
    It takes the character id corresponding to the sheet."""
    char_id = sheet.get_id(name)
    if sheet.verify_id(char_id) is False:
        await ctx.send("This character is not registered!")
        return
    await ctx.send("```" + select.print_char(char_id) + "\n\nPRIMARY STATS:\n"
                   + select.print_prim(char_id) +
                   "\n\nSECONDARY STATS:\n" + select.print_sec(char_id) + "\n\nABILITIES:\n" 
                   + str(select.calculate_abilities(char_id)[0]) + "\n\nCURRENT WEAPON:\n"
                   + "\n\nCURRENT ARMOR:\n" +
                   "\n\nEQUIPPED ABILITY:\n" + str(select.print_ability(char_id)) 
                   + "\n\nREPUTATION:\n" + str(select.print_rep(char_id)) +  "\n\nSLOE:\n" +  "```")

@bot.command()
async def assign_ability(ctx, name):
    """This function displays the available abilities that a character can
    equip, and prompts user if they want to equip an ability for each slot.. It then passes the 
    reply to a function that prompts the user to assign an ability for each slot."""
    char_id = sheet.get_id(name)
    if sheet.verify_id(char_id) is False:
        await ctx.send("This character is not registered!")
        return
    slots = sheet.calculate_slots(char_id)
    await ctx.send("These are your available abilities!\n" +
                   str(select.calculate_abilities(char_id)[0]))
    await ctx.send("Your available slots: " + str(slots))
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    # iterates through each available slot for the character
    while slots != 0:
        await ctx.send("Would you like to assign an ability for slot " + str(slots) +
                       "? Answer with a Y or N.")
        try:
            reply = await bot.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('Timeout occurred')
        else:
            if str(reply.content) == "Y":
                await assign(ctx, slots, char_id, select.calculate_abilities(char_id)[1])
                slots = slots - 1
            elif str(reply.content) == "N":
                break
            else:
                await ctx.send("Invalid answer, please try again.")

@bot.command()
async def edit_rep(ctx, col, row, char_id):
    """This method updates the reputation of a character, by passing their character id into
    a function in the sheet file that updates the database."""
    if sheet.verify_id(char_id) is False:
        await ctx.send("This character is not registered!")
        return
    sheet.find_rep(col, row, char_id)
    await ctx.send("Reputation updated!")

@bot.command()
async def delete_sheet(ctx, name):
    """This method prompts the user to delete a sheet based on the character ID provided.
    It then executes a method in the sheet file that deletes all the character's information
    from the database."""
    char_id = sheet.get_id(name)
    if sheet.verify_id(char_id) is False:
        await ctx.send("This character is not registered!")
        return
    await ctx.send("Are you sure you want to delete this sheet?")
    print_sheet(ctx, char_id)
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    try:
        reply = await bot.wait_for('message', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send('Timeout occurred')
    else:
        if str(reply.content) == "Y":
            sheet.delete_sheet(char_id)
        elif str(reply.content) == "N":
            await ctx.send("Oky")
        else:
            await ctx.send("Invalid answer, please try again.")
@bot.command()
async def register_item(ctx, item):
    '''This function registers a new item to the database, taking the item's
    name and calling a function in the inventory file to add it to the
    database.'''
    inventory.add_item(item)
    await ctx.send("This item has been included.")
    item_id = inventory.find_item_id(item)
    item_id = sheet.clean_up(str(item_id)).replace(",", "")
    await ctx.send("Please input your flavor text here.")
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    try:
        reply = await bot.wait_for('message', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send('Timeout occurred')
    else:
        inventory.add_text(False, False, str(reply.content), item_id)
        await ctx.send("Added flavor text!")

@bot.command()
async def add_to_inventory(ctx, name):
    '''This method adds an item to the character's inventory. It takes the name of the
    item then prompts the user for the character to add the item to, then calls a 
    function to find how many of that item to add to.'''
    item_id = inventory.find_item_id(name)
    item_id = sheet.clean_up(str(item_id)).replace(",", "")
    await ctx.send("Which character would you like to add this item to?")
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    try:
        reply = await bot.wait_for('message', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send('Timeout occurred')
    else:
        if sheet.verify_id(sheet.get_id(reply.content)) is False:
            await ctx.send("This character could not be found!")
        else:
            await prompt_multiple(ctx, id, reply.content)

@bot.command()
async def show_inv(ctx):
    '''This method shows the inventory of a character, taking in no inputs
    and revealing what items are in a character's inventory.'''
    await ctx.send("Which character's inventory do you want shown?")
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    try:
        reply = await bot.wait_for('message', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send('Timeout occurred')
    else:
        if sheet.verify_id(sheet.get_id(reply.content)) is False:
            await ctx.send("This character could not be found!")
        else:
            data = inventory.show_inv(sheet.get_id(reply.content))
            inv = "```"
            for datum in data:
                inv = inv + sheet.clean_up(str(datum)).replace(",", "").replace("'", "") + "\n"
            await ctx.send(inv + "```")

@bot.command()
async def use_item(ctx, char, name):
    '''This method allows a character to use an item, taking in the item
    and the character using it.'''
    item_id = inventory.find_item_id(name)
    item_id = sheet.clean_up(str(id)).replace(",", "")
    flavor = inventory.print_text(True, False, False, id)
    if item_id is None:
        await ctx.send("Item could not be found!")
    elif sheet.verify_id(sheet.get_id(char)) is False:
        await ctx.send("This character could not be found!")
    elif inventory.find_item_in_char(name, sheet.get_id(char)) is None:
        await ctx.send("This item could not be found in the character's inventory!")
    else:
        if flavor is not None:
            await ctx.send(char + " " + sheet.clean_up(str(flavor)).replace(',', '').strip('"'))
        else:
            await ctx.send(char + "used the item.")

@bot.command()
async def drop_item(ctx, char, name):
    '''This method allows a character to drop an item, taking in the item
    and the character using it.'''
    item_id = inventory.find_item_id(name)
    item_id = sheet.clean_up(str(id)).replace(",", "")
    flavor = inventory.print_text(False, True, False, id)
    if item_id is None:
        await ctx.send("Item could not be found!")
    elif sheet.verify_id(sheet.get_id(char)) is False:
        await ctx.send("This character could not be found!")
    elif inventory.find_item_in_char(name, sheet.get_id(char)) is None:
        await ctx.send("This item could not be found in the character's inventory!")
    else:
        inventory.remove_item(name, sheet.get_id(char))
        if flavor is not None:
            await ctx.send(char + ' ' + sheet.clean_up(str(flavor)).replace(',', '').strip('"'))
        else:
            await ctx.send(char + " dropped the item.")

@bot.command()
async def add_use_flavor(ctx, name):
    '''This method adds flavor text for using an item, taking in the name of the item.'''
    item_id = inventory.find_item_id(name)
    item_id = sheet.clean_up(str(id)).replace(",", "")
    if item_id is None:
        await ctx.send("Item could not be found!")
    else:
        await ctx.send("Please input your flavor text here.")
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        try:
            reply = await bot.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('Timeout occurred')
        else:
            inventory.add_text(True, False, str(reply.content), id)
            await ctx.send("Added flavor text!")

@bot.command()
async def add_drop_flavor(ctx, name):
    '''This method adds flavor text for dropping an item, taking in the name of the item.'''
    item_id = inventory.find_item_id(name)
    item_id = sheet.clean_up(str(id)).replace(",", "")
    if item_id is None:
        await ctx.send("Item could not be found!")
    else:
        await ctx.send("Please input your text here.")
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        try:
            reply = await bot.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('Timeout occurred')
        else:
            inventory.add_text(False, True, str(reply.content), id)
            await ctx.send("Added flavor text!")

@bot.command()
async def add_equippable_flavor(ctx, name):
    '''This method adds flavor text for equipping an item, taking in the name of the item.'''
    item_id = inventory.find_item_id(name)
    item_id = sheet.clean_up(str(item_id)).replace(",", "")
    if item_id is None:
        await ctx.send("Item could not be found!")
    else:
        await ctx.send("Please input your text here.")
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        try:
            reply = await bot.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('Timeout occurred')
        else:
            inventory.add_equippable_text(str(reply.content), item_id)
            await ctx.send("Added flavor text!")
@bot.command()
async def remove_item(ctx, name):
    '''This function allows a user to remove items from the items database,
    taking in the name of the item.'''
    item_id = inventory.find_item_id(name)
    item_id = sheet.clean_up(str(item_id)).replace(",", "")
    if item_id is None:
        await ctx.send("Item could not be found!")
    else:
        inventory.remove_all_item(id)
        await ctx.send("Item removed!")

@bot.command()
async def register_weapon(ctx, name):
    '''This function allows a user to register a new weapon to the database,
    taking in the name of the item.'''
    inventory.add_item(name)
    item_id = inventory.find_item_id(name)
    item_id = sheet.clean_up(str(item_id)).replace(",", "")
    await ctx.send("What's the attack power of this weapon?")
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    try:
        reply = await bot.wait_for('message', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send('Timeout occurred')
    else:
        inventory.add_weapon(name, item_id, str(reply.content), True)
        await ctx.send("Weapon added!")

@bot.command()
async def add_weapon(ctx, name):
    '''This method allows a user to add weapons to a character's inventory,
    taking in the name of the character.'''
    item_id = inventory.find_item_id(name)
    item_id = sheet.clean_up(str(item_id)).replace(",", "")
    if item_id is None:
        await ctx.send("Item could not be found!")
    else:
        await ctx.send("Which character would you like to add this weapon to?")
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        try:
            reply = await bot.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('Timeout occurred')
        else:
            if sheet.verify_id(sheet.get_id(reply.content)) is False:
                await ctx.send("This character could not be found!")
            else:
                await insert_into_inventory(ctx, item_id, reply.content, 1)
                await add_weapon_to_sheet(ctx, item_id, name, reply.content)

@bot.command()
async def equip_weapon(ctx, name):
    '''This method allows a user to equip weapons to their character,
    taking in the name of the character.'''
    item_id = inventory.find_item_id(name)
    item_id = sheet.clean_up(str(item_id)).replace(",", "")
    flavor = inventory.print_text(False, False, True, item_id)
    if item_id is None:
        await ctx.send("Item could not be found!")
    else:
        await ctx.send("Which character would you like to equip this weapon to?")
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        try:
            reply = await bot.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('Timeout occurred')
        else:
            if sheet.verify_id(sheet.get_id(reply.content)) is False:
                await ctx.send("This character could not be found!")
            else:
                inventory.equip_weapon(item_id, sheet.get_id(reply.content), True)
                if flavor is not None:
                    await ctx.send(str(reply.content) + ' ' +
                                   sheet.clean_up(str(flavor)).replace(',', '').strip('"'))
                else:
                    ctx.send(str(reply.content) + "equipped the weapon.")
@bot.command()
async def register_armor(ctx, name):
    '''This function allows a user to register a new armor to the database,
    taking in the name of the item.'''
    inventory.add_item(name)
    item_id = inventory.find_item_id(name)
    item_id = sheet.clean_up(str(item_id)).replace(",", "")
    await ctx.send("What's the defense of this armor?")
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    try:
        reply = await bot.wait_for('message', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send('Timeout occurred')
    else:
        inventory.add_weapon(name, item_id, str(reply.content), False)
        await ctx.send("Armor added!")

@bot.command()
async def add_armor(ctx, name):
    '''This method allows a user to add armor to a character's inventory,
    taking in the name of the character.'''
    item_id = inventory.find_item_id(name)
    item_id = sheet.clean_up(str(item_id)).replace(",", "")
    if item_id is None:
        await ctx.send("Item could not be found!")
    else:
        await ctx.send("Which character would you like to add this weapon to?")
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        try:
            reply = await bot.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('Timeout occurred')
        else:
            if sheet.verify_id(sheet.get_id(reply.content)) is False:
                await ctx.send("This character could not be found!")
            else:
                await insert_into_inventory(ctx, item_id, reply.content, 1)
                await add_armor_to_sheet(ctx, item_id, name, reply.content)

@bot.command()
async def equip_armor(ctx, name):
    '''This method allows a user to equip armor to their character,
    taking in the name of the character.'''
    item_id = inventory.find_item_id(name)
    item_id = sheet.clean_up(str(item_id)).replace(",", "")
    flavor = inventory.print_text(False, False, False, id)
    if item_id is None:
        await ctx.send("Item could not be found!")
    else:
        await ctx.send("Which character would you like to equip this weapon to?")
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        try:
            reply = await bot.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('Timeout occurred')
        else:
            if sheet.verify_id(sheet.get_id(reply.content)) is False:
                await ctx.send("This character could not be found!")
            else:
                inventory.equip_weapon(id, sheet.get_id(reply.content), False)
                if flavor is None:
                    await ctx.send(str(reply.content) + ' ' +
                                   sheet.clean_up(str(flavor)).replace(',', '').strip('"'))
                else:
                    await ctx.send(str(reply.content) + " equipped the armor.")
@bot.command()
async def add_equip_flavor(ctx, name):
    '''This method adds flavor text for adding an item to an inventory, taking in the name
    of the item.'''
    item_id = inventory.find_item_id(name)
    item_id = sheet.clean_up(str(item_id)).replace(",", "")
    if item_id is None:
        await ctx.send("Item could not be found!")
    else:
        await ctx.send("Please input your flavor text here.")
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        try:
            reply = await bot.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('Timeout occurred')
        else:
            inventory.add_text(True, False, str(reply.content), item_id)
            await ctx.send("Added flavor text!")
@bot.command()
async def register_npc(ctx, name):
    '''This method adds a new npc to the database, taking in the npc's name.'''
    npc.register_npcs(name, False)
    await ctx.send("npc registered!")
@bot.command()
async def add_dialogue(ctx, name):
    '''This function adds npc dialogue to the database. It takes in the npc's name,
    and prompts the user to input in the text.'''
    npc_id = npc.get_npc_id(name, False)
    npc_id = sheet.clean_up(str(npc_id)).replace(",", "")
    if npc_id is None:
        await ctx.send("NPC not found!")
    else:
        await ctx.send("Input your text here.")
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        try:
            reply = await bot.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('Timeout occurred')
        else:
            npc.add_dialogue(reply.content, npc_id)
            await ctx.send('Dialogue added!')

@bot.command()
async def talk_to(ctx, name):
    '''This method lets characters talk to npcs, outputting their dialogue.
    It takes in the npc's name.'''
    npc_id = npc.get_npc_id(name, False)
    npc_id = sheet.clean_up(str(npc_id)).replace(",", "")
    if npc_id is None:
        await ctx.send("NPC not found!")
    else:
        await ctx.send(name.upper() + ": " +
                       sheet.clean_up(str(npc.talk_to(npc_id))).replace(",", ""))

@bot.command()
async def remove_npc(ctx, name):
    '''This method removes a npc from the database, taking in the npc's name.'''
    npc_id = npc.get_npc_id(name, False)
    npc_id = sheet.clean_up(str(npc_id)).replace(",", "")
    if npc_id is None:
        await ctx.send("NPC not found!")
    else:
        npc.remove_npc(npc_id, False)
        await ctx.send("NPC removed!")

@bot.command()
async def register_enemy(ctx, name):
    '''This method registers a new enemy to the database, taking in the enemy's name.'''
    npc.register_npcs(name, True)
    await ctx.send("enemy registered!")

@bot.command()
async def register_enemy_stats(ctx, *args):
    '''This method registers the enemy's stats, taking in all the stats and prompting
    the user for the enemy's name.'''
    if len(args) != 4:
        await ctx.send('Invalid amount of arguments! Try again.')
        return
    for i in range(0, 4):
        if error.verify_numeric(args[i]) is False:
            await ctx.send("One of your arguments is invalid! Please try again.")
            return
    await ctx.send("What enemy should these stats be assigned to?")
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    try:
        reply = await bot.wait_for('message', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send('Timeout occurred')
    else:
        npc_id = npc.get_npc_id(reply.content, True)
        if npc_id is None:
            await ctx.send("Character not found!")
        else:
            npc_id = sheet.clean_up(str(npc_id)).replace(",", "")
            npc.add_stats(args, npc_id)
            await ctx.send("Stats added!")
@bot.command()
async def remove_enemy(ctx, name):
    '''This method removes an enemy from the database, taking in the name of the enemy.'''
    npc_id = npc.get_npc_id(name, True)
    npc_id = sheet.clean_up(str(npc_id)).replace(",", "")
    if npc_id is None:
        await ctx.send("NPC not found!")
    else:
        npc_id = sheet.clean_up(str(npc_id)).replace(",", "")
        npc.remove_npc(npc_id, True)
        await ctx.send("NPC removed!")

@bot.command()
async def adjustGrid(ctx, row, col):
    if error.verify_numeric:
        grid.adjust_size(int(row), int(col))
    else:
        await ctx.send("Inputs are invalid!")
        return
    await ctx.send("dimensions changed!")

@bot.command()
async def fight(ctx, player, name):
    npc_id = npc.get_npc_id(name, True)
    npc_id = sheet.clean_up(str(npc_id)).replace(",", "")
    char_id = sheet.get_id(player)
    char_id = sheet.clean_up(str(char_id)).replace(",", "")
    mov = select.select_secondary(char_id)[8]
    mov = sheet.clean_up(str(mov)).replace(",", "")
    if npc_id is None:
        await ctx.send("NPC not found!")
    elif sheet.verify_id(char_id) is False:
        await ctx.send("Player not found!")
    else:
        enemy = name[0]
        chara = player[0]
        grid.random_pos()
        await ctx.send("```" + grid.generate_grid(chara, enemy) + "```")
        await ctx.send("KEY: \n" + player + " - " + chara + "\n" + name + " - " + enemy)
        await turn(ctx, player, npc_id, enemy, int(mov))

async def turn(ctx, player, npc_id, enemy, mov):
    max_mov = mov
    char_id = sheet.get_id(player)
    char_id = sheet.clean_up(str(char_id)).replace(",", "")
    await ctx.send("You have " + str(mov) + " MOV left.")
    await ctx.send("Which direction do you want to move, and how far? Or press S to end the turn.")
    await ctx.send("Input both values like this: DirectionNumber(UP(U), DOWN(D), LEFT(L), RIGHT(R)), then Number")
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    try:
        reply = await bot.wait_for('message', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send('Timeout occurred')
    else:
        if reply.content.upper() == 'S':
            await ctx.send("Turn over.")
            return await enemy_turn(ctx, player, npc_id, enemy, max_mov)
        if len(reply.content) < 2:
            await ctx.send("Invalid input format. Please try again (e.g., U3 or D2).")
            return await turn(ctx, player, npc_id, enemy, mov)
        direction = reply.content[0].upper()
        if direction not in ['U', 'D', 'L', 'R']:
            await ctx.send("Invalid direction. Use U (up), D (down), L (left), or R (right).")
            return await turn(ctx, player, npc_id, enemy, mov)
        value = int(reply.content[1:])
        if value > mov:
            await ctx.send("Not enough movement!")
            return await turn(ctx, player, npc_id, enemy, mov)
        mov = mov - value + grid.move(direction, value)
        enemy = enemy[0]
        chara = player[0]
        await ctx.send("```" + grid.generate_grid(chara, enemy) + "```")
        return await turn(ctx, player, npc_id, enemy, mov)

async def enemy_turn(ctx, player, npc_id, enemy, player_mov):
    mov = npc.get_enemy_stats(npc_id)[3]
    mov = int(sheet.clean_up(str(mov)).replace(",", ""))
    grid.a_star(mov)
    enemy = enemy[0]
    chara = player[0]
    await ctx.send("```" + grid.generate_grid(chara, enemy) + "```")
    await turn(ctx, player, npc_id, enemy, player_mov)



async def add_weapon_to_sheet(ctx, item_id, name, char):
    '''This method adds an equippable weapon to the database, taking
    in the weapon's id, name, and the character id.'''
    atk = inventory.find_atk(item_id, True)
    atk = int(sheet.clean_up(str(atk)).replace(",", ""))
    inventory.add_weapon_to_sheet(name, item_id, sheet.get_id(char), atk)
    await ctx.send("Weapon added to inventory!")

async def add_armor_to_sheet(ctx, item_id, name, char):
    '''This method adds an equippable armor to the database, taking
    in the weapon's id, name, and the character id.'''
    atk = inventory.find_atk(item_id, False)
    atk = int(sheet.clean_up(str(atk)).replace(",", ""))
    inventory.add_armor_to_sheet(name, item_id, sheet.get_id(char), atk)
    await ctx.send("Armor added to inventory!")

async def prompt_multiple(ctx, item_id, name):
    '''This method prompts the user to choose how many items to
    add to the inventory.'''
    # finds the maximum amount of items a character can hold
    max_item = select.select_secondary(sheet.get_id(name))[12]
    max_item = int(sheet.clean_up(str(max_item)).replace(",", ""))
    inv = int(sheet.clean_up(str(inventory.find_inv_count(sheet.get_id(name)))).replace(",", ""))
    await ctx.send("How many of this item should be added?")
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    try:
        reply = await bot.wait_for('message', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send('Timeout occurred')
    else:
        if error.verify_numeric(reply.content) is False:
            await ctx.send("Invalid input!")
        # if the number requested is larger than the maximum, it can't be added
        elif max_item < inv + int(reply.content):
            quantity = inv + int(reply.content)
            await ctx.send("This character's inventory is too full to hold this many items! " +
                           f"{quantity} / {max_item}")
        else:
            await insert_into_inventory(ctx, item_id, name, reply.content)

async def insert_into_inventory(ctx, item_id, name, items):
    '''This method inserts an item into the database, taking in the item id,
    the item name, and the number of items to add.'''
    data = inventory.find_item(sheet.get_id(name), item_id, int(items))
    flavor = inventory.print_text(False, False, True, item_id)
    if data is None:
        await ctx.send(f"Could not find {data[0]}")
    else:
        print(item_id)
        if flavor is not None:
            await ctx.send(name + ' ' + sheet.clean_up(str(flavor)).replace(',', '').strip('"'))
        else:
            await ctx.send(name + "added this item to their inventory.")

async def assign(ctx, slot, char_id, valid):
    """This function prompts the user to assign an ability for their character, for
    each slot. It then calls a function from the sheet file to put it in the database."""
    if sheet.verify_id(char_id) is False:
        await ctx.send("This character is not registered!")
        return
    await ctx.send("Please choose an ability for slot " + str(slot) + ".")
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    try:
        reply = await bot.wait_for('message', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send('Timeout occurred')
    else:
        print(valid)
        if reply.content in valid:
            sheet.update_abilities(char_id, slot, reply.content)
            await ctx.send("Ability assigned!")
        else:
            await ctx.send("not a valid ability!")

@bot.event
async def on_member_join(member):
    """This function recognizes when a new member joins a server, printing
    the appropriate welcome message."""
    print("Recognised that a member called " + member.name + " joined")
    channel = bot.get_channel(552942757358993470)
    await channel.send('Welcome, ' + member.name + ' to the Republic of Blackthorn!' +
    'Be sure to mind the laws, buy Voidrot products, and do your part to keep Blackthorn safe and' +
    'secure from criminals and the Overgrowth.')

@bot.event
async def on_member_remove(member):
    """This function recognizes when a new member leaves a server, printing
    the appropriate goodbye message."""
    print("Recognised that a member called " + member.name + " left")
    channel = bot.get_channel(552942757358993470)
    await channel.send('Goodbye ' + member.name + '. Your service to Blackthorn will' +
    'be sorely missed.')

@bot.event
async def on_member_ban(member):
    """This function recognizes when a new member is banned a server, printing
    the appropriate message."""
    print("Recognised that a member called " + member.name + " was banned")
    channel = bot.get_channel(552942757358993470)
    await channel.send(member.name + ' was expelled from the Republic of Blackthorn for rebellious'+
    'behavior and aiding and abetting Resistance members. The penalty for this crime is death.')

@bot.event
async def on_member_unban(user):
    """This function recognizes when a new member is unbanned from a server, printing
    the appropriate message."""
    channel = bot.get_channel(552942757358993470)
    await channel.send('Recognizing the service of ' + user.name + ', the Republic of Blackthorn' +
    'has decided to pardon this person.')

@bot.event
async def on_command_error(ctx, err):
    """This function checks if there is an invalid amount of arguments in a command,
    and prints out an error message."""
    if isinstance(err, commands.MissingRequiredArgument):
        await ctx.send('Invalid amount of arguments! Try again.')
bot.run(config.TOKEN)
