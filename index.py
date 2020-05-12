# code source : https://github.com/gastbob40/epigear
# continué par : Delepoulle Samuel et Boddaert Arthur



from argparse import ArgumentParser
import discord
import yaml
from src.discord_creator.discord_creator import DiscordCreator
from src.config_builder.config_builder import ConfigBuilder
from src.utils import *
from discord.ext import commands # added

# Logger
logger = logging.getLogger("epigear_logger")

with open('run/config_bot/config.default.yml', 'r', encoding='utf8') as stream:
    config_bot = yaml.safe_load(stream)

client = commands.Bot(command_prefix='--')
mode = "build"

async def create():
    discord_creator = DiscordCreator(client, config_bot['discord_server_id'])
    roles_to_ignore = config_bot['roles_to_ignore'] if config_bot['roles_to_ignore'] is not None else []

    if config_bot['clear_channels']:
        channels_to_ignore = config_bot['channels_to_ignore'] if config_bot['channels_to_ignore'] is not None else []
        await discord_creator.delete__channels(channels_to_ignore)
    if config_bot['clear_roles']:
        await discord_creator.delete_roles(roles_to_ignore)

    await discord_creator.create_role(roles_to_ignore)
    await discord_creator.create_categories_and_channels()
    await discord_creator.get_roles_id()


async def build():
    config_builder = ConfigBuilder(client, config_bot['discord_server_id'])
    config_builder.create_config()


@client.event
async def on_ready():
    logger.info('We have logged in as {0.user}'.format(client))
    if mode == 'create':
        await create()
    elif mode == 'build':
        await build()
    #quit()

# **************************************************************************
# évènements 
# **************************************************************************

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await client.process_commands(message) # nécessaire pour intégrer des des commandes et des évènements
    

# **************************************************************************
# commandes 
# **************************************************************************
command_brief="affiche la liste des roles existants"
command_help="affiche la liste des roles existants\n"
@client.command(name="rolelist", help=command_help)
async def rolelist(ctx, *args):
    embed = discord.Embed(title="--rolelist")
    texte = ""
    for role in ctx.guild.roles:
        if role.name != "@everyone":
            texte += role.name + "\n"
    embed.description = texte
    await ctx.send(embed=embed)

