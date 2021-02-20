class BotConfiguration:
    def __init__(self, **args):
        self.guildId = args.get("guildId")
        self.role = args.get("role")
        self.command_channel = args.get("command_channel", 'spam-bot')
        self.command_prefix = args.get("command_prefix", 's!')
        self.welcome_channel = args.get("welcome_channel", 'generale')
        self.welcome_message_list = args.get("welcome_message_list", "Ciao e benvenuto sul server discord di Stadia Italia {member.mention}.")
        self.welcome_direct_message = args.get("welcome_direct_message", "Ciao e benvenuto sul server discord di Stadia Italia.")

    def to_dict(self):
        return {
            "guildId": self.guildId,
            "role": self.role,
            "command_prefix" : self.command_prefix,
            "command_channel": self.command_channel,
            "welcome_channel": self.welcome_channel,
            "welcome_message_list": self.welcome_message_list,
            "welcome_direct_message": self.welcome_direct_message
        }

    @staticmethod
    def from_dict(obj):
        return BotConfiguration(**obj)
