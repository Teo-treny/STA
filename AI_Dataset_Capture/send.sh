#! /bin/sh
rm -rf archive.tar.gz
tar -czvf archive.tar.gz *
scp archive.tar.gz pi@192.168.1.119:~/Desktop/Teleop
