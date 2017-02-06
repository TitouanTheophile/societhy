import pytest
from time import sleep

from core import wallet, keys
from core.blockchain_watcher import blockchain_watcher as bw
from core.utils import *

from models.user import users
from models.organization import OrgaDocument, organizations
from models.clients import eth_cli
from models.contract import contracts
from models.user import users

from tests.fixtures import *

from ethjsonrpc import wei_to_ether

def test_create_orga(miner):
	bw.run()
	mockTx(nb=1)
	while miner.refreshBalance() < 1:
		bw.waitBlock()

	test_orga = {"name": "basic_orga"}
	new_orga = Organization(contract='basic_orga', doc=test_orga, owner=miner)
	tx_hash = new_orga.deployContract(from_=miner, password='simon', args=["bite"])
	
	assert tx_hash != None
	bw.waitTx(tx_hash)
	sleep(1)
	assert new_orga["contract_id"] != None
	inserted_orga = organizations.find_one({"contract_id": new_orga["contract_id"]})
	assert inserted_orga != None
	assert inserted_orga.contract != None


def test_join(miner, testOrga):
	tx_hash = testOrga.join(miner, password="simon")
	assert tx_hash != None
	print('tx hash = ', tx_hash)
	bw.waitEvent('newMember')
	assert miner.get('name') in [member.get('name') for member in testOrga.getMemberList()]

def test_memberlist(testOrga):
	result = testOrga.getMemberList()
	assert len(result) == 1
	assert result[0].get('name') == 'miner'

def test_donate(miner, testOrga):
	tx_hash = testOrga.donate(miner, 1000, password="simon")
	assert tx_hash is not None
	bw.waitEvent("newDonation")
	assert testOrga.getTotalFunds() == 1000
	
def test_leave(miner, testOrga):
	tx_hash = testOrga.leave(miner, password='simon')
	assert tx_hash.startswith('0x')
	bw.waitEvent("memberLeft")

	assert miner.get('name') not in [member.get('name') for member in testOrga.getMemberList()]

def test_createproject(miner, testOrga):
	tx_hash = testOrga.createProject(miner, {}, password='simon')
	assert tx_hash.startswith('0x')
	bw.waitTx(tx_hash)

def test_destroyOrga(miner, testOrga):
	pass

