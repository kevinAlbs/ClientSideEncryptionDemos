# Explicitly encrypt and decrypt a value. Available in MongoDB Community.
import base64
import os

from pymongo import MongoClient
from pymongo.encryption import ClientEncryption
from bson import binary
from bson.codec_options import CodecOptions

codec_opts = CodecOptions(uuid_representation=binary.STANDARD)

if "LOCAL_MASTERKEY_BASE64" not in os.environ or not os.path.exists("key_uuid.txt"):
    raise Exception("Prerequisites not met. Run 01-setup.py")

masterkey = binary.Binary(base64.b64decode(os.environ["LOCAL_MASTERKEY_BASE64"]))
kms_providers = {"local": {"key": masterkey}}
key_uuid = binary.Binary(base64.b64decode(open("key_uuid.txt", "r").read()), binary.UUID_SUBTYPE)
client = MongoClient("mongodb://localhost:27017/")
client_encryption = ClientEncryption(
    kms_providers, "demo.keyvault", client, codec_opts)

encrypted = client_encryption.encrypt ("123-45-6789", "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic", key_id=key_uuid)
print ("encrypted data: %s" % base64.b64encode(encrypted).decode("utf-8"))
print ("decrypted back to: %s" % client_encryption.decrypt (encrypted))