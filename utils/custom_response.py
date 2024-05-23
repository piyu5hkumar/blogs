from rest_framework.response import Response

class APIResponse(Response):
    def __init__(self, status=None, template_name=None, headers=None, exception=False, content_type=None, success=True, message=None, data=None):
        response_data = {
            'success': success,
            
        }
        if success:
            response_data['data'] = data
        else:
            response_data['message'] = message
        super().__init__(response_data, status, template_name, headers, exception, content_type)