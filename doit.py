import numpy as np
import sklearn.cluster
import distance

words = "YOUR WORDS HERE".split(" ") #Replace this line

with open('_data_workordertitles', 'r') as f:
    raw_lines = f.readlines()

titles = [x.strip() for x in raw_lines]
titles = [x.split() for x in titles]
# import pdb; pdb.set_trace()

def words_to_sentence(words):
    return " ".join(words)

def process_words(words):
    words = np.asarray(words) #So that indexing with a list will work
    lev_similarity = -1*np.array([[distance.levenshtein(w1,w2) for w1 in words] for w2 in words])

    affprop = sklearn.cluster.AffinityPropagation(affinity="precomputed", damping=0.5)
    affprop.fit(lev_similarity)
    for cluster_id in np.unique(affprop.labels_):
        exemplar = words[affprop.cluster_centers_indices_[cluster_id]]
        cluster = np.unique(words[np.nonzero(affprop.labels_==cluster_id)])
        cluster_str = " | ".join([" ".join(y) for y in [x for x in cluster]])
        print("{%s} -> [%s]" % (words_to_sentence(exemplar), cluster_str))


process_words(titles[:100])
