from base64 import b64encode, b64decode
import os

from pymongo import MongoClient
from pymongo.encryption import ClientEncryption
from pymongo.encryption_options import AutoEncryptionOpts
from bson.binary import Binary, UUID_SUBTYPE
import bson.json_util

if "LOCAL_MASTERKEY_BASE64" not in os.environ or not os.path.exists(
        "key_uuid.txt"):
    raise Exception("Prerequisites not met. Run 01-setup.py")

masterkey = Binary(b64decode(os.environ["LOCAL_MASTERKEY_BASE64"]))
key_uuid = Binary(b64decode(open("key_uuid.txt", "r").read()), UUID_SUBTYPE)

# Reset collection
MongoClient().demo.coll.drop()

def dumps (doc):
    return bson.json_util.dumps(doc, indent=4)