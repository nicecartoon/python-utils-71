import sys
from datetime import datetime

class RetroGameLogger:
    LEVELS = {
        "INFO": ("\u001b[92m[▮▮▮▮▮]\u001b[0m", "SYS"),
        "WARNING": ("\u001b[93m[▮▮▮▯▯]\u001b[0m", "WARN"),
        "ERROR": ("\u001b[91m[▮\u001b[90m▮▮▮▮\u001b[91m]\u001b[0m", "CRIT"),
        "CRITICAL": ("\u001b[95m[💀💀💀]\u001b[0m", "DEATH")
    }

    def __init__(self, game_title: str = "RETRO-OS"):
        self.game_title = game_title.upper()

    def _format(self, level: str, message: str) -> str:
        bar, prefix = self.LEVELS.get(level.upper(), ("\u001b[97m[?????]\u001b[0m", "UNKN"))
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        return f"[{timestamp}] <{self.game_title}> {bar} | {prefix} :: {message}"

    def log(self, level: str, message: str):
        formatted_message = self._format(level, message)
        sys.stdout.write(formatted_message + "\n")
        sys.stdout.flush()

    def info(self, msg: str): 
        self.log("INFO", msg)

    def warning(self, msg: str): 
        self.log("WARNING", msg)

    def error(self, msg: str): 
        self.log("ERROR", msg)

    def critical(self, msg: str): 
        self.log("CRITICAL", msg)

    def achievement(self, title: str, xp: int = 100):
        border = "★" * (len(title) + 26)
        msg = f"\n{border}\n★ ACHIEVEMENT UNLOCKED: {title} (+{xp} XP) ★\n{border}\n"
        sys.stdout.write(f"\u001b[96m{msg}\u001b[0m")
        sys.stdout.flush()