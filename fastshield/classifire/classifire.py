import joblib
import urllib.parse
import json
from fastshield.request import BaseRequest
from pathlib import Path



class ThreatClassifier(object):
    def __init__(self):
        main_path = Path(__file__).parent.parent / 'models'
        try:
            self.clf = joblib.load(main_path / "predictor.joblib")
            self.pt_clf = joblib.load(main_path / "pt_predictor.joblib")
        except FileNotFoundError as e:
            print(f"Error loading model: {e}")
            self.clf = None
            self.pt_clf = None

    def __unquote(self, text: str) -> str:
        """
        decodes a URL-encoded string until it is fully decoded 
        or a maximum of 100 iterations is reached.
        """
        k = 0
        uq_prev = text
        while k < 100:
            uq = urllib.parse.unquote_plus(uq_prev)
            if uq == uq_prev:
                break
            else:
                uq_prev = uq
        return uq_prev

    def __remove_new_line(self, text: str) -> str:
        text = text.strip()
        return ' '.join(text.splitlines())

    def __remove_multiple_whitespaces(self, text) -> str:
        return ' '.join(text.split())

    def __clean_pattern(self, pattern: str) -> str:
        pattern = self.__unquote(pattern)
        pattern = self.__remove_new_line(pattern)
        pattern = pattern.lower()
        pattern = self.__remove_multiple_whitespaces(pattern)
        return pattern

    def __is_valid(self, parameter):
        return parameter is not None and parameter != ''

    def classify_request(self, req: BaseRequest) -> BaseRequest:
        """
        To classify the threat type from the request
        """
        if not isinstance(req, BaseRequest):
            raise TypeError("Object should be a Request!!!")

        # To Classify the threat type from the request
        ## Populate the parameters and locations in the request
        parameters = []
        locations = []
        if self.__is_valid(req.request):
            parameters.append(self.__clean_pattern(req.request))
            locations.append('Request')
        if self.__is_valid(req.body):
            parameters.append(self.__clean_pattern(req.body))
            locations.append('Body')
        if 'Cookie' in req.headers and self.__is_valid(req.headers['Cookie']):
            parameters.append(self.__clean_pattern(req.headers['Cookie']))
            locations.append('Cookie')
        if 'User_Agent' in req.headers and self.__is_valid(req.headers['User_Agent']):
            parameters.append(self.__clean_pattern(req.headers['User_Agent']))
            locations.append('User Agent')
        if 'Accept_Encoding' in req.headers and self.__is_valid(req.headers['Accept_Encoding']):
            parameters.append(self.__clean_pattern(req.headers['Accept_Encoding']))
            locations.append('Accept Encoding')
        if 'Accept_Language' in req.headers and self.__is_valid(req.headers['Accept_Language']):
            parameters.append(self.__clean_pattern(req.headers['Accept_Language']))
            locations.append('Accept Language')
        if 'Referer' in req.headers and self.__is_valid(req.headers['Referer']):
            parameters.append(self.__clean_pattern(req.headers['Referer']))
            locations.append('Referer')
        if 'Cache_Control' in req.headers and self.__is_valid(req.headers['Cache_Control']):
            parameters.append(self.__clean_pattern(req.headers['Cache_Control']))
            locations.append('Cache Control')
        
        ## Classify the threat type from the request
        req.threats = dict()
        if len(parameters) != 0:
            predictions = self.clf.predict(parameters)
            for idx, pred in enumerate(predictions):
                if pred != 'valid':
                    req.threats[pred] = locations[idx]

        # To Classify the parameter tampering from the request
        ## to parse Query Parameters from the request
        request_parameters = dict()
        if self.__is_valid(req.request):
            request_parameters = urllib.parse.parse_qs(self.__clean_pattern(req.request))
        
        ## to parse Body Parameters from the request
        body_parameters = dict()
        if self.__is_valid(req.body):
            body_parameters = urllib.parse.parse_qs(self.__clean_pattern(req.body))
            if len(body_parameters) == 0:
                # in case of JSON body
                try:
                    body_parameters = json.loads(self.__clean_pattern(req.body))
                except json.JSONDecodeError:
                    pass
            # print(body_parameters)

        ## Populate the parameters and locations in the request
        parameters = []
        locations = []
        for name, value in request_parameters.items():
            for e in value:
                parameters.append([len(e)])
                locations.append('Request')  
        for name, value in body_parameters.items():
            if isinstance(value, list):
                # array of values
                for e in value:
                    parameters.append([len(e)])
                    locations.append('Body')
            else:
                parameters.append([len(value)])
                locations.append('Body')

        ## Classify the threat type from the request
        if len(parameters) != 0:
            pt_predictions = self.pt_clf.predict(parameters)

            for idx, pred in enumerate(pt_predictions):
                if pred != 'valid':
                    req.threats[pred] = locations[idx]

        if len(req.threats) == 0:
            req.threats['valid'] = ''
    
        return req
