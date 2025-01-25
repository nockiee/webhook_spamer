## Description
This is a python spam bot based on webhooks provided by discord. The application sends messages every N seconds on behalf of one of your selected webhooks.

## How to use
1. Create `hook.txt` and `message.json` files
2. In the `hook.txt` file, specify the URLs of the webhooks (1 per line)
3. Insert the following construction into `message.json`:
```json
{
    "username": "HOOK NAME",
    "avatar_url": "AVARAR_URL",
    "content": "MESSAGE"

      }
```
5. Run `main.py` and select the number of messages.

## NOTICE
Do not use this software with the intent to harm others. the software is intended for demonstration purposes.
