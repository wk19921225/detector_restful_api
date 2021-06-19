class Response:
    @staticmethod
    def success(data=None, message=None, status=200):
        response = {
            "result": True,
            "status": "success",
        }

        if message:
            response["message"] = message
        if data:
            response["data"] = data

        return response, status

    @staticmethod
    def fail(data=None, message=None, status=400):
        response = {
            "result": False,
            "status": "fail",
        }

        if message:
            response["message"] = message
        if data:
            response["data"] = data

        return response, status

    @staticmethod
    def error(data=None, message=None, status=500):
        response = {
            "result": False,
            "status": "error",
        }

        if message:
            response["message"] = message
        if data:
            response["data"] = data

        return response, status
