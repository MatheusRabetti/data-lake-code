# Makes n number of copies of Les Miserables

INPUT=lesmiserables.txt
for num in $(seq 1 1000)
do
    bn=$(basename $INPUT .txt)
    cp $INPUT $bn$num.txt
done
