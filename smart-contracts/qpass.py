from qps.txio import *
from qps.token import *
from qps.nep5 import *
from qps.ico import mint,perform_exchange
from boa.interop.Neo.Runtime import GetTrigger, CheckWitness , Log
from boa.interop.Neo.TriggerType import Application, Verification
from boa.interop.Neo.Storage import Get,Put,GetContext,Delete

context = GetContext()
NEP5_METHODS = ['name', 'symbol', 'decimals', 'totalSupply', 'balanceOf', 'transfer', 'transferFrom', 'approve', 'allowance']

"""
#deploy NEP5-based QPS Token
#don't forget to change TOKEN_OWNER in qps/token.py with token's owner hash key
testinvoke 3f50d55c3a4e31288bc200ca6663701744996908 deploy []

#inspect circulation
testinvoke 3f50d55c3a4e31288bc200ca6663701744996908 circulation []

#mint QPS tokens (accepting only GAS)
testinvoke 3f50d55c3a4e31288bc200ca6663701744996908 mintTokens [] --attach-gas=10
import token 3f50d55c3a4e31288bc200ca6663701744996908

#register a smart lock
testinvoke 3f50d55c3a4e31288bc200ca6663701744996908 register_smart_lock ['AGzRsaa21AP14YNpJ6feyhZscrjHGtbKxn','192.168.1.1','owner_name','property_name','2000']

#make a deposit
testinvoke 3f50d55c3a4e31288bc200ca6663701744996908 make_deposit ['AR8jfZDgdCbGattRN2JDWQFeurrkAiJnHZ','192.168.0.1','1','2']

#authorization to the Smart LOCK
testinvoke 3f50d55c3a4e31288bc200ca6663701744996908 authorize_lock ['AR8jfZDgdCbGattRN2JDWQFeurrkAiJnHZ','192.168.0.1']
testinvoke 3f50d55c3a4e31288bc200ca6663701744996908 authorize_unlock ['AR8jfZDgdCbGattRN2JDWQFeurrkAiJnHZ','192.168.0.1']

#release a deposit
testinvoke 3f50d55c3a4e31288bc200ca6663701744996908 release_deposit ['AR8jfZDgdCbGattRN2JDWQFeurrkAiJnHZ','192.168.0.1','1','2']

"""

def Main(operation, args):
    """

    :param operation: str The name of the operation to perform
    :param args: list A list of arguments along with the operation
    :return:
        bytearray: The result of the operation
    """

    trigger = GetTrigger()
    if trigger == Verification():
        # check if the invoker is the owner of this contract
        is_owner = CheckWitness(TOKEN_OWNER)

        # If owner, proceed
        if is_owner:

            return True

        return False
    elif trigger == Application():
        for op in NEP5_METHODS:
            if operation == op:
                return handle_nep51(context, operation, args)
        if operation == 'deploy':
            return deploy()
        elif operation == 'circulation':
            return get_circulation(context)
        elif operation == 'mintTokens':
            return mint(context)
        elif operation == 'get_attachments':
            return get_asset_attachments()
        # qpass operations
        elif operation =='register_smart_lock':
            address = args[0]
            ip_address = args[1]
            owner_name = args[2]
            room_name = args[3]
            price = args[4]
            return register_smart_lock(address,ip_address,owner_name,room_name,price)
        elif operation =='make_deposit':
            address = args[0]
            device_id = args[1]
            start_date = args[2]
            end_date = args[3]
            return make_deposit(address,device_id,start_date,end_date)
        elif operation =='authorize_lock':
            address = args[0]
            device_id = args[1]
            return authorize_lock(address,device_id)
        elif operation == 'authorize_unlock':
            address = args[0]
            device_id = args[1]
            return authorize_unlock(address,device_id)
        elif operation =='release_deposit':
            address = args[0]
            device_id = args[1]
            return release_deposit(address,device_id)

        return 'unknown operation'
    return False


