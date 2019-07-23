# EpiGear

## About

EpiGear is a discord bot for server creation, and includes several points:
- Creation of permission groups
- Creation of roles with corresponding permissions on the server
- Creation of channels and categories according to settings with permissions overwrites
- Update of the channels and roles even after their creation
- All based on a configuration file

## How to install it ?

1. First, you will have to clone the project.

```shell
git clone https://github.com/gastbob40/epigear
```

2. Consider creating a `virtual environment`, in order to install dependencies locally.

```shell
python -m venv venv
```

3. You need to activate the virtual environment now

```shell
# If you are on Linux or Mac ?
source venv/bin/activate 

# If you are on Windows
./venv/Scripts/activate
``` 

4. Finally, install the dependencies

````shell
pip install requirements.txt
````

## How it works ?

The `run` folder contains all the data of the program configuration.

### config_bot

This folder contain a single file, `default.config.yml`. This file looks like this:
 
```yaml
# General information
discord_server_id: ~
token: ~

# Clear information
clear: false
channels_to_ignore: ~ 
roles_to_ignore:   
    - '@everyone' 
```

You will therefore have to modify in this file the `discord_server_id` by the one of the server where you want to run the bot.
Also remember to put the `token` of your bot discord.

You can also choose to delete the roles and channels of the server in question before creating the new roles and channels.
The `channels_to_ignore` and `roles_to_ignore` are lists of name of roles / channels

### config_server

This folder contains the configuration of permissions groups, roles and channels.

#### `perms_groups.yml`

This file contains the names of the permission groups and their correspondence to Discord.
Each group correspond to certain settings that can be used in the rest of the configuration file to set permissions to different roles
You can therefore add or remove groups.

For example:

```yaml
READ_ONLY: #the name of the group
  read_messages: true     # One permission (read_messages) and its value (true)
  send_messages: false    # One permission (send_messages) and its value (false)
```

Here is the list of all the permissions:

```yaml
# Moderation permission
create_instant_invite: true
administrator: true
kick_members: true
ban_members: true
view_audit_log: true
manage_nicknames: true
manage_roles: true
manage_emojis: true
manage_webhooks: true
manage_channels: true
manage_guild: true

# General permission
change_nickname: true
add_reactions: true

# Text channels permissions
read_messages: true
send_messages: true
send_tts_messages: true
manage_messages: true
embed_links: true
attach_files: true
read_message_history: true
mention_everyone: true
external_emojis: true

# Voice channels permissions
connect: true
speak: true
mute_members: true
deafen_members: true
move_members: true
use_voice_activation: true
priority_speaker: true
```

When you create a group of permissions, you don't have to set all the permissions to true or false.
If a permission is not in the list, it will be set by default to false for the server perm, and to Neutral for the channels perm. 


#### `roles.yml`

This file contains the list of roles and their specificities.

For example:

```yaml
EXTERNE:  # The name of the role object, used in channel definition
  name: Externe             # The name of the role (on discord)
  color: 0xc0ff00           # The color of the role
  permissions: DEFAULT      # The permission group of the role (one of the perm group set in perms_groups.yml)
  hoist: true               # If the role is hoist or not
  mentionable: false        # If the role is mentionable or not
```


#### `server_channels.yml`

The file contains the list of categories and channels for the server.

For example:

```yml
 CATEGORY
my_category: # name of the variable
  # NAME
  name: MY_CATEGORY # name displayed in discord
  # PERM
  overwrites:
    ROLE: HIDDEN # overwrites for the category : couple of ROLE and PERM_GROUP (linked to perms_groups.yml) (can be null -> ~ )
  # EVERYONE
  default_perm: HIDDEN # PERM_GROUP for the role everyone (can not be null)
  # CHANNELS
  channels: # list of the channels in your category (can be null -> ~ )

    my_text_channel:
      # NAME
      name: my-text-channel # name of the channel in discord
      #PERM
      overwrites: # overwrites for the channel : couple of ROLE and PERM_GROUP (can be null -> ~ )
        ROLE: DEFAULT # overwrites the permission of the category set previously
      default_perm: HIDDEN # PERM_GROUP for the role everyone (can not be null)

  # VOCAL CHANNELS
  vocal_channels: #list of the voice channels in your category (can be null -> ~ )

    my_voice_channel: (can not be null -> you need each following parameters)
      # NAME
      name: my_voice_channel
      #PERM
      overwrites: # overwrites for the channel : couple of ROLE and PERM_GROUP (can be null -> ~ )
        ROLE: VOCAL # overwrites the permission of the category set previously
      default_perm: HIDDEN # PERM_GROUP for the role everyone (can not be null)
```

Note that in discord, the name of the channels and categories follow some rules :
 - the name of a category is in upper case (example: My Category -> MY CATEGORY)
 - the name of a channel (text or vocal) is in lower case and space will be filled with '-' (example: My Text Channel -> my-text-channel)

You can write the names you want in the config file but they will not appear in discord as they are written here
