sed -i -e 's/easyocr\=\=1\.7\.1/#\ Removed\ EasyOCR/g' requirements.txt
sed -i -e 's/import\ easyocr/#\ Removed\ EasyOCR/g' src/image_verification.py
sed -i -e 's/immich\_tiktok\_remover\.py/immich\_tiktok\_remover\.py\ \-\-avoid\-image\-recognition/g' run_docker.sh

echo "requirements.txt"
cat requirements.txt

echo "src/image_verification.py"
cat src/image_verification.py

echo "src/immich_tiktok_remover.py"
cat src/immich_tiktok_remover.py

echo "run_docker.sh"
cat run_docker.sh