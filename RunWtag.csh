
python Wtag_Selector.py --filestr LooseWP --tau21Cut 0.6 --applyTheaCorr --type ttjets --isMC --applyHIPCorr --80x --applyElSF > & ttjets_selection.txt &
python Wtag_Selector.py --filestr LooseWP --tau21Cut 0.6 --applyTheaCorr --type data  --applyHIPCorr --80x --applyElSF > & data_selection.txt &

python Wtag_Plotter.py --filestr LooseWP --infile LooseWP --pre  
python Wtag_Plotter.py --filestr LooseWP --infile LooseWP   

python Wtag_Plotter.py --filestr LooseWP --infile LooseWP --pre  --Mudata
python Wtag_Plotter.py --filestr LooseWP --infile LooseWP   --Mudata

python Wtag_Plotter.py --filestr LooseWP --infile LooseWP --pre  --Eldata
python Wtag_Plotter.py --filestr LooseWP --infile LooseWP   --Eldata

