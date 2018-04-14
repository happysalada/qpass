"""
Settings for QPS Token
"""

from boa.interop.Neo.Storage import *

TOKEN_NAME = 'QPass'

TOKEN_SYMBOL = 'QPS'

TOKEN_DECIMALS = 8

# This is the script hash of the address for the owner of the token
TOKEN_OWNER = b'\x03\x6d\xbb\xbe\x94\xfb\x07\x33\x33\x8e\xd4\x1f\x28\x4f\x0e\xde\xad\x22\xf9\xb0\x30\xf9\x8a\x86\x37\xed\x84\x14\x0e\x0f\x63\xfe\xfa'

TOKEN_CIRC_KEY = b'in_circulation'

TOKEN_TOTAL_SUPPLY = 100000000 * 100000000  # 100m of Total Supply eg. 1B. QPS Token

TOKEN_INITIAL_AMOUNT = 25000000 * 100000000  # 25m contribute to the Lucky Guy (Owner)

# we're accepting GAS in 1 usd per 1 qps
TOKENS_PER_GAS = 20 * 100


# we're accepting GAS in 1 usd per 1 qps
TOKENS_PER_NEO = 40 * 100


def crowdsale_available_amount(ctx):
    """

    :return: int The amount of tokens left for sale in the crowdsale
    """

    in_circ = Get(ctx, TOKEN_CIRC_KEY)

    available = TOKEN_TOTAL_SUPPLY - in_circ

    return available


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
