from utils import timestamp_string, APIRequest

# Change these
task_id = 576
api_info = {"key": "c0e00731-b9fc-5309-8b8c-ac1f85716074", "secret": "1e8eae50-7186-4e53-a641-892dc63edc2a"}

# Don't change these
url = "https://www.naradametrics.net"


def results(result_dict):
    # Result Dict in the format of {'received': 1}
    payload = {"task_id": task_id, "time": timestamp_string(), "results": [result_dict]}
    try:
        response = APIRequest(url=url, uri='/collector/', payload=payload, api_auth=api_info, file_name='results')
        print result_dict, response.response.status_code,  response.response.content
    except Exception as e:
        print result_dict, str(e)

