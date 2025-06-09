import ursa_bbs as bbs


def log(msg: str, *vals):
    print(msg, *vals)
    print()


def test_random_keypair():
    dpk, sk = bbs.generate_bls_keypair()
    pk = dpk.to_public_key(5)
    log("Public key:", pk, bytes(pk).hex())
    log("Secret key:", sk, bytes(sk).hex())


def test_seed_keypair():
    dpk, sk = bbs.generate_bls_keypair(seed=b"seed00001")
    pk = dpk.to_public_key(5)
    log("Public key:", pk, bytes(pk).hex())


def test_pre_hashed():
    dpk, sk = bbs.generate_bls_keypair()
    pk = dpk.to_public_key(5)
    log("Public key:", bytes(pk).hex())

    messages = [b"message 1", b"message 2", b"message 3", b"message 4", b"message 5"]

    hashed_messages = [bbs.hash_message(m) for m in messages]
    signature = bbs.sign_messages(hashed_messages, sk, pk, pre_hashed=True)
    log("Signature:", bytes(signature).hex())

    log(
        "Verify:", bbs.verify_signature(hashed_messages, signature, pk, pre_hashed=True)
    )


def test_signature():
    dpk, sk = bbs.generate_bls_keypair()
    pk = dpk.to_public_key(5)
    log("Public key:", bytes(pk).hex())

    messages = [b"message 1", b"message 2", b"message 3", b"message 4", b"message 5"]

    signature = bbs.sign_messages(messages, sk, pk)
    log("Signature:", bytes(signature).hex())

    log("Verify:", bbs.verify_signature(messages, signature, pk))


def test_blind_context():
    dpk, sk = bbs.generate_bls_keypair()
    pk = dpk.to_public_key(5)
    log("Public key:", bytes(pk).hex())

    signing_nonce = bbs.generate_signing_nonce()
    # log("Signing nonce:", signing_nonce.hex())

    link_secret = b"secret"
    context_messages = {0: link_secret}
    signature_blinding, context = bbs.create_blinding_context(
        context_messages, pk, signing_nonce
    )
    log("Blinding:", signature_blinding.hex())
    log("Context:", context.hex())

    messages = {1: b"message_1", 2: b"message_2", 3: b"message_3", 4: b"message_4"}

    blind_signature = bbs.sign_messages_blinded_context(
        messages, sk, pk, context, signing_nonce
    )
    log("Blind signature:", bytes(blind_signature).hex())

    signature = bbs.unblind_signature(blind_signature, signature_blinding)
    log("Unblinded signature:", bytes(signature).hex())

    all_messages = [link_secret] + [messages[i] for i in range(1, 5)]
    log("Verify:", bbs.verify_signature(all_messages, signature, pk))


def test_zkp():
    dpk, sk = bbs.generate_bls_keypair()
    pk = dpk.to_public_key(5)
    log("Public key:", bytes(pk).hex())

    messages = [b"message_1", b"message_2", b"message_3", b"message_4", b"message_5"]

    signature = bbs.sign_messages(messages, sk, pk)
    log("Signature:", bytes(signature).hex())

    verifier_nonce = bbs.generate_proof_nonce()
    # log("Verifier nonce:", verifier_nonce.hex())

    proof = bbs.create_proof(messages, [1, 3], pk, signature, verifier_nonce)
    log("Proof:", bytes(proof).hex())

    verify_messages = [messages[1], messages[3]]
    log("Verify:", bbs.verify_proof(verify_messages, [1, 3], pk, proof, verifier_nonce))


from collections.abc import Iterable

def flatten_and_encode(messages):
    result = []
    for m in messages:
        if isinstance(m, bytes):
            result.append(m)
        elif isinstance(m, str):
            result.append(m.encode('utf-8'))
        elif isinstance(m, Iterable):
            for s in m:
                if isinstance(s, bytes):
                    result.append(s)
                elif isinstance(s, str):
                    result.append(s.encode('utf-8'))
                else:
                    raise TypeError(f"Unsupported message type in inner iterable: {type(s)}")
        else:
            raise TypeError(f"Unsupported message type: {type(m)}")
    return result


