from src.addCommand import addCommand
from src.deleteCommand import deleteCommand
from src.listCommand import listCommand
from src.updateCommand import updateCommand
from src.infoCommand import infoCommand
from src.helpCommand import helpCommand

commands = {
    'add' : addCommand,
    'delete' : deleteCommand,
    'list' : listCommand,
    'info' : infoCommand,
    'update' : updateCommand,
    'help' : helpCommand,
    '-h' : helpCommand,
    '--help' : helpCommand
}

async def split_args(message, argv, client) :
    if len(argv) < 2:
        await message.channel.send(":x: No command")
        return -1
    if argv[1] in commands.keys():
        await commands[argv[1]](message, argv, client)
        return 0
    await message.channel.send(":x: Wrong command")



