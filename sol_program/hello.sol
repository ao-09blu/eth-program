pragma solidity ^0.5.16;
contract HelloWorld{
    string public greeting;

    constructor() public{
        greeting = "Hello, world!";
    }

    function greet() view public returns (string memory){
        return greeting;
    }
}


