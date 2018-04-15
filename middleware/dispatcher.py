
import os
import threading
import json
import time
from queue import Queue
import argparse
import sys
import binascii
from logzero import logger
from functools import wraps
from twisted.internet import reactor, task, endpoints
from twisted.web.server import Request, Site
from klein import Klein, resource

# Allow importing 'neo' from parent path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, parent_dir)

from neocore.UIntBase import UIntBase
from neocore.UInt256 import UInt256

from neo.Core.State.StorageKey import StorageKey
from neo.Network.NodeLeader import NodeLeader
from neo.Core.Blockchain import Blockchain
from neo.Implementations.Blockchains.LevelDB.LevelDBBlockchain import LevelDBBlockchain
from neo.Implementations.Notifications.LevelDB.NotificationDB import NotificationDB
from neo.Settings import settings

from neo.Network.api.decorators import json_response, gen_authenticated_decorator, catch_exceptions

from neo.Implementations.Wallets.peewee.UserWallet import UserWallet
from neo.Prompt.Commands.Invoke import InvokeContract, TestInvokeContract, test_invoke
from neo.contrib.smartcontract import SmartContract

import urllib.request


# setup the protocol to be used
PROTOCOL_CONFIG = os.path.join(parent_dir, "protocol.privnet.json")
# Setup the smart contract instance
smart_contract = SmartContract("0b93cde1096433b2d1d9ddf74f85a7c6e266c4dc")


@smart_contract.on_notify
def sc_notify(event):
    logger.info("SmartContract Runtime.Notify event: %s", event)

    # Make sure that the event payload list has at least one element.
    if not len(event.event_payload):
        return

    # The event payload list has at least one element. As developer of the smart contract
    # you should know what data-type is in the bytes, and how to decode it. In this example,
    # it's just a string, so we decode it with utf-8:
    logger.info("- payload part 1: %s", event.event_payload[0].decode("utf-8"))

    if 'LOCK01' in event.event_payload[0].decode("utf-8"):
        ip_address = event.event_payload[0].decode("utf-8").split('/')[1]
        contents = urllib.request.urlopen("http://"+ip_address+"/on").read()
    if 'UNLOCK02' in event.event_payload[0].decode("utf-8"):
        ip_address = event.event_payload[0].decode("utf-8").split('/')[1]
        contents = urllib.request.urlopen("http://"+ip_address+"/off").read()

#
# Custom code that runs in the background
#
def custom_background_code():
    """ Custom code run in a background thread. Prints the current block height.
    This function is run in a daemonized thread, which means it can be instantly killed at any
    moment, whenever the main thread quits. If you need more safety, don't use a  daemonized
    thread and handle exiting this thread in another way (eg. with signals and events).
    """
    while True:
        logger.info("Block %s / %s", str(Blockchain.Default().Height), str(Blockchain.Default().HeaderHeight))

        time.sleep(15)




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", action="store", help="Config file (default. %s)" % PROTOCOL_CONFIG,
                        default=PROTOCOL_CONFIG)
    args = parser.parse_args()
    settings.setup(args.config)

    logger.info("Starting api.py")
    logger.info("Config: %s", args.config)
    logger.info("Network: %s", settings.net_name)

    # Setup the blockchain
    blockchain = LevelDBBlockchain(settings.LEVELDB_PATH)
    Blockchain.RegisterBlockchain(blockchain)
    dbloop = task.LoopingCall(Blockchain.Default().PersistBlocks)
    dbloop.start(.1)
    NodeLeader.Instance().Start()

    # Disable smart contract events for external smart contracts
    settings.set_log_smart_contract_events(False)

    # Start a thread with custom code
    d = threading.Thread(target=custom_background_code)
    d.setDaemon(True)  # daemonizing the thread will kill it when the main thread is quit
    d.start()



    # Run all the things (blocking call)
    logger.info("Everything setup and running. Waiting for events...")
    reactor.run()
    logger.info("Shutting down.")




if __name__ == "__main__":
    main()