def deploy():
    """

    :param token: Token The token to deploy
    :return:
        bool: Whether the operation was successful
    """
    if not CheckWitness(TOKEN_OWNER):
        print("Must be owner to deploy")
        return False

    if not Get(context, 'initialized'):
        # do deploy logic
        Put(context, 'initialized', 1)
        Put(context, TOKEN_OWNER, TOKEN_INITIAL_AMOUNT)
        return add_to_circulation(context, TOKEN_INITIAL_AMOUNT)

    return False

def register_smart_lock(address,smart_lock_ip,owner_name,room_name,price):
    if not CheckWitness(address):
        return False
    Log('Registering Smart LOCK')
    Put(context, smart_lock_ip, address)

    key = concat(smart_lock_ip,'/price')
    Put(context, key, price)

    key = concat(smart_lock_ip,'/owner')
    Put(context, key, owner_name)

    key = concat(smart_lock_ip,'/room')
    Put(context, key, room_name)

    return True

def make_deposit(address,smart_lock_ip,start_date,end_date):
    if not CheckWitness(address):
        return False
    deposit = Get(context,concat(smart_lock_ip, '/deposit'))
    if (deposit != 0):
        Notify("Smart Lock still has a deposit")
        return False
    from_balance = Get(context, address)
    price = Get(context, concat(smart_lock_ip, '/price'))
    if (price == 0):
        Notify("Wrong Smart LOCK")
        return False
    if from_balance < price:
        print("Insufficient tokens for the deposit")
        return False
    balance = from_balance - price
    Put(context, address, balance)
    Put(context,concat(smart_lock_ip, '/deposit'),price)
    Put(context,concat(smart_lock_ip, '/permission'),address)


    Log("deposit completed")



    return True

def release_deposit(address,smart_lock_ip):
    if not CheckWitness(address):
        return False
    Log('Releasing Deposit')
    deposit = Get(context,concat(smart_lock_ip, '/deposit'))
    if (deposit != 0):
        Notify("No deposit on Smart Lock")
        return False
    owner_address = Get(context,concat(smart_lock_ip))
    owner_balance = Get(context, owner_address)
    owner_balance_with_deposit = owner_balance+deposit

    Put(context,owner_address,owner_balance_with_deposit)

    Delete(context, concat(smart_lock_ip, '/deposit'))
    Log('Deposit has been released!')
    return True

def authorize_lock(address, smart_lock_ip):
    if not CheckWitness(address):
        return False
    authorized_address = Get(context,concat(smart_lock_ip, '/permission'))
    if (authorized_address == 0):
        Notify("No Deposit has been found on this Smart LOCK")
        return False
    if address==authorized_address:
        message = concat("LOCK01/",smart_lock_ip)
        Notify(message)
        return True
    else:
        Notify("You have no permission!")
        return False

def authorize_unlock(address, smart_lock_ip):
    if not CheckWitness(address):
        return False
    authorized_address = Get(context,concat(smart_lock_ip, '/permission'))
    if (authorized_address == 0):
        Notify("No Deposit has been found on this Smart LOCK")
        return False
    if address==authorized_address:
        message = concat("UNLOCK02/",smart_lock_ip)
        Notify(message)
        return True
    else:
        Notify("You have no permission!")
        return False


"""
def register_provider(address,provider_name):
    if not CheckWitness(address):
        Log("Owner argument is not the same as the sender")
        return False
    Log('Registering Provider')
    count = get_total("provider")
    hex = count+48
    Log('Provider ID :')
    Log(hex)
    key = concat('provider/',hex)
    Put(context, key, address)

    k = concat(key, '/name')
    Put(context, k, provider_name)

    Put(context, 'providercount',count)
    Log('Registering Provider - DONE')
    return True




def register_device(address,provider_id,device_ip,price):
    if not CheckWitness(address):
        Log("Owner argument is not the same as the sender")
        return False
    count = get_total("device")
    hex = count+48
    key = concat('device/',hex)
    Put(context, key, device_ip)

    k = concat(key, '/provider')
    Put(context, k, provider_id)

    k = concat(key, '/price')
    Put(context, k, price)

    Put(context, 'devicecount',count)
    return True



"""
