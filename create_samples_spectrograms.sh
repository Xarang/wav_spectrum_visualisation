PROGRAM_NAME=$0

test ! -d env && echo "$PROGRAM_NAME: could not find env directory to source into" && exit 2

cd env
source bin/activate
cd ..

SPECTROGRAMS_DIR=spectrograms
SAMPLES_DIR=samples

mkdir $SPECTROGRAMS_DIR 2>/dev/null

PLOTTING_PROGRAM=plotter/plot_csv.py
FILES=$(find $SAMPLES_DIR -name "*.wav")

for FILE in $FILES; do
    python3 $PLOTTING_PROGRAM $FILE
    mv *.wav.png $SPECTROGRAMS_DIR
done
