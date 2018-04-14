from boa.interop.Neo.Blockchain import GetHeight
from boa.interop.Neo.Runtime import CheckWitness
from boa.interop.Neo.Action import RegisterAction
from boa.interop.Neo.Storage import Get, Put
from boa.builtins import concat
from nex.token import TOKENS_PER_GAS


from nex.txio import get_asset_attachments

def mint(ctx):
    attachments = get_asset_attachments()  # [receiver, sender, gas]
    current_balance = Get(ctx, attachments[1])
    print(current_balance)
    exchanged_tokens += attachments[2] * TOKENS_PER_GAS
    print(exchanged_tokens)
    # add it to the the exchanged tokens and persist in storage
    new_total = exchanged_tokens + current_balance
    Put(ctx, attachments[1], new_total)
    # update the in circulation amount
    result = add_to_circulation(ctx, exchanged_tokens)
    return True


def perform_exchange(ctx):
    """

     :param token:Token The token object with NEP5/sale settings
     :return:
         bool: Whether the exchange was successful
     """
    attachments = get_asset_attachments()  # [receiver, sender, gas]

    current_balance = Get(ctx, attachments[1])

    exchanged_tokens += attachments[2] * TOKENS_PER_GAS

    # add it to the the exchanged tokens and persist in storage
    new_total = exchanged_tokens + current_balance
    Put(ctx, attachments[1], new_total)

    # update the in circulation amount
    result = add_to_circulation(ctx, exchanged_tokens)

    return True

