// SPDX-License-Identifier: MIT
pragma solidity >=0.4.0 <0.9.0;

contract LostStorage {
    address public myAddress;
    uint public myUint;

    function setAddress(address _address) public {
        myAddress = _address;
    }

    function setMyUint(uint _uint) public {
        myUint = _uint;
    }

}