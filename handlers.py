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

        def check_input_data_mistakes(answers):
            if sum([0 if isinstance(answer, (int, float)) else 1 for answer in answers]) != 0:
                return 1, "Все параметры - численные."
            elif answers[0] < answers[1] + answers[6]:
                return 1, "Сумма жилой площади и площади кухни не может превышать общую площадь."
            elif answers[2] > answers[3]:
                return 1, "Этаж не может превышать максимальное число этажей."
            elif answers[4] < 1700:
                return 1, "Минимальный год постройки - 1700"
            else:
                return 0, ""

        def feature_preparing(feature):
            if feature == "":
                feature = None
            if feature is not None:
                feature = int(feature)
            return feature

        answers = [self.get_query_argument(feature, None) for feature in MainHandler.features]
        answers = list(map(feature_preparing, answers))
        error, error_text = check_input_data_mistakes(answers)
        price = PricePredictor.request_processing(answers)
        response = {"price": price, "error": error, "error_text": error_text}
        self.write(response)

    @staticmethod
    def request_processing(answers):
        XGB = XGBoostPredictor()
        response = XGB.predict_price(answers)
        return response