
from calendar import c
import IPython.display as ipd
import librosa
import librosa.display
import numpy as np
import pandas as pd
from scipy import stats



def getColumns():
    feature_sizes = dict(chroma_stft=12, chroma_cqt=12, chroma_cens=12,
                         tonnetz=6, mfcc=20, rmse=1, zcr=1,
                         spectral_centroid=1, spectral_bandwidth=1,
                         spectral_contrast=7, spectral_rolloff=1)
    moments = ('mean', 'std', 'skew', 'kurtosis', 'median', 'min', 'max')

    columns = []
    for name, size in feature_sizes.items():
        for moment in moments:
            it = ((name, moment, '{:02d}'.format(i+1)) for i in range(size))
            columns.extend(it)

    names = ('feature', 'statistics', 'number')
    columns = pd.MultiIndex.from_tuples(columns, names=names)

    return columns.sort_values()


def feature_stats(name, values, features):
        features[name, 'mean'] = np.mean(values, axis=1)
        features[name, 'std'] = np.std(values, axis=1)
        features[name, 'skew'] = stats.skew(values, axis=1)
        features[name, 'kurtosis'] = stats.kurtosis(values, axis=1)
        features[name, 'median'] = np.median(values, axis=1)
        features[name, 'min'] = np.min(values, axis=1)
        features[name, 'max'] = np.max(values, axis=1)



def ExtractFeatures(f):

    x, sr = librosa.load(f, sr=None, mono=True)
    print('Duration: {:.2f}s, {} samples'.format(x.shape[-1] / sr, x.size))

    features = pd.Series(index= getColumns(), dtype=np.float32, name=1)

    f = librosa.feature.zero_crossing_rate(x, frame_length=2048, hop_length=512)
    feature_stats('zcr', f, features)

    cqt = np.abs(librosa.cqt(x, sr=sr, hop_length=512, bins_per_octave=12,
                                 n_bins=7*12, tuning=None))
    assert cqt.shape[0] == 7 * 12
    assert np.ceil(len(x)/512) <= cqt.shape[1] <= np.ceil(len(x)/512)+1

    f = librosa.feature.chroma_cqt(C=cqt, n_chroma=12, n_octaves=7)
    feature_stats('chroma_cqt', f, features)
    f = librosa.feature.chroma_cens(C=cqt, n_chroma=12, n_octaves=7)
    feature_stats('chroma_cens', f, features)
    f = librosa.feature.tonnetz(chroma=f)
    feature_stats('tonnetz', f, features)

    del cqt
    stft = np.abs(librosa.stft(x, n_fft=2048, hop_length=512))
    assert stft.shape[0] == 1 + 2048 // 2
    assert np.ceil(len(x)/512) <= stft.shape[1] <= np.ceil(len(x)/512)+1
    del x

    f = librosa.feature.chroma_stft(S=stft**2, n_chroma=12)
    feature_stats('chroma_stft', f, features)

    f = librosa.feature.rms(S=stft)
    feature_stats('rmse', f, features)

    f = librosa.feature.spectral_centroid(S=stft)
    feature_stats('spectral_centroid', f, features)
    f = librosa.feature.spectral_bandwidth(S=stft)
    feature_stats('spectral_bandwidth', f, features)
    f = librosa.feature.spectral_contrast(S=stft, n_bands=6)
    feature_stats('spectral_contrast', f, features)
    f = librosa.feature.spectral_rolloff(S=stft)
    feature_stats('spectral_rolloff', f, features)

    mel = librosa.feature.melspectrogram(sr=sr, S=stft**2)
    del stft
    f = librosa.feature.mfcc(S=librosa.power_to_db(mel), n_mfcc=20)
    feature_stats('mfcc', f, features)

    features = features.to_frame().T
    print(features.shape)

    columns = ['mfcc', 'chroma_cens', 'tonnetz', 'spectral_contrast']
    columns.append(['spectral_centroid', 'spectral_bandwidth', 'spectral_rolloff'])
    columns.append(['rmse', 'zcr'])
    for column in columns:
        #ipd.display(features[column].head().style.format('{:.2f}'))
        print("features: ", features[column].head())
