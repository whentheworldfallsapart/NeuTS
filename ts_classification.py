from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, recall_score, precision_score
import pickle, time
import numpy as np

def kappa(confusion_matrix):
    pe_rows = np.sum(confusion_matrix, axis=0)
    pe_cols = np.sum(confusion_matrix, axis=1)
    sum_total = sum(pe_cols)
    pe = np.dot(pe_rows, pe_cols) / float(sum_total ** 2)
    po = np.trace(confusion_matrix) / float(sum_total)
    return (po - pe) / (1 - pe)

feature_files = [
    './features/embedding_8100_ElectricDevices_cdtw', 
    './features/embedding_1000_ItalyPowerDemand_cdtw',
    './features/embedding_4400_UWaveGestureLibraryAll_cdtw']

labels_files = [
    './features/ElectricDevices_all_ts_label',
    './features/ItalyPowerDemand_all_ts_label',
    './features/UWaveGestureLibraryAll_all_ts_label']

distances_files = [
    './features/ElectricDevices_cdtw_distance_all_8100',
    './features/ItalyPowerDemand_cdtw_distance_all_1000',
    './features/UWaveGestureLibraryAll_cdtw_distance_all_4400'
]

features = pickle.load(open(feature_files[0], 'rb'))

labels = pickle.load(open(labels_files[0],'rb'))[0][:features.shape[0]]

distances = pickle.load(open(distances_files[0], 'rb'))

train_num = int(features.shape[0] * 0.2)

print(distances.shape)
knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(features[:train_num], labels[:train_num])
predicted_species = knn.predict(features[train_num:])

print("Embedding KNN:")
print('Accuracy:{}'.format(accuracy_score(
    labels[train_num:], predicted_species)))
cm_emb = confusion_matrix(labels[train_num:], predicted_species)
print('Kappa Value: {}'.format(kappa(cm_emb)))

train_distances = distances[:, :train_num]
indexs = np.argmin(train_distances, axis=1)
pred_labels = [labels[i] for i in indexs[train_num:]]
print("Distance KNN:")
print('Accuracy:{}'.format(accuracy_score(
    labels[train_num:], predicted_species)))
cm_g = confusion_matrix(labels[train_num:], pred_labels)
print('Kappa Value: {}'.format(kappa(cm_g)))

coverage_num = 0

for i in range(len(pred_labels)):
    predict_emb = list(predicted_species)
    if int(predict_emb[i]) == int(pred_labels[i]):
        coverage_num += 1
print('Coverage: {}'.format(float(coverage_num/len(pred_labels))))