def ursa_test():
    message1 = "Age: 43".encode()
    message2 = "Gender: Female".encode()
    msgs = [message1, message2]
    label = "My label".encode()

    messages = [msgs, label]
    messages = flatten_and_encode(messages)

    messages_len = len(messages)
    print(f"messages_len: {messages_len}")

    dpk, sk = bbs.generate_bls_keypair()
    pk = dpk.to_public_key(messages_len)
    log("Public key:", bytes(pk).hex())    

    signature = bbs.sign_messages(messages, sk, pk)
    log("Signature:", bytes(signature).hex())

    verifier_nonce = bbs.generate_proof_nonce()
    # log("Verifier nonce:", verifier_nonce.hex())

    proof = bbs.create_proof(messages, [0, 2], pk, signature, verifier_nonce)
    log("Proof:", bytes(proof).hex())

    verify_messages = [messages[0], messages[2]]
    log("Verify:", bbs.verify_proof(verify_messages, [0, 2], pk, proof, verifier_nonce))

    """
    proof = bbs.create_proof(messages, [0, 1, 2], pk, signature, verifier_nonce)
    log("Proof:", bytes(proof).hex())

    verify_messages = [messages[0], messages[1], messages[2]]
    log("Verify:", bbs.verify_proof(verify_messages, [0, 1, 2], pk, proof, verifier_nonce))
    """

import os

if __name__ == "__main__":
    #print(os.getcwd())
    # Full path of the currently running script
    print(os.path.abspath(__file__))
    
    test_random_keypair()
    print("---\n")
    test_seed_keypair()
    print("---\n")
    test_signature()
    print("---\n")
    test_pre_hashed()
    print("----\n")
    test_blind_context()
    print("----\n")
    test_zkp()

    print("----\n")
    print('\n ----- [Ursa test] -----')
    ursa_test()

"""
/content/...ursa_bbs_python/test.py

:
Verify: True

----


 ----- [Ursa test] -----
messages_len: 3
Public key: 95e0dbd0a7410a985295392b8aafcc5b37672427d23a659e0d6914d07eabe4f9b38cb1621210f41e45c11acb5a89349a059d49f9c57a45d0e853ed5c9368def5d8e6570e0c8b322a9457b50848bb5cb7ac7d3670d59083e29be7962c5b41ad48a313cbf407121ea01248114d80684a3fe55025125a5a021564218640645f0c3e8c59ce1931622e98f2ce79d2ab693a0a000000038206fc6bb35e06fcc06dd382fe9d12397e2a9450639238eea35664b44a777120fa7e9f865ddeb6bb0e2b0cb3b327e38e94629117e5b083e0d7f74adc01905da33ff36cfeb570789844168e160fffdd8b4f8dd877525024c6977afe2789eb26969493480f9060bdf51621756f38cbded2ce5b4f1b1fe933f778ddcd248e8682fdc697a71ae0ae1ab4abfe1103b7b92a73

Signature: 8ae355b4f064b798ad91c14c4d8ae36084011e4cc93717d985b2d67df0ea7034dd401c72ae05077a8e82ecd68d1a7165145969c0c9905ba3164fe23396d11526b39effb791f97ca222f422304c7050e0008aab21158277ce56e9a7090fc89150012b31253da6865946dedec05a84c1ce

Proof: 98d119d7e435f36f19a1d46a85ddad99ac6083eb25825321d0e5a9bbf6373eb2f7441826f6800f9209c57ccad57f223aa01ff04a177ac361b4d711729c9cd7bc5832955e894c2a8c5266284309a6e1a52c100290b3ec29d2c37568f0e6bca597ae22b96331843a3ffa5e08dbc2dd41c44282f7db6acec374015e82886fe4483657a2dfc6b428f411308e220a2d31c1ee000000748b257ec00e55b68803d027add073a54a360ec5aad0abf1d3f06ab2c0b0a38cb41abdd919e7de2c3baba996943faa607500000002342116a48575ec120868b9a2f6a6d89a109e7621dc09add936df6bf33da712410096491950c726d2abe2bee16d7ec80f4ed1f78ffcfe7d51f170955ce87bb009828e30df6e4239ea9f4092f5bc93cbff95e413e97a9f8fb245966a389f8c64772b6bf06feb20ff078a201429bbf292c5000000034736fa9195fc7d9c56166a20f5d57c1671a49a651e56679fe79e99351de9b6e92b6ff9c8bf5544e4eda6ccfe062c1c3b5b0ee64b71b14ab8a8138e42fa8f03ea12c52cac2623a5a253548c95ca13ca5bbf49732e1ff1eff23f7c66bf0dded0a6

Verify: True
"""