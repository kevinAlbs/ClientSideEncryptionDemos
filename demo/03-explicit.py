from setup.explicit import *

kms_providers = {"local": {"key": masterkey}}
client = MongoClient()
client_encryption = ClientEncryption(
    kms_providers, "demo.keyvault", client, codec_opts)

encrypted = client_encryption.encrypt(
    "123-45-6789",
    "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic",
    key_id=key_uuid)

print("encrypted data: %s" % b64encode(encrypted).decode("utf-8"))
print("decrypted back to: %s" % client_encryption.decrypt(encrypted))
