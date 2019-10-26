# An example of automatic encryption and decryption. Requires MongoDB enterprise.
import base64
import os

from pymongo import MongoClient
from pymongo.encryption import ClientEncryption
from pymongo.encryption_options import AutoEncryptionOpts
from bson import binary
from bson.codec_options import CodecOptions

codec_opts = CodecOptions(uuid_representation=binary.STANDARD)

if "LOCAL_DATAKEY_BASE64" not in os.environ or not os.path.exists("key_uuid.txt"):
    raise Exception("Prerequisites not met. Run 01-setup.py")

local_key = os.environ["LOCAL_DATAKEY_BASE64"]
kms_providers = {"local": {"key": binary.Binary(base64.b64decode(local_key))}}
key_uuid = binary.Binary(base64.b64decode(open("key_uuid.txt", "r").read()), binary.UUID_SUBTYPE)
schema_map = {
    "demo.coll": {
        "bsonType": "object",
        "properties": {
            "ssn": {
                "encrypt": {
                    "bsonType": "string",
                    "algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic",
                    "keyId": [key_uuid]
                }
            },
        }
    }
}

encryption_opts = AutoEncryptionOpts(
    kms_providers, "demo.keyvault", schema_map=schema_map, mongocryptd_bypass_spawn=True)

client = MongoClient("mongodb://localhost:27017/",
                     auto_encryption_opts=encryption_opts)

# With our MongoClient configured, use it as you would an ordinary MongoClient.
db = client.demo
# Reset the collection
db.coll.drop()

db.coll.insert_one({"name": "Doris", "ssn": "457-55-5462"})
print ("Inserted into db.coll: %s" % db.coll.find_one())
print ("Proceed to 03-explicit.py")