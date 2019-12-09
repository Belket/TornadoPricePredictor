import tornado.web
from threading import Thread
from predictor import XGBoostPredictor


class MainHandler(tornado.web.RequestHandler):

    XGB = XGBoostPredictor()
    model_data = XGB.get_model_data()
    features = [data["feature"] for data in model_data]

    def get(self):
        self.render("index.html", data=MainHandler.model_data)


class PricePredictor(tornado.web.RequestHandler):

    def get(self):
        answers = [self.get_query_argument(feature, None) for feature in MainHandler.features]
        print("ANSWERS", answers)
        price = PricePredictor.request_processing()
        response = {"price": price}
        self.write(response)

    @staticmethod
    def request_processing():
        response = 3000
        return response