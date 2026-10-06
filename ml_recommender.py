import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.neighbors import NearestNeighbors


def train_model(data):

    df = data.copy()

    features = [
        "Programme",
        "Discipline",
        "State Name",
        "District Name",
        "Mode"
    ]

    # Convert categorical data into numerical form
    encoder = OneHotEncoder(handle_unknown="ignore")

    X = encoder.fit_transform(
        df[features].astype(str)
    )

    # ML similarity model
    model = NearestNeighbors(
        n_neighbors=10,
        metric="cosine"
    )

    model.fit(X)

    return model, encoder, features


def get_recommendations(
    data,
    model,
    encoder,
    features,
    programme,
    discipline,
    state,
    district,
    mode
):

    user_data = pd.DataFrame([{
        "Programme": programme,
        "Discipline": discipline,
        "State Name": state,
        "District Name": district,
        "Mode": mode
    }])

    user_vector = encoder.transform(
        user_data[features].astype(str)
    )

    distances, indices = model.kneighbors(
        user_vector
    )

    recommendations = data.iloc[indices[0]].copy()

    # Convert distance into similarity percentage
    similarity = (1 - distances[0]) * 100

    recommendations["ML Match Score"] = (
        similarity.round(1)
    )

    return recommendations