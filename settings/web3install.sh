#!/user/bin/bash
sudo apt update
sudo apt-get upgrade
pip install ipython
pip install web3==6.0.0b8
pip install "web3[tester]"
