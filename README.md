## Setup ##
Download mongocryptd, which is included with the MongoDB enterprise download. Run it with `./mongocryptd`.

Install Python dependencies.
```
python -m pip install pymongo
python -m pip install "pymongo[encryption]"
```

Set a local masterkey in the environment for testing.
```
export LOCAL_DATAKEY_BASE64="base64 encoded 96 byte value"
```

`LOCAL_DATAKEY_BASE64` is your masterkey for testing locally (use AWS KMS in production). It needs to be a 96 byte base64 encoded value. For example, this could be generated with `openssl`:

```
export LOCAL_DATAKEY_BASE64="$(openssl rand -base64 96 | tr -d '\n')"
```

FAQ