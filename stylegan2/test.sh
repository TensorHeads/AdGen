for d in $(seq 1 100); do 
	stylegan2_pytorch  --generate --models_dir "./path_to_model_dir" --num_image_tiles 1 --results_dir "./path_to_generated_images"; 
	sleep 5; 
done;