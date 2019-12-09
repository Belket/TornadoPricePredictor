import joblib
import numpy as np
import pandas as pd
# import xgboost as xgb


class XGBoostPredictor:

    def __init__(self):
        # self._model = joblib.load('xgboost.pkl')
        self._features = ['full_sq', 'life_sq', 'floor', 'max_floor', 'build_year', 'num_room', 'kitch_sq',
                          'metro_min_walk', 'public_transport_station_min_walk', 'water_km', 'kremlin_km']
        self._placeholders = ["Общая площадь", "Жилая площадь", "Этаж", "Этажей всего", "Год постройки",
                              "Количество комнат", "Площадь кухни", "До метро", "До общественного транспорта",
                              "До водоемов", "До Кремля"]
        self._patterns = ["[0-9]{,3}", "[0-9]{,3}", "[0-9]{,2}", "[0-9]{,2}", "[0-9]{4,4}", "[0-9]{,2}", "[0-9]{,3}",
                          "[0-9]{,2}", "[0-9]{,2}", "[0-9]{,2}", "[0-9]{,2}"]

    def get_model_data(self):
        feature_placeholder_pairs = []
        for index in range(len(self._features)):
            feature_placeholder_pairs.append({"feature": self._features[index], "placeholder": self._placeholders[index],
                                              })
        return feature_placeholder_pairs

    def _create_xgboost_matrix(self, user_parameters):
        user_parameters = np.array(user_parameters).reshape(1, -1)
        features = pd.Index(self._features, dtype=object)
        return xgb.DMatrix(user_parameters, feature_names=features)

    def _make_prediction(self, xgb_matrix):
        ylog_pred = self._model.predict(xgb_matrix)
        return np.exp(ylog_pred) - 1

    def predict_price(self, answers):
        xgb_matrix = self._create_xgboost_matrix(answers)
        return self._make_prediction(xgb_matrix)[0]