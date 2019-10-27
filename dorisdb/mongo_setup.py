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
masterkey = binary.Binary(base64.b64decode(local_key))
key_uuid = binary.Binary(base64.b64decode(open("key_uuid.txt", "r").read()), binary.UUID_SUBTYPE)