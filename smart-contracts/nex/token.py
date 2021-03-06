"""
Basic settings for an NEP5 Token
"""

from boa.interop.Neo.Storage import *

TOKEN_NAME = 'Quick pass'

TOKEN_SYMBOL = 'QPS'

TOKEN_DECIMALS = 8

# This is the script hash of the address for the owner of the token
# This can be found in ``neo-python`` with the walet open, use ``wallet`` command
TOKEN_OWNER = b'#\xba\'\x03\xc52c\xe8\xd6\xe5"\xdc2 39\xdc\xd8\xee\xe9'

TOKEN_CIRC_KEY = b'in_circulation'

TOKEN_TOTAL_SUPPLY = 10000000 * 100000000  # 10m total supply * 10^8 ( decimals)

TOKEN_INITIAL_AMOUNT = 2500000 * 100000000  # 2.5m to owners * 10^8

# for now assume 1 dollar per token, and one neo = 40 dollars * 10^8
#TOKENS_PER_NEO = 40 * 100000000
TOKENS_PER_NEO = 40 * 100000000

# for now assume 1 dollar per token, and one gas = 20 dollars * 10^8
TOKENS_PER_GAS = 20 * 100000000

def add_to_circulation(ctx, amount):
    """
    Adds an amount of token to circlulation

    :param amount: int the amount to add to circulation
    """

    current_supply = Get(ctx, TOKEN_CIRC_KEY)

    current_supply += amount
    Put(ctx, TOKEN_CIRC_KEY, current_supply)
    return True


def get_circulation(ctx):
    """
    Get the total amount of tokens in circulation

    :return:
        int: Total amount in circulation
    """
    return Get(ctx, TOKEN_CIRC_KEY)
