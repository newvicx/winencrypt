import sys

import click
import pywintypes
import win32crypt



def abort_if_false(ctx: click.Context, _, value: bool):
    if not value:
        ctx.abort()


@click.group()
def winencrypt() -> None:
    pass


@click.command()
@click.option("--data", prompt=True, hide_input=True)
def encrypt(data: str) -> None:
    encrypted = win32crypt.CryptProtectData(data.encode())
    click.echo(click.style(int.from_bytes(encrypted, sys.byteorder), fg="green"))


@click.command()
@click.argument("data", type=click.INT)
@click.option(
    "--yes",
    is_flag=True,
    callback=abort_if_false,
    expose_value=False,
    prompt="Confirm to show value"
)
def decrypt(data: int) -> None:
    try:
        _, decrypted = win32crypt.CryptUnprotectData(
            data.to_bytes(
                (data.bit_length() + 7) // 8,
                byteorder=sys.byteorder
            )
        )
    except pywintypes.error as e:
        click.echo(click.style(f"Failed to decrypt data: {str(e)}", fg="red"))
    else:
        click.echo(click.style(decrypted.decode(), fg="green"))


winencrypt.add_command(encrypt)
winencrypt.add_command(decrypt)