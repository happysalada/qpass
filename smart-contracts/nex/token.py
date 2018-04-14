"""
Basic settings for an NEP5 Token
"""

from boa.interop.Neo.Storage import *

TOKEN_NAME = 'Quick pass'

TOKEN_SYMBOL = 'QPS'

TOKEN_DECIMALS = 8

# This is the script hash of the address for the owner of the token
# This can be found in ``neo-python`` with the walet open, use ``wallet`` command
<<<<<<< HEAD
#TOKEN_OWNER = b'S\xefB\xc8\xdf!^\xbeZ|z\xe8\x01\xcb\xc3\xac/\xacI)'
TOKEN_OWNER = b'\x03\x6d\xbb\xbe\x94\xfb\x07\x33\x33\x8e\xd4\x1f\x28\x4f\x0e\xde\xad\x22\xf9\xb0\x30\xf9\x8a\x86\x37\xed\x84\x14\x0e\x0f\x63\xfe\xfa'
=======
TOKEN_OWNER = b'#\xba\'\x03\xc52c\xe8\xd6\xe5"\xdc2 39\xdc\xd8\xee\xe9'
>>>>>>> 683be1f28dbac9b5d373abe1a4695067c7586ab8

TOKEN_CIRC_KEY = b'in_circulation'

TOKEN_TOTAL_SUPPLY = 10000000 * 100000000  # 10m total supply * 10^8 ( decimals)

TOKEN_INITIAL_AMOUNT = 2500000 * 100000000  # 2.5m to owners * 10^8

# for now assume 1 dollar per token, and one neo = 40 dollars * 10^8
#TOKENS_PER_NEO = 40 * 100000000
# stick 1:1 with NEO 
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
