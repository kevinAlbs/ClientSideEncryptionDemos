from setup.createkey import *

# Configure a ClientEncryption object to create datakeys.
kms_providers = {"local": {"key": masterkey}}
key_vault_client = MongoClient()
client_encryption = ClientEncryption(
    kms_providers, "demo.keyvault", key_vault_client, codec_opts)

key_uuid = client_encryption.create_data_key("local")

# Store the key id into a file for easy access.
open("key_uuid.txt", "w").write(b64encode(key_uuid).decode("utf-8"))
print("Created data key in demo.keyvault with UUID: %s" % key_uuid.hex())