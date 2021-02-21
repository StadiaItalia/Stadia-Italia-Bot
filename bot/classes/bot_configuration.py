class BotConfiguration:
    def __init__(self, **args):
        self.guildId = args.get("guildId")
        self.role = args.get("role",'Template')
        self.command_channel = args.get("command_channel",'Template')
        self.command_prefix = args.get("command_prefix", 's!')
        self.welcome_channel = args.get("welcome_channel",'Template')
        self.welcome_message_list = args.get("welcome_message_list", 'Template')
        self.welcome_direct_message = args.get("welcome_direct_message", 'Template')
        self.albicocco_message_list = args.get("albicocco_message_list", [])
        self.blue_message_list = args.get("blue_message_list", [])



    def to_dict(self):
        return {
            "guildId": self.guildId,
            "role": self.role,
            "command_prefix" : self.command_prefix,
            "command_channel": self.command_channel,
            "welcome_channel": self.welcome_channel,
            "welcome_message_list": self.welcome_message_list,
            "welcome_direct_message": self.welcome_direct_message,
            "albicocco_message_list": self.albicocco_message_list,
            "blue_message_list": self.blue_message_list
        }

    @staticmethod
    def from_dict(obj):
        return BotConfiguration(**obj)
