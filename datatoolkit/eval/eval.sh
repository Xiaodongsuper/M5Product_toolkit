python retrieval_unit_id_list.py \
  --query_feature_path ${QUERY_FEATURE_DIR} \
  --gallery_feature_path ${GALLERY_FEATURE_DIR} \
  --retrieval_results_path ${RETRIEVAL_RESULTS_DIR} \
  --max_topk 10 \
  --t


GT_file=product1m_product5m_id_label.json
python evaluate_unit.py \
  --retrieval_result_dir ${RETRIEVAL_RESULTS_DIR} \
  --GT_file ${GT_file} \
  --output_metric_dir ${OUTPUT_METRIC_DIR} \
  --t