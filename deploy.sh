rsync -r --progress backend    me:~/app/pastebin/
cd front
webpack
cd ..
rsync -r --progress front/dist   me:~/app/pastebin/front/