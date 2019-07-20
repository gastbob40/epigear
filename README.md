# EpiGear

## About

EpiGear is a discord bot for server creation, and includes several points.
- Creation of permission groups
- Creation of roles based on permissions
- Creation of a channel and category according to these permissions
- Synchronization of roles and salons even after their creation
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
discord_server_id: ~
current_promo: ~
token: ~
```

You will therefore have to modify in this file the `discord_server_id` by the one of the server where you want to run the bot.
Also remember to put the `token` of your bot discord

> The `current_promo` line is only used for EPITA, it is not to be filled in for other uses

### config_server

This folder contains the configuration of permissions groups, roles and channels.

#### `perms_groups.yml`

This file contains the names of the permission groups and their correspondence to Discord.
You can therefore add or remove groups.

For example:

```yaml
READ_ONLY: #the name of the group
  read_messages: true     # One permission (read_messages) and its value (true)
  send_messages: false    # One permission (send_messages) and its value (false)
```

#### `roles.yml`

This file contains the list of roles and their specificity.

For example:

```yaml
EXTERNE:  # The name of the role object, used in channel definition
  name: Externe             # The name of the role (on discord)
  color: 0xc0ff00           # The color of the role
  permissions: DEFAULT      # The permission group of the role (link to perms_groups.yml)
  hoist: true               # If the role is hoist or not
  mentionable: false        # If the mentionable is hoist or not
```

#### `server_channels.yml`

The file contains the list of categories and channels for the server

For example:

```yml
epita_adm:                   # The name of the object
  name: EPITA/ADM👥          # Name of the category 
  overwrites: ~              # General permission (link to perms_group.yml)
  default_perm: HIDDEN       # The default perm 

  channels:                  # List of channel 
    administration:          # Name of the object
      name: administration   # Name of the channel
      overwrites:            # Overwrited permission
        STAFF_EPILOGIN: SERVER_ADMIN_PERM   # role (link to roles.yml): permisision (link to perms_group.yml)
        ADMIN: ADMIN_PERM                   # Also
      default_perm: HIDDEN   # Default perm

  vocal_channels:            # Same things for vocal channel
    reunion:
      name: Réunion
      overwrites:
        STAFF_EPILOGIN: SERVER_ADMIN_PERM
        ADMIN: ADMIN_PERM
        MODO: VOCAL
        ADM: VOCAL
        PROF: VOCAL
      default_perm: HIDDEN
```