docs> sphinx-quickstart

docs> sphinx-apidoc -o ./source ../src

docs> .\make.bat html

rm -r /var/www/docs/
cp -r /root/artworks-server/docs/build/html/ /var/www/docs