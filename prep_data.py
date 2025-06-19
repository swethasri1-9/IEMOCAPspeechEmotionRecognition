import os
from shutil import copyfile
import glob
import pandas as pd

def create_data_dir(pathData: str, pathDataOrig: str):
    """Generate directories for audio and image outputs
       Copy .wav files to audio subfolders based on emotion
       
    Args:
        pathData (str): path to the output root folder (e.g., '/kaggle/working/')
        pathDataOrig (str): path to the original IEMOCAP dataset (e.g., '/kaggle/input/iemocap-dataset/')
    """

    os.makedirs(pathData, exist_ok=True)
    pathAudio = os.path.join(pathData, 'audio')
    pathImage = os.path.join(pathData, 'image')
    os.makedirs(pathAudio, exist_ok=True)
    os.makedirs(pathImage, exist_ok=True)

    emotions = ['anger', 'happiness', 'neutral', 'sadness']
    csv_prefixes = {
        'anger': 'ang',
        'happiness': 'hap',
        'neutral': 'neu',
        'sadness': 'sad'
    }

    # Create subfolders for each emotion
    for emotion in emotions:
        pathAudioEmotion = os.path.join(pathAudio, emotion)
        pathImageEmotion = os.path.join(pathImage, emotion)
        os.makedirs(pathAudioEmotion, exist_ok=True)
        os.makedirs(pathImageEmotion, exist_ok=True)

    for emotion in emotions:
        print('Processing emotion:', emotion)
        
        csv_name = csv_prefixes[emotion] + '.csv'
        csv_path = f"/kaggle/input/emotion-csvs/{csv_name}"  # <-- adjust if your CSV path is different
        emotionFile = pd.read_csv(csv_path)
        
        if 'filenames' not in emotionFile.columns:
            emotionFilenames = emotionFile.iloc[:, 0]  # fallback to first column
        else:
            emotionFilenames = emotionFile['filenames']

        for filename_target in emotionFilenames:
            found = False
            for filename in glob.iglob(os.path.join(pathDataOrig, '**', filename_target + '.wav'), recursive=True):
                copyfile(filename, os.path.join(pathAudio, emotion, filename_target + '.wav'))
                found = True
                break
            if not found:
                print(f"⚠️  File not found: {filename_target}.wav")
