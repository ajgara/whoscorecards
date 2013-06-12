class CROS(object):
    def process_response(self, request, response):
        response["Access-Control-Allow-Origin"] = "*"  
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"  
        response["Access-Control-Max-Age"] = "1000"  
        response["Access-Control-Allow-Headers"] = "*"  
        return response   
