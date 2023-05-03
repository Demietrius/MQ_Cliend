import json
import unittest
import uuid


class Test(unittest.TestCase):
    foo = ""
    test_template = None

    def test_1_get_token(self):
        from lambda_accessor import lambda_accessor
        try:
            path = "C:\\Users\\user\\PycharmProjects\\CNG_CREDENTIALS.json"
            file = open(path)
            credentials = json.loads(file.read())
            id = str(uuid.uuid1())
            payload = {
                "context": {
                    "securityToken": "",
                    "domainName": "Security",
                    "language": "EN",
                    "client": "CAG POS",
                    "transactionId": id
                },
                "commonParms": {
                    "action": "SIGNON",
                    "view": "DEFAULT",
                    "version": "1.0.0"
                },
                "request": {
                    "userName": credentials["ca_user"],
                    "password": credentials["ca_password"]
                }
            }
            return_code, response_type, body = lambda_accessor.call_lambda(payload, "SecurityMS-Dev")
            token = body["responseMessage"]["responseMessage"]["securityToken"]
            print(token)
            self.__class__.foo = token
        except Exception as details:
            print("failed to login")
            print(details)

    def test_2_template_create(self):
        from src import app
        payload = self.cert_template_create()
        ret = app.lambda_handler(payload, "")
        data = json.loads(ret["body"])

        assert ret["statusCode"] == '200'
        assert "standardResponse" in data
        assert data["standardResponse"]["returnCode"] == 0

    def test_3_template_read_all(self):
        from src import app
        payload = self.cert_template_read_all()
        ret = app.lambda_handler(payload, "")
        data = json.loads(ret["body"])

        assert ret["statusCode"] == '200'
        assert "standardResponse" in data
        assert data["standardResponse"]["returnCode"] == 0
        assert "templates" in data["responseMessage"]
        assert len(data["responseMessage"]["templates"]) > 0

    def test_4_template_read(self):
        from src import app
        payload = self.cert_template_read()
        ret = app.lambda_handler(payload, "")
        data = json.loads(ret["body"])

        assert ret["statusCode"] == '200'
        assert "standardResponse" in data
        assert data["standardResponse"]["returnCode"] == 0
        assert "templates" in data["responseMessage"]
        assert data["responseMessage"]["templates"] is not None
        test_template = data["responseMessage"]["templates"][0]["certDetails"]["lastUpdatedDate"],
        print(test_template)

    def test_5_template_update(self):
        from src import app
        self.template_read()
        payload = self.cert_template_update()
        ret = app.lambda_handler(payload, "")
        data = json.loads(ret["body"])

        assert ret["statusCode"] == '200'
        assert "standardResponse" in data
        assert data["standardResponse"]["returnCode"] == 0
        assert "responseMessage" in data
        assert "testingList" not in data["responseMessage"]["template"]["trackable"]

    def test_6_template_delete(self):
        import app
        payload = self.cert_template_delete()
        ret = app.lambda_handler(payload, "")
        data = json.loads(ret["body"])

        assert ret["statusCode"] == '200'
        assert "standardResponse" in data
        assert data["standardResponse"]["returnCode"] == 0

    # helper functions
    def template_read(self):
        from src import app
        payload = self.cert_template_read()
        ret = app.lambda_handler(payload, "")
        data = json.loads(ret["body"])
        self.__class__.test_template = data["responseMessage"]["templates"][0]["certDetails"]["lastUpdatedDate"]

    # ************************* json structures below***********************

    def cert_template_read_all(self):
        return {
            "context": {
                "securityToken": self.__class__.foo,
                "domainName": "Crew",
                "language": "EN",
                "client": "CAG POS",
                "transactionId": "e12d339f-b8f5-408c-a889-e5536dec0dc5"
            },
            "commonParms": {
                "action": "Read",
                "view": "DEFAULT",
                "version": "1.0.0"
            },
            "request": {
                "supplierId": 83498,
                "businessProfileId": 0,
            }
        }

    def cert_template_create(self):
        return {
            "context": {
                "securityToken": self.__class__.foo,
                "domainName": "Crew",
                "language": "EN",
                "client": "CAG POS",
                "transactionId": "e12d339f-b8f5-408c-a889-e5536dec0dc5"
            },
            "commonParms": {
                "action": "createTemplate",
                "view": "DEFAULT",
                "version": "1.0.0"
            },
            "request": {
                "supplierId": 83498,
                "businessProfileId": 0,
                "certTemplate": {
                    "certDetails": {
                        "userId": 0,
                        "templateType": "CNG_DEFAULT",
                        "name": "testing",
                        "description": "This is a default for a Typ Rating cert.",
                        "status": "ACT",
                        "certType": "TypeRating",
                        "positions": "PILOT",
                        "role": "PIC",
                        "logicRules": "",
                        "createdDate": "",
                        "createdBy": 0,
                        "createdByIp": "",
                        "lastUpdatedDate": "",
                        "lastUpdatedBy": 0,
                        "lastUpdatedIp": "",
                    },
                    "currency": [
                        {
                            "id": 1,
                            "trackingName": "numberOfLandings",
                            "elementType": "INT",
                            "logicalCondition": ">",
                            "logicalValue": 4,
                            "logicalUnit": "CYCLES",
                            "startTime": "",
                            "cycleCondition": ">",
                            "cycleValue": 7,
                            "cycleUnit": "DAYS",
                            "timeCondition": [],
                            "status": "GOOD",
                            "warning": "you are exceeding the number of days without a landing",
                            "noWork": "Y"
                        },
                        {
                            "id": 2,
                            "trackingName": "hoursInLast30Days",
                            "elementType": "INT",
                            "logicalCondition": ">",
                            "logicalValue": 120,
                            "logicalUnit": "minutes",
                            "startTime": "2022-10-02T13:00:00-07:00",
                            "cycleCondition": ">",
                            "cycleValue": 30,
                            "cycleUnit": "DAYS",
                            "timeCondition": [],
                            "status": "GOOD",
                            "warning": "this is a warning, you need more landings",
                            "noWork": "Y"
                        },
                        {
                            "id": 3,
                            "trackingName": " ",
                            "elementType": "",
                            "logicalCondition": " ",
                            "logicalValue": 0,
                            "logicalUnit": " ",
                            "startTime": "2022-10-02T13:00:00-07:00",
                            "cycleCondition": ">",
                            "cycleValue": 3,
                            "cycleUnit": "MONTHS",
                            "timeCondition": [],
                            "warning": "this is expiring",
                            "noWork": "Y"
                        }
                    ],
                    "trackable": {
                        "PicHours": {
                            "name": "PicHours",
                            "displayName": "PIC Hours",
                            "unit": "MINUTES",
                            "elementType": "INT",
                            "validValues": [],
                            "status": "CNG_DEFAULT",
                            "linkedTrackablesTo": [
                                "AIRCRAFT"
                            ],
                            "tripType": []
                        },
                        "numberOfLandings": {
                            "name": "numberOfLandings",
                            "displayName": "number of landings",
                            "description": "number of landings",
                            "unit": "CYCLE",
                            "example": "400",
                            "elementType": "INT",
                            "validValues": [],
                            "status": "CNG_DEFAULT",
                            "linkedTrackablesTo": [
                                "AIRCRAFT"
                            ],
                            "tripType": []
                        },
                        "firstName": {
                            "name": "firstName",
                            "displayName": "first name",
                            "description": "First Name",
                            "unit": "",
                            "example": "first name",
                            "elementType": "STRING",
                            "validValues": [],
                            "status": "CNG_DEFAULT",
                            "linkedTrackablesTo": [
                                "AIRCRAFT"
                            ],
                            "tripType": []
                        },
                        "LatName": {
                            "name": "LastName",
                            "displayName": "Last Name",
                            "description": "",
                            "unit": "",
                            "example": "",
                            "elementType": "STRING",
                            "validValues": [],
                            "status": "CNG_DEFAULT",
                            "linkedTrackablesTo": [
                                "AIRCRAFT"
                            ],
                            "tripType": []
                        },
                        "testingList": {
                            "name": "",
                            "displayName": "",
                            "description": "",
                            "unit": "",
                            "example": "",
                            "elementType": "LIST",
                            "validValues": ["yes", "no"],
                            "status": "CUSTOM",
                            "linkedTrackablesTo": [
                                "AIRCRAFT"
                            ],
                            "tripType": [""]
                        }
                    }
                }
            }
        }

    def cert_template_read(self):
        return {
            "context": {
                "securityToken": self.__class__.foo,
                "domainName": "Crew",
                "language": "EN",
                "client": "CAG POS",
                "transactionId": "e12d339f-b8f5-408c-a889-e5536dec0dc5"
            },
            "commonParms": {
                "action": "Read",
                "view": "Name",
                "version": "1.0.0"
            },
            "request": {
                "supplierId": 83498,
                "businessProfileId": 0,
                "name": "testing"
            }
        }

    def cert_template_update(self):
        return {
            "context": {
                "securityToken": self.__class__.foo,
                "domainName": "Crew",
                "language": "EN",
                "client": "CAG POS",
                "transactionId": "e12d339f-b8f5-408c-a889-e5536dec0dc5"
            },
            "commonParms": {
                "action": "updateTemplate",
                "view": "DEFAULT",
                "version": "1.0.0"
            },
            "request": {
                "supplierId": 83498,
                "businessProfileId": 0,
                "certTemplate": {
                    "certDetails": {
                        "userId": 0,
                        "templateType": "CNG_DEFAULT",
                        "name": "testing",
                        "description": "This is a default for a Typ Rating cert.",
                        "status": "ACT",
                        "certType": "TypeRating",
                        "positions": "PILOT",
                        "role": "PIC",
                        "logicRules": "",
                        "createdDate": "",
                        "createdBy": 0,
                        "createdByIp": "",
                        "lastUpdatedDate": self.__class__.test_template,
                        "lastUpdatedBy": 0,
                        "lastUpdatedIp": "",
                        "aircraft": [
                            {
                                "manufacturer": "",
                                "model": "",
                                "typeRating": "",
                                "tailNumber": "",
                                "certifiedCagId": [],
                                "trackables": {}
                            }
                        ]
                    },
                    "currency": [
                        {
                            "id": 1,
                            "trackingName": "numberOfLandings",
                            "elementType": "INT",
                            "logicalCondition": ">",
                            "logicalValue": 4,
                            "logicalUnit": "CYCLES",
                            "startTime": "",
                            "cycleCondition": ">",
                            "cycleValue": 7,
                            "cycleUnit": "DAYS",
                            "timeCondition": [],
                            "status": "GOOD",
                            "warning": "you are exceeding the number of days without a landing",
                            "noWork": "Y"
                        },
                        {
                            "id": 2,
                            "trackingName": "hoursInLast30Days",
                            "elementType": "INT",
                            "logicalCondition": ">",
                            "logicalValue": 120,
                            "logicalUnit": "minutes",
                            "startTime": "2022-10-02T13:00:00-07:00",
                            "cycleCondition": ">",
                            "cycleValue": 30,
                            "cycleUnit": "DAYS",
                            "timeCondition": [],
                            "status": "GOOD",
                            "warning": "this is a warning, you need more landings",
                            "noWork": "Y"
                        },
                        {
                            "id": 3,
                            "trackingName": " ",
                            "elementType": "",
                            "logicalCondition": " ",
                            "logicalValue": 0,
                            "logicalUnit": " ",
                            "startTime": "2022-10-02T13:00:00-07:00",
                            "cycleCondition": ">",
                            "cycleValue": 3,
                            "cycleUnit": "MONTHS",
                            "timeCondition": [],
                            "warning": "this is expiring",
                            "noWork": "Y"
                        }
                    ],
                    "trackable": {
                        "PicHours": {
                            "name": "PicHours",
                            "displayName": "PIC Hours",
                            "unit": "MINUTES",
                            "elementType": "INT",
                            "validValues": [],
                            "status": "CNG_DEFAULT",
                            "linkedTrackablesTo": [
                                "PILOT_LOG",
                                "AIRCRAFT"
                            ],
                            "tripType": []
                        },
                        "numberOfLandings": {
                            "name": "numberOfLandings",
                            "displayName": "number of landings",
                            "description": "number of landings",
                            "unit": "CYCLE",
                            "example": "400",
                            "elementType": "INT",
                            "validValues": [],
                            "status": "CNG_DEFAULT",
                            "linkedTrackablesTo": [
                                "PILOT_LOG",
                                "AIRCRAFT"
                            ],
                            "tripType": []
                        },
                        "firstName": {
                            "name": "firstName",
                            "displayName": "first name",
                            "description": "First Name",
                            "unit": "",
                            "example": "first name",
                            "elementType": "STRING",
                            "validValues": [],
                            "status": "CNG_DEFAULT",
                            "linkedTrackablesTo": [
                                "PILOT_LOG",
                                "AIRCRAFT"
                            ],
                            "tripType": []
                        },
                        "LatName": {
                            "name": "LastName",
                            "displayName": "Last Name",
                            "description": "",
                            "unit": "",
                            "example": "",
                            "elementType": "STRING",
                            "validValues": [],
                            "status": "CNG_DEFAULT",
                            "linkedTrackablesTo": [
                                "PILOT_LOG",
                                "AIRCRAFT"
                            ],
                            "tripType": []
                        }
                    }
                }
            }
        }

    def cert_template_delete(self):
        return {
            "context": {
                "securityToken": self.__class__.foo,
                "domainName": "Crew",
                "language": "EN",
                "client": "CAG POS",
                "transactionId": "e12d339f-b8f5-408c-a889-e5536dec0dc5"
            },
            "commonParms": {
                "action": "Delete",
                "view": "Name",
                "version": "1.0.0"
            },
            "request": {
                "supplierId": 83498,
                "businessProfileId": 0,
                "name": "testing"
            }
        }

    # def test_submit_login(self):
    #     import process_certifications
    #     try:
    #         var1 = "1N2"
    #         var2 = "(1N2)O3"
    #         var3 = "((1O2)N(3O4)N(1O4))N5"
    #         currency = [
    #             {
    #                 "id": 1,
    #                 "name": "test1",
    #                 "value": 100,
    #                 "condition": ">",
    #                 "warning": "id 1 is bad"
    #             },
    #             {
    #                 "id": 2,
    #                 "name": "test2",
    #                 "value": 100,
    #                 "condition": ">",
    #                 "warning": "id 2 is bad"
    #             },
    #             {
    #                 "id": 3,
    #                 "name": "test3",
    #                 "value": 100,
    #                 "condition": ">",
    #                 "warning": "id 3 is bad"
    #             },
    #             {
    #                 "id": 4,
    #                 "name": "test4",
    #                 "value": 100,
    #                 "condition": ">",
    #                 "warning": "id 4 is bad"
    #             },
    #             {
    #                 "id": 5,
    #                 "name": "test5",
    #                 "value": 100,
    #                 "condition": ">",
    #                 "warning": "id 5 is bad"
    #             }
    #         ]
    #         value = {
    #             "test1": 100,
    #             "test2": 100,
    #             "test3": 101,
    #             "test4": 101,
    #             "test5": 101
    #         }
    #         var3 = "((1O2)N(3O4)N(1O4))N5"
    #         is_true, warnings = process_certifications.process_currency_logic(var3, currency, value)
    #         print("---------------\n")
    #         print(is_true)
    #         print(*warnings, sep=", ")
    #     except Exception as details:
    #         return 01, format(details)
