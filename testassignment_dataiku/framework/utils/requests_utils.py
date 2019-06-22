import requests
import json
from requests.auth import HTTPBasicAuth
from urllib.parse import urljoin


BASEURL = "http://iankusheva.qatest.dataiku.com/"
TAGS = "tags"
USERS = "users"
AUTH = "authenticate"
RESET = "reset"


class RequestsHelpers:
    @staticmethod
    def post_request(url, data, verify=True):
        try:
            rsp = requests.post(url, json=data)
            if verify:
                assert rsp.status_code == 200, "Unsuccessful post request, got response code {}".format(rsp.status_code)
            return rsp
        except Exception:
            print("Failed to retrieve: %s", url)
            raise

    @staticmethod
    def get_request(url, params=None):
        try:
            rsp = requests.get(url, params)
            assert rsp.status_code == 200, "Unsuccessful get request, got response code {}".format(rsp.status_code)
            return rsp
        except Exception:
            raise

    @staticmethod
    def put_request(url, data, verify, auth=None, headers=None):
        try:
            rsp = requests.put(url, data, auth=auth, headers=headers)
            if verify:
                assert rsp.status_code == 200, "Unsuccessful put request, got response code {}".format(rsp.status_code)
            return rsp
        except Exception:
            raise

    @staticmethod
    def delete_request(url, verify, auth=None):
        try:
            rsp = requests.delete(url, auth=auth)
            if verify:
                assert rsp.status_code == 200, "Unsuccessful delete request, got response code {}".format(
                    rsp.status_code)
            return rsp
        except Exception:
            raise

    @staticmethod
    def patch_request(url, data, verify, auth=None):
        try:
            rsp = requests.patch(url, data, auth=auth)
            if verify:
                assert rsp.status_code == 200, "Unsuccessful patch request, got response code {}".format(
                    rsp.status_code)
            return rsp
        except Exception:
            raise


class AvailableAPIActions:
    
    @staticmethod
    def get_list_of_tasks():
        return RequestsHelpers.get_request(BASEURL)

    @staticmethod
    def get_list_of_tags():
        return RequestsHelpers.get_request(urljoin(BASEURL, TAGS))

    @staticmethod
    def create_task(params, username, password, verify=True, needs_auth=True):
        auth = HTTPBasicAuth(username, password) if needs_auth else None
        rsp = RequestsHelpers.put_request(BASEURL, json.dumps(params), verify, auth)
        return rsp

    @staticmethod
    def create_task_with_token(params, headers, verify=True):
        rsp = RequestsHelpers.put_request(BASEURL, json.dumps(params), verify=verify, headers=headers)
        return rsp

    @staticmethod
    def get_task_description(task_id):
        return RequestsHelpers.get_request(urljoin(BASEURL, str(task_id)))

    @staticmethod
    def delete_task(task_id, username, password, verify=True, needs_auth=True):
        auth = HTTPBasicAuth(username, password) if needs_auth else None
        rsp = RequestsHelpers.delete_request(urljoin(BASEURL, str(task_id)), verify, auth)
        return rsp

    @staticmethod
    def modify_task(task_id, data, username, password, verify=True, needs_auth=True):
        auth = HTTPBasicAuth(username, password) if needs_auth else None
        rsp = RequestsHelpers.patch_request(urljoin(BASEURL, str(task_id)), json.dumps(data), verify, auth)
        return rsp

    @staticmethod
    def get_information_about_tag(tag_id):
        rsp = RequestsHelpers.get_request(urljoin(BASEURL, "{}/{}".format(TAGS, tag_id)))
        return rsp

    @staticmethod
    def create_new_user(data, verify=True):
        rsp = RequestsHelpers.post_request(urljoin(BASEURL, USERS), data, verify)
        return rsp

    @staticmethod
    def authenticate(data, verify=True):
        return RequestsHelpers.post_request(urljoin(BASEURL, AUTH), data, verify)

    @staticmethod
    def reset_db():
        RequestsHelpers.get_request(urljoin(BASEURL, RESET))

    @staticmethod
    def create_auth_headers(token):
        return {'Authorization': 'Basic {}'.format(token)}

    @staticmethod
    def create_params_for_auth(username, password):
        return {"username": username, "password": password}

    @staticmethod
    def create_params_for_task_creation(title, tags=None):
        params_struct = {"title": title}
        if tags:
            params_struct["tags"] = tags

        return params_struct

    @staticmethod
    def create_params_for_task_modification(**kwargs):
        params = {}
        allowed_keys = ("title", "tags", "date", "done", "id", "username")
        for k, v in kwargs.items():
            if k not in allowed_keys:
                continue
            params[k] = v

        return params


