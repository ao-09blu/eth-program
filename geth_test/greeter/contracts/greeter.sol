pragma solidity ^0.5.4;
contract greeter{
    string greeting;
    
    function greet(string memory _greeting)public {
        greeting=_greeting;
    }
    function getGreeting() public view returns(string memory) {
        return greeting;
    }
}
