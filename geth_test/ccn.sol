pragma solidity >=0.5.16;

//配列を返す&入力できるように
pragma experimental ABIEncoderV2;

contract Greeter {
    //必要な情報の宣言

    //コンテンツ情報の登録
    struct Contents_info{
        string name; //コンテンツ名
        address producer; //コンテンツの配信者のアドレス
        string URI; //コンテンツのURI(実際に検索するための文字列)
        string[] keyword;
    }
    //コンテンツ配信者の登録
    struct Producer{
        string Pname;
        address ip_add;
    }
    struct Router{
        uint RouterID;
        string[] content_URI;
        string[] neighbor; 
    }

    Contents_info[] public contents_list;//contents_infoの配列宣言
    mapping(address=>Router) public Link_DB;
    uint ID = 0;
    //関数

    //コンテンツの登録
    function regist_content(string memory _name, string memory _URI, string[] memory _keyword) public returns(uint){
        uint id = contents_list.push(Contents_info({
            name: _name,
            producer: msg.sender,
            URI: _URI,
            keyword: _keyword
        }));
        return (id-1);
    }

    function regist_router(string[] memory _URI, string[] memory _neighbor)public{
        Link_DB[msg.sender].RouterID = ID;
        Link_DB[msg.sender].content_URI = _URI;
        Link_DB[msg.sender].neighbor = _neighbor;
        ID = ID + 1;
    }

    function update_router(string[] memory _URI, string[] memory _neighbor) public{
        Link_DB[msg.sender].content_URI = _URI;
        Link_DB[msg.sender].neighbor = _neighbor;
    }

    function show_router() view public returns (uint){
        return Link_DB[msg.sender].RouterID;
    }

    function update_topology(string[] memory _URI, string[] memory _neighbor) public{
        
    }

    function show_contents() view public returns (Contents_info[] memory) {
        uint list_length = contents_list.length;
        Contents_info[] memory content_array = new Contents_info[](list_length);
        content_array = contents_list;
        return content_array;
    }
}