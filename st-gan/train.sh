python train_Donly.py --name=D0 --warpN=0 --pertFG=0.2 --group=final_model --size=128x128 --toIt 50000;
for w in {1..3}; do
	python train_STGAN.py --loadD=final_model/D0_warp0_it50000 --warpN=$w --group=final_model --size=128x128 --toIt 50000;
done
