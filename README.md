# Client-Side Encryption Demos #
This repository includes demonstrations to accompany the talk "Using Client-Side Encryption in MongoDB 4.2".

For more information about Client-Side Encryption, refer to the [MongoDB Manual](https://docs.mongodb.com/manual/core/security-client-side-encryption/).

## Setup ##
Download mongocryptd, which is included with the MongoDB enterprise download. Run it with `./mongocryptd`.

Install Python dependencies.
```
pip install pymongo
pip install "pymongo[encryption]"
pip install Flask
```

Set a local masterkey in the environment for testing.
```
export LOCAL_MASTERKEY_BASE64="base64 encoded 96 byte value"
```

`LOCAL_MASTERKEY_BASE64` is your masterkey for testing locally (use AWS KMS in production). It needs to be a 96 byte base64 encoded value. For example, this could be generated with `openssl`:

```
export LOCAL_MASTERKEY_BASE64="$(openssl rand -base64 96 | tr -d '\n')"
```

Use Python 3 to run demos.

Example output of scripts in `/demo`.
```
> cd demo
> python 01-setup.py
Created data key in demo.keyvault with UUID: e67ffcb003f84076b0031ed809c2b712
Proceed to 02-roundtrip.py
> python 02-roundtrip.py
Inserted into db.coll: {'_id': ObjectId('5db5d47b3cd5f3667fb83811'), 'name': 'Doris', 'ssn': '457-55-5462'}
Proceed to 03-explicit.py
> python 03-explicit.py
encrypted data: AeZ//LAD+EB2sAMe2AnCtxICu6XJXY2XmAfvUZkeNcDHBgOGizxVCMREhcshCnlIt+miL+oE6Yr+jCWa4194jCn9J68FfgbpIqHg8PQFGZW1PGE61o6KvmXuP7PyRPSLSZI=
decrypted back to: 123-45-6789
```

To run the demo webapp, set the hostname "dorisdb" to point to a host running mongod on port 27017. To refer to a local mongod, add the following to `/etc/hosts`
```
127.0.0.1 dorisdb
```

Then run:
```
cd dorisdb
python setup.py
FLASK_APP=./server.py flask run
# Open localhost:5000 in web browser.
```