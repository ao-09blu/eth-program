pragma solidity >=0.5.16;

//配列を返す&入力できるように
pragma experimental ABIEncoderV2;

contract Greeter {
    //必要な情報の宣言
    //コンテンツ情報の登録
    struct Contents_Inf{
        address producer; //コンテンツの配信者のアドレス
        uint[] holder;//コンテンツホルダーのルータID
        string[] keyword;
    }
    //コンテンツ配信者の登録
    struct Producer{
        string Pname;
        address ip_add;
    }
    struct Router{//ルータ情報を保存
        uint RouterID;
        string[] content_URI;//所持しているコンテンツのURIの情報
        string[] neighbor;//接続ルータのIPアドレス??nodeID??
        uint[] hop_count;
    }
    mapping(string=>Contents_Inf) public content_array;//コンテンツ名でアクセスできるようにマッピング
    mapping(address=>Router) public Link_DB;//アドレスでアクセスできるようにマッピング
    uint public ID = 0;
    address[] R_add;//添字がルータID,中身がそのルータのaddress
    bool[] flag;
    uint[] hop; //ホップ数
    //関数

    //新規コンテンツの登録
    function regist_content(string memory _URI, uint[] memory _holder, string[] memory _keyword) public returns(uint){
        content_array[_URI].producer = msg.sender;
        content_array[_URI].holder = _holder;
        content_array[_URI].keyword = _keyword;
    }

    //新規ルータ追加
    function regist_router(string[] memory _URI, string[] memory _neighbor)public returns(uint){
        Link_DB[msg.sender].RouterID = ID;
        Link_DB[msg.sender].content_URI = _URI;
        Link_DB[msg.sender].neighbor = _neighbor;
        R_add.push(msg.sender);
        ID = ID + 1;
        return Link_DB[msg.sender].RouterID;
    }

    function update_router(string[] memory _URI, string[] memory _neighbor) public{
        Link_DB[msg.sender].content_URI = _URI;
        Link_DB[msg.sender].neighbor = _neighbor;
    }

    /*
    function show_contents() view public returns (Contents_info[] memory) {
        uint list_length = contents_list.length;
        Contents_info[] memory content_array = new Contents_info[](list_length);
        content_array = contents_list;
        return content_array;
    }
    */
}