# !/bin/bash
set -eu

# Network Namespaceの作成
sudo ip netns add server1
sudo ip netns add router
sudo ip netns add server2

# インターフェースの作成
# peer で指定した相手と接続関係になる
sudo ip link add name server1-veth1 type veth peer name router-veth1
sudo ip link add name router-veth2 type veth peer name server2-veth1

# インターフェースを各Namespaceに所属させる
sudo ip link set server1-veth1 netns server1
sudo ip link set router-veth1 netns router
sudo ip link set router-veth2 netns router
sudo ip link set server2-veth1 netns server2

# 各インターフェースへIPアドレスを付与
sudo ip netns exec server1 ip addr add 10.0.0.1/24 dev server1-veth1
sudo ip netns exec router ip addr add 10.0.0.254/24 dev router-veth1
sudo ip netns exec router ip addr add 10.0.1.254/24 dev router-veth2
sudo ip netns exec server2 ip addr add 10.0.1.1/24 dev server2-veth1

# 各インターフェースの起動
# lo には自動的に 127.0.0.1/8 が割り当てられます
sudo ip netns exec server1 ip link set server1-veth1 up
sudo ip netns exec router ip link set router-veth1 up
sudo ip netns exec router ip link set router-veth2 up
sudo ip netns exec server2 ip link set server2-veth1 up
sudo ip netns exec server1 ip link set lo up
sudo ip netns exec router ip link set lo up
sudo ip netns exec server2 ip link set lo up

# サーバーのデフォルトルートを設定＋ルーターでルーティングを有効化
sudo ip netns exec server1 ip route add 0.0.0.0/0 via 10.0.0.254
sudo ip netns exec server2 ip route add 0.0.0.0/0 via 10.0.1.254
sudo ip netns exec router sysctl -w net.ipv4.ip_forward=1
