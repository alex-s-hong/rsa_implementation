#! /bin/bash


cnt=1
while (("${cnt}"< 21)); do
	python3 main.py > ./outputs/output${cnt}.txt
	echo "output${cnt} has been created!"
	((cnt="${cnt}"+1 ))
done

echo "finished"

#python main.py > test.txt

