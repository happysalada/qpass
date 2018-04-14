<p align="center">
  <img
    src="http://neonexchange.org/img/NEX-logo.svg"
    width="125px;">

</p>
<h3 align="center">Qps ICO Smart Contract</h3>
<p align="center">Quick pass token official ICO Smart Contract</p>
<hr/>

Based on [Neo ICO Template](https://github.com/neonexchange/neo-ico-template) by Thomas Saunders of the NEX team - a good [reference article](https://medium.com/proof-of-working/how-to-build-an-ico-on-neo-with-the-nex-ico-smart-contract-template-1beac1ff0afd)

#### Requirements

Usage requires Python 3.6+

## Install

Before being able to use **neo-local**, you will need to install **Docker** and **Docker Compose**.

For MacOS and Windows users, both are bundled together:

- [Docker for Mac](https://docs.docker.com/docker-for-mac/install/)
- [Docker for Windows](https://docs.docker.com/docker-for-windows/install/)

For Linux users, you will have two seperate things to install:

1. [Docker (Community Edition)](https://store.docker.com/search?offering=community&operating_system=linux&q=&type=edition)
1. [Docker Compose](https://docs.docker.com/compose/install/#install-compose)

## Usage
#### deploy on your privatenet

deploy a privatenet first

MacOS or Linux users can make use of the **Makefile**:

```
make start
```

This will deploy a privatenet with a wallet with 100_000_000 NEO in a docker container
To access the wallet
`open wallet ./neo-privnet.wallet`
Enter password `coz`

To deploy the smart contract
`build /smart-contracts/qps_ico.py test 07 05 True False deploy qps`

Import the smart contract on your private net
`import contract /smart-contracts/qps_ico.avm test 07 05 True False`

Fill in the informations asked (name, email address...)

look for the contract hash
`contract search qps` (if you have named it qps)

then deploy it
`testinvoke 0x3fdc2dc4d26f98ab21b427270d284be9de70305b deploy []` (the hash value being the reference hash of your smart contract)

test the amount of funds in circulation
`testinvoke 0x3fdc2dc4d26f98ab21b427270d284be9de70305b circulation []`

```
make stop
```

## Block Explorer

View what is happening on your local blockchain: [http://localhost:4000](http://localhost:4000)

## Services

The [Docker Compose](https://docs.docker.com/compose/) stack is made up of the following
services:

- [neo-privatenet](https://hub.docker.com/r/cityofzion/neo-privatenet/) (consensus nodes)
- [neo-python](https://github.com/CityOfZion/neo-python) (development CLI)
- [neo-scan](https://github.com/CityOfZion/neo-scan) (block explorer)
- [postgres](https://hub.docker.com/_/postgres/) (database for neo-scan)
- (coming sooon) [neo-faucet](https://github.com/CityOfZion/neo-faucet)

## Troubleshooting

If you have an issue then please contact any of the
[contributors](https://github.com/CityOfZion/neo-local/graphs/contributors) on the
[NEO Discord](https://discord.cityofzion.io), or create an [issue](https://github.com/CityOfZion/neo-local/issues/new).

The **Makefile** is designed to simplify the setup process, however in doing so it can
obscure debugging. Thus it is recommended to run the Docker commands manually if you encounter
an error (as outlined in [usage](#usage)).

## Credit

[@slipo](https://github.com/slipo) used Docker Compose to create a simpler
local development environment (see [repo](https://github.com/slipo/neo-scan-docker)). His work was built
upon by the [NeoAuth](https://github.com/neoauth) team, who simplified the idea
further with the use of a wrapper and renamed the project.

It has now moved to be a part of CoZ and is actively maintained by the team - see
[contributors](https://github.com/CityOfZion/neo-local/graphs/contributors).

**Note** - this project sits on the shoulders of a number of great CoZ projects, and wouldn't be
possible without their hard work (see [services](#services)).

## License

[MIT](https://github.com/CityOfZion/neo-local/blob/master/LICENSE)
