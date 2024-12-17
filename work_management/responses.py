import json

class ResponseObject:
    code: int
    data: list or dict or None
    message: str

    def __init__(self, **kwargs) -> dict or None:
        self.code = kwargs.get('code', 200)
        self.data = kwargs.get('data', None)
        self.message = kwargs.get('message', "")

    def set_not_found_resp(self, message="Data not found!"):
        self.code = 404
        self.message = message
        self.data = None


    def to_dict(self):
        data = {
            'code': self.code,
            'message': self.message,
            'data': self.data
        }
        return data


    def to_json(self):
        return json.dumps(self.to_dict())

class ErrorResponse(ResponseObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.code = kwargs.get('code', 400)
        self.errors = kwargs.get('errors', '')


    def to_dict(self):
        data = super().to_dict()
        data['errors'] = self.errors
        return data

        