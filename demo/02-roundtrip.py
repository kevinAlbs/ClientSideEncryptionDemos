from setup.roundtrip import *
# An example of automatic encryption and decryption.
# Requires MongoDB enterprise.
kms_providers = {"local": {"key": masterkey}}
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
    kms_providers,
    "demo.keyvault",
    schema_map=schema_map,
    mongocryptd_bypass_spawn=True)

coll_encrypted = MongoClient(auto_encryption_opts=encryption_opts).demo.coll
coll_unencrypted = MongoClient().demo.coll

coll_encrypted.insert_one({"name": "Doris", "ssn": "457-55-5462"})

print("find_one with auto decryption")
print (dumps(coll_encrypted.find_one({}, { "_id": 0})))

print("find_one without auto decryption")
print (dumps(coll_unencrypted.find_one({}, {"_id": 0})))