command_brief="affiche la liste des utilisateurs du serveur"
command_help="affiche la liste des utilisateurs du serveur\narguments possibles: nom de rôle, statut, nom d'un salon vocal ou '-o' suivi d'un nom de fichier\n"
command_help+="  --list : affiche la liste des utilisateurs ayant au moins un rôle\n"
command_help+="  --list ROLE1 ROLE2 ... : affiche la liste des utilisateurs ayant les rôles spécifiés\n"
command_help+="  --list STATUT1 STATUT2 ... : affiche la liste des utilisateurs ayant les statuts spécifiés\n"
command_help+="  --list SALON_VOCAL1 SALON_VOCAL1 ... : affiche la liste des utilisateurs présents dans les salons vocaux spécifiés\n"
command_help+="  --list -o NOM_DE_FICHIER : crée et upload un fichier contenant les noms des utilisateurs, leurs id et leurs rôles"
@client.command(name="list", help=command_help, brief=command_brief) 
async def list(ctx, *args):
    embed = discord.Embed(title="--list")
    texte = ""
    memberList = []
    memberListRole = []
    memberListStatut = []
    statutList = ["ONLINE", "OFFLINE", "IDLE", "DND", "INVISIBLE"]
    statutArgsList = []
    # list sans argument
    if len(args) == 0:
        for member in ctx.guild.members:
            if len(member.roles) > 1:
                if not member.bot:  
                    memberList.append(member)
    else:
        if args[0] == "-o" and len(args) == 2:
            memberRoles = ""
            file = open("./files/list-o/"+args[1]+".txt", "w+")
            for member in ctx.guild.members:
                memberRoles = ""
                for role in member.roles:
                    memberRoles += role.name
                    if not role == member.roles[(len(member.roles)-1)]:
                        memberRoles += ","
                file.write(pseudo(member)+":"+str(member.id)+":"+memberRoles+"\n")
            file.close()
            return await ctx.send(file=discord.File("./files/list-o/"+args[1]+".txt", filename=args[1]))
        # list STATUT
        for arg in args:
            if arg.upper() in statutList:
                statutArgsList.append(arg)
                for member in ctx.guild.members:
                    if check_statut(member, arg):
                        if member not in memberListStatut and not member.bot:
                            memberListStatut.append(member)

        # list ROLE
        for arg in args:
            for role in ctx.guild.roles:
                if role.name.upper() == arg.upper():
                    for member in ctx.guild.members:
                        if role in member.roles:
                            if member not in memberListRole and not member.bot:
                                memberListRole.append(member)

        # list SALON_VOCAL
        for arg in args:
            for voice_channel in ctx.guild.voice_channels:
                if voice_channel.name.upper() == arg.upper():
                    for member in voice_channel.members:
                        if member not in memberList and not member.bot:
                            memberList.append(member)

    if len(memberListRole) > 0 and len(memberListStatut) > 0:
        for item in memberListRole:
            if item in memberListStatut:
                memberList.append(item)
    else:
        if len(memberListRole) > 0:
            memberList = memberListRole
        if len(memberListStatut) > 0:
            memberList = memberListStatut
    texte = str(len(memberList)) + " personnes trouvées" + "\n \n"
    for memberListItem in memberList:
        texte += pseudo(memberListItem) + "\n"
    embed.description = texte;
    return await ctx.send(embed=embed)


@client.command(name="dm")
async def dmall(ctx, role_arg, *args):
    # on récupère le role concerné
    listRole = []
    for role in ctx.guild.roles:
        if role.name.upper() == role_arg.upper():
            listRole.append(role)
            await ctx.send(role.name)
    # on établit la liste des personnes concernées
    destinataires = []
    for member in ctx.guild.members:
        for role in listRole:
            if member not in destinataires and role in member.roles and not member.bot:
                destinataires.append(member)
                await ctx.send(member.name)
    # on récupère les fichiers attachés
    attachmentList = []
    for attachment in ctx.message.attachments:
        attachmentList.append(await attachment.to_file())
    # on envoie le message à chaque personne concernée
    for destinataire in destinataires:
        await ctx.send("send")
        await destinataire.send(content=" ".join(args), files=attachmentList)

# **************************************************************************
# **************************************************************************
# **************************************************************************

def pseudo(member): # si le membre s'est renommé sur le serveur on prend son surnom, sinon on prend son pseudo habituel
    if isinstance(member, discord.Member):
        if member.nick is None:
            return member.name
        else:
            return member.nick
    return

def check_statut(member, statut): # si le statut du membre correspond au statut 'statut' on retourne True
    if isinstance(member, discord.Member) and isinstance(statut, str):
        if statut.upper() == "ONLINE":
            if member.status == discord.Status.online:
                return True
        if statut.upper() == "OFFLINE":
            if member.status == discord.Status.offline:
                return True
        if statut.upper() == "IDLE":
            if member.status == discord.Status.idle:
                return True
        if statut.upper() == "DND":
            if member.status == discord.Status.dnd:
                return True
        if statut.upper() == "INVISIBLE":
            if member.status == discord.Status.invisible:
                return True
    return False

# **************************************************************************
# **************************************************************************
# **************************************************************************

def main():
    client.run(config_bot['token'])


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true',
                        help="show debug messages")
    parser.add_argument('-m', '--mode', default='create',
                        help="show debug messages")
    args = parser.parse_args()
    define_logger(args)
    logger.info('Launching EpiGear')
    logger.debug('Debug Mod Enabled')
    mode = args.mode
    main()