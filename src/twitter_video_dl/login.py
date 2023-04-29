import requests
import json

class TwitterLoginClient:
   def __init__(self, bear_token,proxies={}):
      self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
      self.bear_token = bear_token
      self.proxies = proxies
      self.session = requests.session()
      self.__twitter()
      self.x_guest_token = self.get_guest_token()
      self.flow_token = None

   def login(self,username,password):

    


   def __twitter(self):
    headers = {
            "User-Agent":self.USER_AGENT,
        }
    response = self.session.get(
            "https://twitter.com/", headers=headers, proxies=self.proxies
  )
  


   def get_guest_token(self):
    headers = {
            "authorization": self.AUTHORIZATION,
            "User-Agent": self.USER_AGENT,
        }
    response = self.session.post(
            "https://api.twitter.com/1.1/guest/activate.json",
            headers=headers,
            proxies=self.proxies,
        ).json()
    return response["guest_token"]
   

   def login_flow(self):
        data = {
            "input_flow_data": {
                "flow_context": {
                    "debug_overrides": {},
                    "start_location": {"location": "splash_screen"},
                }
            },
            "subtask_versions": {
                "contacts_live_sync_permission_prompt": 0,
                "email_verification": 1,
                "topics_selector": 1,
                "wait_spinner": 1,
                "cta": 4,
            },
        }
        params = {"flow_name": "login"}
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            params=params,
            proxies=self.proxies,
        ).json()
        self.__error_check(response)
        self.flow_token = response.get("flow_token")
        self.content = response
        return self

    def LoginJsInstrumentationSubtask(self):
        self.__flow_token_check()
        self.__method_check("LoginJsInstrumentationSubtask")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "LoginJsInstrumentationSubtask",
                    "js_instrumentation": {
                        "response": json.dumps(
                            {
                                "rf": {
                                    "af07339bbc6d24ced887d705eb0c9fd29b4a7d7ddc21136c9f94d53a4bc774d2": 88,
                                    "a6ce87d6481c6ec4a823548be3343437888441d2a453061c54f8e2eb325856f7": 250,
                                    "a0062ad06384a8afd38a41cd83f31b0dbfdea0eff4b24c69f0dd9095b2fb56d6": 16,
                                    "a929e5913a5715d93491eaffaa139ba4977cbc826a5e2dbcdc81cae0f093db25": 186,
                                },
                                "s": "Q-H-53m1uXImK0F0ogrxRQtCWTH1KIlPbIy0MloowlMa4WNK5ZCcDoXyRs1q_cPbynK73w_wfHG_UVRKKBWRoh6UJtlPS5kMa1p8fEvTYi76hwdzBEzovieR8t86UpeSkSBFYcL8foYKSp6Nop5mQR_QHGyEeleclCPUvzS0HblBJqZZdtUo-6by4BgCyu3eQ4fY5nOF8fXC85mu6k34wo982LMK650NsoPL96DBuloqSZvSHU47wq2uA4xy24UnI2WOc6U9KTvxumtchSYNnXq1HV662B8U2-jWrzvIU4yUHV3JYUO6sbN6j8Ho9JaUNJpJSK7REwqCBQ3yG7iwMAAAAX2Vqcbs",
                            }
                        ),
                        "link": "next_link",
                    },
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.__error_check(response)
        self.flow_token = response.get("flow_token")
        self.content = response
        return self

    def LoginEnterUserIdentifierSSO(self, user_id):
        self.__flow_token_check()
        self.__method_check("LoginEnterUserIdentifierSSO")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "LoginEnterUserIdentifierSSO",
                    "settings_list": {
                        "setting_responses": [
                            {
                                "key": "user_identifier",
                                "response_data": {"text_data": {"result": user_id}},
                            }
                        ],
                        "link": "next_link",
                    },
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.__error_check(response)
        self.flow_token = response.get("flow_token")
        self.content = response
        return self
