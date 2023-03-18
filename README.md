# winencrpyt

`winencrypt` is a very simple tool that attempts to solve the "clear-text" password problem in configuration files. It might even satisfy your InfoSec team so they will leave you alone (but probably not)!

## Background

How many times have you opened up Notepad and done this...

```
USERNAME=myuser
PASSWORD=mypassword
```

You do a little `CTRL + S` and you save that puppy as `.env` at the root directory of your project. You then throw your project on a server and fire it up as a service. Simple, easy, works great!

You go to tell your team about your project, our protagonist, Joel, starts poking around, and the goody-two-shoes sees your `.env` file and sees that password plain as day.

<p align="center">
	<img src="https://github.com/newvicx/winencrypt/blob/master/docs/img/narc.gif?raw=true" alt='narc'>
</p>

The narc rats you out to InfoSec...

`winencrypt` allows you store that plain text password as an encrypted integer and then decrypt that password at runtime. Let's discuss...

## Installation

First things first, install `winencrypt` with `pip`

`pip install winencrypt`

As the name implies (**WIN** - encrypt), this is for Windows systems only as it uses the [Data Protection API](https://en.wikipedia.org/wiki/Data_Protection_API)

## Usage

### Encryption

To encrypt data, use the `encrypt` command...

![encrypt.jpg](https://github.com/newvicx/winencrypt/blob/master/docs/img/encrypt.jpg?raw=true)

The data will be hidden as you type (yes, we're looking at you Dale! Stop sharing your screen on Teams when you're typing sensitive information.)

That long a** integer is your encrypted text. Only the user who encrypted the text can decrypt it (and only on the same machine).

### Decryption

You can decrypt the data from the command line as well, use the `decrypt` command...

![decrypt-1.jpg](https://github.com/newvicx/winencrypt/blob/master/docs/img/decrypt-1.jpg?raw=true)

`winencrypt` will ask for confirmation to show the encrypted text. If you proceed, your text will be shown...

![decrypt-2.jpg](https://github.com/newvicx/winencrypt/blob/master/docs/img/decrypt-2.jpg?raw=true)

Decrypting from the command line isn't that helpful though. What we want is to decrypt the password at runtime after we load in the `.env` file.

So what do we do?

<p align="center">
	<img src="https://github.com/newvicx/winencrypt/blob/master/docs/img/king.gif?raw=true" alt='king'>
</p>

### ...Enter Pydantic

[Pydantic](https://docs.pydantic.dev/) makes settings management easy through the `BaseSettings` class. `winencrypt` provides a custom type that can be used with Pydantic and will decrypt your sensitive information at runtime.

```python
from pydantic import BaseSettings
from winencrypt import Win32Crypt


class MySettings(BaseSettings):
    username: str
    password: Win32Crypt
    
    class Config:
        env_file=".env"
        
   
SETTINGS = MySettings()
```

`Win32Crypt` will take the integer output from the `encrypt` command and decrypt it when the settings are loaded. The value is stored as a `SecretStr` so to retrieve the value you need to use the `get_secret_value()` method...

```python
password = SETTINGS.password.get_secret_value()
```

Now you can store your encrypted data in the `.env` file and use it securely throughout your application.

## Disclaimer

I am by no means a security expert. I am not saying this is a secure way to store passwords or sensitive information. What I am saying is that if you are someone like me who works in a large manufacturing company and you manage servers that are behind a locked down firewall and your goal is hide your password or service account password from any would be "hackers" in your company who happen to get access to the same server... this will probably do the trick. Of course all the same security tips apply such as **NEVER** expose your `.env` file anywhere public even if the password is a huge a** integer. Happy programming 😁