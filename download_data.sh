#! /bin/bash

# e.g. https://drive.google.com/file/d/1gg530dZeii_XwFb4BegmsubGzCGk1o9b/view?usp=drive_link
FILENAME="pytorch_resnet101.pth"
FILEID="1gg530dZeii_XwFb4BegmsubGzCGk1o9b"
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate "https://docs.google.com/uc?export=download&id=$FILEID" -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=$FILEID" -O $FILENAME && rm -rf /tmp/cookies.txt