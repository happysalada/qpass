
from nex.txio import get_asset_attachments
from nex.token import *
from nex.crowdsale import *
from nex.nep5 import *
from boa.interop.Neo.Runtime import GetTrigger, CheckWitness , Log
from boa.interop.Neo.TriggerType import Application, Verification
from boa.interop.Neo.Storage import *


ctx = GetContext()
NEP5_METHODS = ['name', 'symbol', 'decimals', 'totalSupply', 'balanceOf', 'transfer', 'transferFrom', 'approve', 'allowance']


def Main(operation, args):
    """

    :param operation: str The name of the operation to perform
    :param args: list A list of arguments along with the operation
    :return:
        bytearray: The result of the operation
    """

    trigger = GetTrigger()

    # This is used in the Verification portion of the contract
    # To determine whether a transfer of system assets ( NEO/Gas) involving
    # This contract's address can proceed
    if trigger == Verification():

        # check if the invoker is the owner of this contract
        is_owner = CheckWitness(TOKEN_OWNER)

        # If owner, proceed
        if is_owner:

            return True

        # Otherwise, we need to lookup the assets and determine
        # If attachments of assets is ok
        attachments = get_asset_attachments()
        return can_exchange(ctx, attachments, True)

    elif trigger == Application():

        for op in NEP5_METHODS:
            if operation == op:
                return handle_nep51(ctx, operation, args)

        if operation == 'deploy':
            return deploy()

        elif operation == 'circulation':
            return get_circulation(ctx)

        # the following are handled by crowdsale

        elif operation == 'mintTokens':
            return perform_exchange(ctx)

        #elif operation == 'crowdsale_register':
            #return kyc_register(ctx, args)

        #elif operation == 'crowdsale_status':
            #return kyc_status(ctx, args)

        #elif operation == 'crowdsale_available':
            #return crowdsale_available_amount(ctx)

        elif operation == 'get_attachments':
            return get_asset_attachments()
        
        # qpass operations
        elif operation =='register_provider':
            address = args[0]
            name = args[1]
            return register_provider(address,name)
        elif operation =='register_device':
            address = args[0]
            provider_id = args[1]
            device_id = args[2]
            price = args[3]
            return register_device(address,provider_id,device_id,price)
        elif operation == 'get_total':
            type = args[0]
            return get_total(type)
        elif operation == 'get_storage_item':
            type = args[0]
            k = args[1]
            return get_storage_item(type,k)
        

        return 'unknown operation'

    return False


def get_total(type):
    context = GetContext()
    if type=='provider':
        total = Get(context, 'providercount')
    else:
        return False
    if len(total) == 0:
        total = 1
    else:
        total += 1
    return total

def deploy():
    """

    :param token: Token The token to deploy
    :return:
        bool: Whether the operation was successful
    """
    if not CheckWitness(TOKEN_OWNER):
        print("Must be owner to deploy")
        return False

    if not Get(ctx, 'initialized'):
        # do deploy logic
        Put(ctx, 'initialized', 1)
        Put(ctx, TOKEN_OWNER, TOKEN_INITIAL_AMOUNT)
        return add_to_circulation(ctx, TOKEN_INITIAL_AMOUNT)

    return False



