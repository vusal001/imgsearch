from django.shortcuts import render
import numpy as np
from PIL import Image
from searchimg.feature_extractor import FeatureExtractor
from datetime import datetime
from .forms import Imageform
from pathlib import Path



# Read image features
fe = FeatureExtractor()
features = []
img_paths = []
for feature_path in Path("./static/feature").glob("*.npy"):
    features.append(np.load(feature_path))
    img_paths.append(Path("./static/img") / (feature_path.stem + ".jpg"))
features = np.array(features)




def index(request):
    if request.method == 'POST':
        file = request.FILES["query"]

        

        # Save query image
        img = Image.open(file)  # PIL image
        uploaded_img_path = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + str(file)
        img.save(uploaded_img_path)
        

        # Run search
        query = fe.extract(img = Image.open(uploaded_img_path))
        dists = np.linalg.norm(features-query, axis=1)  # L2 distances to features
        

        ids = np.argsort(dists)[:5]  # Top 30 results
        scores = [(dists[id], img_paths[id]) for id in ids]

        return render(request, 'index.html', {'scores': scores, 'query_path':uploaded_img_path, })
                               
    else:
        return render(request, 'index.html')

    



