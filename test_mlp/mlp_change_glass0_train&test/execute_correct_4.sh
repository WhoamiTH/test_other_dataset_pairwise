python train_correct.py file_name=../1_year_data/glass0_train_4.csv model_record_path=../1_year_result/model_1/ file_record_path=../1_year_result/record_1/ method_name=change_loss scaler_name=scaler_4.m pca=False pca_name=pca_4.m model_name=model_4/my_model.pkl
python test.py train_file_name=../1_year_data/glass0_train_4.csv test_file_name=../1_year_data/glass0_test_origin_4.csv model_record_path=../1_year_result/model_1/ file_record_path=../1_year_result/record_1/ method_name=change_loss scaler_name=scaler_4.m model_name=model_4/my_model.pkl record_name=validation_result_4.csv
