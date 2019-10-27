import base64
import os

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from pymongo.encryption import ClientEncryption
from pymongo.encryption_options import AutoEncryptionOpts
from bson import binary, ObjectId
from bson.codec_options import CodecOptions

# Setup.
codec_opts = CodecOptions(uuid_representation=binary.STANDARD)

if "LOCAL_MASTERKEY_BASE64" not in os.environ or not os.path.exists(
        "key_uuid.txt"):
    raise Exception("Prerequisites not met. Run setup.py")

local_key = os.environ["LOCAL_MASTERKEY_BASE64"]
key_uuid = binary.Binary(base64.b64decode(
    open("key_uuid.txt", "r").read()), binary.UUID_SUBTYPE)

# Configure automatic encryption and ClientEncryption object.
kms_providers = {"local": {"key": binary.Binary(base64.b64decode(local_key))}}
schema_map = {
    "db.users": {
        "bsonType": "object",
        "properties": {
            "email": {
                "encrypt": {
                    "bsonType": "string",
                    "algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic",
                    "keyId": [key_uuid]
                }
            },
            "pwd": {
                "encrypt": {
                    "bsonType": "string",
                    "algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Random",
                    "keyId": [key_uuid]
                }
            }
        }
    },
    "db.posts": {
        "bsonType": "object",
        "properties": {
            "title": {
                "encrypt": {
                    "bsonType": "string",
                    "algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Random",
                    "keyId": "/user_id"
                }
            },
            "body": {
                "encrypt": {
                    "bsonType": "string",
                    "algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Random",
                    "keyId": "/user_id"
                }
            },
        }
    },
}
key_vault_client = MongoClient("mongodb://localhost")

encryption_opts = AutoEncryptionOpts(
    kms_providers,
    "db.keyvault",
    schema_map=schema_map,
    key_vault_client=key_vault_client,
    mongocryptd_bypass_spawn=True)

client = MongoClient("mongodb://dorisdb:27017/",
                     auto_encryption_opts=encryption_opts)

client_encryption = ClientEncryption(
    kms_providers, "db.keyvault", client, codec_opts)

def register(email, pwd):
    """
    Create a new user in the db.users collection.
    Encrypts the values of "email" and "pwd".
    Returns (<user_id>, <status message>)
    """
    try:
        result = client.db.users.insert_one({
            "_id": str(ObjectId()),
            "email": email,
            "pwd": pwd
        })
        client_encryption.create_data_key(
            "local", key_alt_names=[result.inserted_id])
        return (result.inserted_id, "Registered!")
    except DuplicateKeyError as e:
        return (None, "Error: User already exists")

def login(email, pwd):
    """
    Finds user from db.users collection.
    Queries by deterministically encrypted "email".
    Returns (<user_id>, <status message>)
    """
    result = client.db.users.find_one({"email": email})
    if result and result["pwd"] == pwd:
        return (result["_id"], "Logged in!")
    else:
        return (None, "Failed to log in.")


def create_post(user_id, title, body):
    """
    Creates a new post, auto encrypts title and body.
    """
    client.db.posts.insert_one({
        "user_id": user_id,
        "title": title,
        "body": body
    })

def get_posts(user_id):
    """
    Returns all of user's posts, after auto decryption.
    """
    return list(client.db.posts.find({"user_id": user_id}))

def delete_all_data (user_id):
    """
    Deletes posts, user info, and (most importantly) the
    associated encryption key for this user.
    """
    client.db.posts.delete_many ({"user_id": user_id})
    client.db.users.delete_one ({"  _id": user_id})
    key_vault_client.db.keyvault.delete_one ({"keyAltNames": user_id})