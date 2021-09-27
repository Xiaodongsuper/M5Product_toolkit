
import numpy as np
import os
import heapq
from tqdm import tqdm
import argparse
import pickle
import json

def read_json(file):
    f = open(file, "r", encoding="utf-8").read()
    return json.loads(f)


def write_json(file, data):
    f = open(file, "w", encoding="utf-8")
    json.dump(data, f, indent=2, ensure_ascii=False)
    return

def read_pickle(filename):
    return pickle.loads(open(filename,"rb").read())

def write_pickle(filename,data):
    open(filename,"wb").write(pickle.dumps(data))
    return


def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--query_feature_path",type=str
    )
    parser.add_argument(
        "--gallery_feature_path",type=str
    )
    parser.add_argument(
        "--retrieval_results_path",type=str
    )
    parser.add_argument(
        "--v",action="store_true"
    )
    parser.add_argument(
        "--t",action="store_true"
    )
    parser.add_argument(
        "--i",action="store_true"
    )
    parser.add_argument(
        "--p",action="store_true"
    )
    parser.add_argument(
        "--a",action="store_true"
    )
    parser.add_argument(
        "--it",action="store_true"
    )
    parser.add_argument(
        "--itp",action="store_true"
    )
    parser.add_argument(
        "--max_topk",type=int,default=110
    )

    return parser.parse_args()


def read_feature(query_feature_txt):
    query_id = []
    query_feature=[]
    for each in tqdm(query_feature_txt):
        each_split = each.split(",")
        item_id = each_split[0]
        each_feature = [float(i) for i in each_split[1:]]

        query_id.append(item_id)
        query_feature.append(each_feature)
    return query_id,query_feature


if __name__ == '__main__':
    print()

    args=parse_args()

    save_path=args.retrieval_results_path
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    feature_type = []
    if args.v:
        feature_type.append("v")
    if args.t:
        feature_type.append("t")
    if args.i:
        feature_type.append("i")
    if args.p:
        feature_type.append("p")
    if args.a:
        feature_type.append("a")
    if args.it:
        feature_type.append("it")
    if args.itp:
        feature_type.append("itp")


    for each_feature_type in feature_type:

        query_dir = args.query_feature_path
        gallery_dir = args.gallery_feature_path

        save_file=open("{}/{}_feature_retrieval_id_list.txt".format(save_path,each_feature_type),"w")

        # new
        gallery_ids = np.load("{}/id.npy".format(gallery_dir))
        gallery_ids = np.hstack(gallery_ids)

        query_ids = np.load("{}/id.npy".format(query_dir))
        query_ids = np.hstack(query_ids)

        gallery_feature_np = np.load("{}/{}_feature_np.npy".format(gallery_dir, each_feature_type))
        print(gallery_feature_np.shape)

        query_feature_np = np.load("{}/{}_feature_np.npy".format(query_dir, each_feature_type))
        print(query_feature_np.shape)

        # query_id=query_id[:100]
        # query_feature_np=query_feature_np[:100]

        score_matrix = query_feature_np.dot(gallery_feature_np.T)
        max_topk = args.max_topk
        for q,each_score in tqdm(zip(query_ids,score_matrix)):
            max_index = heapq.nlargest(max_topk, range(len(each_score)), each_score.take)
            topk_item_id = gallery_ids[max_index]
            topk_item_id=[each_item_id for each_item_id in topk_item_id if each_item_id!=q]

            topk_item_id_str = ",".join(topk_item_id)
            save_file.write("{},{}\n".format(q, topk_item_id_str))
























