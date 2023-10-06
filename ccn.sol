pragma solidity >=0.5.16;

//配列を返す&入力できるように
pragma experimental ABIEncoderV2;

contract Greeter {
    //必要な情報の宣言

    //コンテンツ情報の登録
    struct Contents_info{
        string name; //コンテンツ名
        address producer; //コンテンツの配信者のアドレス
        uint[] router_ID;
        string[] keyword;
        bool flag;
        uint pri;
    }
    //コンテンツ配信者の登録
    struct Producer{
        string Pname;
        address ip_add;
    }
    struct Router{
        uint RouterID;
        string[] neighbor; 
    }
    //コンテンツの名前に対して情報を登録する手法に変更
    struct Contents_key{
        address producer;
        uint[] router_ID;
        string[] keyword;
    }

    //二次元配列の宣言
    uint[][] public neighbor_array = new uint[][](0);//隣接行列
    string[] public ip_addr;//ipaddr配列





    Contents_info[] public contents_list;//contents_infoの配列宣言
    mapping(address=>Router) public Link_DB;
    uint public ID = 0;
    //関数

    //コンテンツの登録
    function regist_content(string memory _name, uint[] memory _routerID, string[] memory _keyword, bool _flag) public returns(uint){
        uint id = contents_list.push(Contents_info({
            name: _name,
            producer: msg.sender,
            router_ID: _routerID,
            keyword: _keyword,
            flag: _flag,
            pri: 3
        }));
        return (id-1);
    }

    function regist_router(string memory _IPadd) public {
        //新しいルータのために隣接行列を追加
        neighbor_array.push(new uint[](ID));
        for(uint i=0; i<=ID; i++){//それぞれの配列を1づつ長くする
            neighbor_array[i].push(0);
        }
        Link_DB[msg.sender].RouterID = ID;
        ip_addr.push(_IPadd);
        ID = ID + 1;
    }

    function regist_neigbor(uint[] memory _neighbor)public{
        uint router_id = Link_DB[msg.sender].RouterID;
        for (uint i=0; i < _neighbor.length; i++){
            if( neighbor_array[router_id][i] != _neighbor[i] ){//更新があった場合
                neighbor_array[router_id][i] = _neighbor[i];//neighbor情報更新
                neighbor_array[i][router_id] = _neighbor[i];//通信相手の情報も更新
            }
        }
    }

    function show_router() view public returns (uint){
        return Link_DB[msg.sender].RouterID;
    }


    function show_contents() view public returns (Contents_info[] memory) {
        uint list_length = contents_list.length;
        Contents_info[] memory content_now = new Contents_info[](list_length);
        content_now = contents_list;
        return content_now;
    }

    function show_networks() view public returns (uint[][] memory){
        uint[][] memory networks = new  uint[][](neighbor_array.length);
        for(uint i=0; i<neighbor_array.length; i++){
            networks[i] = new uint[](neighbor_array[i].length);
            for(uint j=0; j<neighbor_array[i].length; j++){
                networks[i][j] = neighbor_array[i][j];
            }
        }
        return networks;
    }

    function return_networks() view public returns (uint[][] memory){
        return neighbor_array;
    }

    function return_ipadd() view public returns (string[] memory){
        uint list_length = ip_addr.length;
        string[] memory return_list = new string[](list_length);
        return_list = ip_addr;
        return return_list;
    }

    function return_sender() view public returns (address){
        return msg.sender;
    }

    function return_nowID() view public returns (uint){
        return ID;
    }
}
