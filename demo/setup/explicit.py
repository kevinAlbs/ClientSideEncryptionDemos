# Explicitly encrypt and decrypt a value. Available in MongoDB Community.
from base64 import b64encode, b64decode
import os

from pymongo import MongoClient
from pymongo.encryption import ClientEncryption
from bson import binary
from bson.codec_options import CodecOptions

codec_opts = CodecOptions(uuid_representation=binary.STANDARD)

if "LOCAL_MASTERKEY_BASE64" not in os.environ or not os.path.exists("key_uuid.txt"):
    raise Exception("Prerequisites not met. Run 01-setup.py")

masterkey = binary.Binary(b64decode(os.environ["LOCAL_MASTERKEY_BASE64"]))
key_uuid = binary.Binary(b64decode(open("key_uuid.txt", "r").read()), binary.UUID_SUBTYPE)