import os
from bot.bot import main
from bot.token import TELEGRAM_BOT_TOKEN

if __name__ == '__main__':
    os.environ['TOKEN'] = TELEGRAM_BOT_TOKEN  # '123456789:123456789-123456789-123456789-12345'
    main()
