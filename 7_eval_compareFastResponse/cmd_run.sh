# Run with id_file
python main.py --id_file ids.txt --token "{{token}}"
# Run with id
python main.py --id 358 359 362 --token "{{token}}"
python main.py --id 8532 8534 --token "{{token}}"

# Run with id_file and id
python main.py --id_file ids.txt --id 358 359 362 --token "{{token}}"


---

nohup python main.py --id_file ids.txt --token "{{token}}" > output.log 2>&1 &