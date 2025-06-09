package main

import (
	"crypto/rand"
	"crypto/sha256"
	"encoding/hex"
	"fmt"

	"github.com/agl/pond/bbssig"
)

func log(msg string, vals ...interface{}) {
	fmt.Println(msg, vals)
	fmt.Println()
}

func flattenAndHash(messages [][]byte) [][]byte {
	var hashed [][]byte
	for _, m := range messages {
		h := sha256.New()
		h.Write(m)
		hashed = append(hashed, h.Sum(nil))
	}
	return hashed
}

// GenerateRandomHex generates a secure random hex string of n bytes
func GenerateRandomHex(n int) string {
	b := make([]byte, n)
	_, err := rand.Read(b)
	if err != nil {
		panic(err)
	}
	return hex.EncodeToString(b)
}

func main() {
	// Flatten and encode messages
	randomLabel := "__label__[start] " + GenerateRandomHex(8) + " __label__[end]"

	messages := [][]byte{
		[]byte("Age: 43"),
		[]byte("Gender: Female"),
		[]byte(randomLabel),
	}

	dpk, err := bbssig.GenerateGroup(rand.Reader) // priv, _
	if err != nil {
		fmt.Println("Key generation failed:", err)
		return
	}
	group := dpk.Group // priv.Group
	member, err := dpk.NewMember(rand.Reader)
	if err != nil {
		fmt.Println("Member creation failed:", err)
		return
	}

	hashedMsgs := flattenAndHash(messages)
	fmt.Println("messages_len:", len(messages))

	// Sign the first message as a demonstration
	sig, err := member.Sign(rand.Reader, hashedMsgs[0], sha256.New())
	if err != nil {
		fmt.Println("Signing failed:", err)
		return
	}
	fmt.Printf("Signature: %x\n", sig)

	if group.Verify(hashedMsgs[0], sha256.New(), sig) {
		fmt.Println("Verify: true")
	} else {
		fmt.Println("Verify: false")
	}

	// Tamper check:  flip the least significant bit of the hash of the message, and check the signature (and which should fail).
	hashedMsgs[0][1] ^= 0x01
	if !group.Verify(hashedMsgs[0], sha256.New(), sig) {
		fmt.Println("Tampered signature failed as expected")
	}
	// Flip it back and check again (and which should be successful).
	hashedMsgs[0][1] ^= 0x01

	// Open signature
	tag, ok := dpk.Open(sig)
	if ok {
		fmt.Printf("Signature opened okay.\nTag: %x\n", tag)
	}

	// do another signing
	h := sha256.New()
	for _, m := range messages {
		h.Write(m)
	}
	hashmsg := h.Sum(nil)

	fmt.Printf("Message: %s\n", messages)

	sig, err = member.Sign(rand.Reader, hashmsg, h)

	if err == nil {
		fmt.Printf("Message signed okay: %x\n", sig)
	}

	if group.Verify(hashmsg, h, sig) {
		fmt.Printf("Signature verified okay\n")
	}

	hashmsg[1] ^= 0x01
	if !group.Verify(hashmsg, h, sig) {
		fmt.Printf("Signature failed okay\n")
	}
	hashmsg[1] ^= 0x01

	tag, ok = dpk.Open(sig)
	if ok {
		fmt.Printf("Signature opened okay.\n\nTag: %x\n", tag)
	}

}

/*
go mod init ursa
go mod tidy
go run main.go

% go run main.go
messages_len: 3
Signature: 59a12ca7dfbf4d766fb96267e3240b99b1ca78c8fbeee3df8407244458bc016646ae7c14e147f519e26326fb224f422523e46042eb44045bcd1ff43d733042190091ef41737d0166bb3e1b528602a18cd2f70525e6cd8247e5b05b11aab7cb6a09aba692eaf0f5f243e9ffeebd3f4b641cabc71ca3b614bede0dfe690b4cb6e9124d604066d118ae424d8ca0183b3d60ec3aaaca96dbfe3a0df3f489e8eff9f043f0ed5de6d5898e0736ff543c8c2fb217c9bd856ccde7ccc2b41bc3f7ede9ae4a03d9ae6ec7af8a94d1c829777644a336d89f9f77605ae6650c5330900dc79c42828b6fd6f7402bcd37e688aea76b8a1614d885d60a7bd066a51bf3e2f59df37f0e06a4d64c96d78538bc0d158fe7789ddbb61f12ee033996ebb98c282c361a75588931bfc94a3251b50f286b6187bdc69c3a3cc577094502bd5af25ebf8d98320581d8cd7f375ee6504ec3253f319034555941db1e62747742481c1a55e5dd30209d35c9d7ba85a1c433dd54a0b667058de264dffee074746fcc077c8c1bb2
Verify: true
Tampered signature failed as expected
Signature opened okay.
Tag: 06810af2f00cd32251acfb37c618cffc59683782ac13a21b49e6f229f6a377de14c23c62bc808a7fad5bbbd83df9b8d20f35e783580c4599484b131ed9ce09cb
Message: [Age: 43 Gender: Female __label__[start] 7119c1b7046995de __label__[end]]
Message signed okay: 4b6f334f17d44b5e5244de6a77d43eb456c39d85fb962545ede749f597877f43370643fd9b25aaf1f6a5237a60b48ecf2667ff3364e7ca39dc536dc8e95ad722583294fe133c4d97feacc60da350538b8650d39e66311284b5ba4b6e436962e626aa213a58c9a859e83aa37b65991ec3e60c8bf82c150c1626f11c79a179f6291d6a375d7f1fcb69dff405b82ccdea742304a5a07c7c3dc02629a6418a25ec0a8c8d501a8b6237eedb12058842ce68be410ac7a9978c6efd0374a52fba305d936d113f5b0a7488bfd8475552e996de7426c129c63c0733af8e1086395ece8deb84aa34c7f69c87677f36bf18a7e01016722769dc74a6b99ba8130779e0139e122744228c025477534f015b9b64c5c6e2992d6cb5980f0e098e71a8b4b4c2af5750fc414982d07517c4cca310b7876ff6e4e9d92b97f516625043447e1e35e294266d8c6cc5884a6e7d0be3236019a99259dbb49d2ece457b6ca40d4208bbb4f667861f0b88941726fc93ec5de5d2ed7302b0dbb5f55db8602906d12678f768e8
Signature verified okay
Signature failed okay
Signature opened okay.

Tag: 06810af2f00cd32251acfb37c618cffc59683782ac13a21b49e6f229f6a377de14c23c62bc808a7fad5bbbd83df9b8d20f35e783580c4599484b131ed9ce09cb

*/
