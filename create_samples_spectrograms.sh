PROGRAM_NAME=$0

test ! -d env && echo "$PROGRAM_NAME: could not find env directory to source into" && exit 2

cd env
source bin/activate
cd ..

SPECTROGRAMS_DIR=spectrograms
SPECTROGRAMS_F_DIR="$SPECTROGRAMS_DIR/f"
SPECTROGRAMS_M_DIR="$SPECTROGRAMS_DIR/m"
SAMPLES_DIR=samples
F_DIR="$SAMPLES_DIR/f"
M_DIR="$SAMPLES_DIR/m"

rm -rf spectrograms
mkdir $SPECTROGRAMS_DIR 2>/dev/null
mkdir $SPECTROGRAMS_F_DIR
mkdir $SPECTROGRAMS_M_DIR

PLOTTING_PROGRAM=plotter/plot_csv.py

FILES=$(find $F_DIR -name "*.wav")
for FILE in $FILES; do
    python3 $PLOTTING_PROGRAM $FILE
    mv *.wav.png $SPECTROGRAMS_F_DIR
done

FILES=$(find $M_DIR -name "*.wav")
for FILE in $FILES; do
    python3 $PLOTTING_PROGRAM $FILE
    mv *.wav.png $SPECTROGRAMS_M_DIR
done
