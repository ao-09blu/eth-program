// 秘密鍵の取得に使用する
const keythereum = require("keythereum");
const Buffer = require('buffer/').Buffer;


//var keyObject = keythereum.importFromFile("0x0b05fc1720fd4789f9245373e9c6e1f94e53183b", ".");
var keyObject = keythereum.importFromFile(process.argv[2], ".");
var privateKey = keythereum.recover(process.argv[3], keyObject);
process.stdout.setEncoding("binary");
//process.stdout.write(privateKey);
var privateKey_buf = Buffer.from(privateKey);
for(var i=0; i<privateKey_buf.length; i++){
    process.stdout.write(String(privateKey_buf[i]) + " ");
}
//process.stdout.write(String(privateKey_buf[0]));
