import os
import json
import unittest
import uuid

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJmaXJzdE5hbWUiOiJEZW1pZXRyaXVzIiwibGFzdE5hbWUiOiJIdWZmIiwibG9nb25UeXBlIjoiQ0EiLCJzdXBwbGllcklkIjoxMDAwLCJidXNpbmVzc0lkIjowLCJ1c2VySWQiOjI2MjIyNjg1LCJpc3MiOiJDaGFydGVyIGFuZCBHbyBhdXRoZW50aWNhdGlvbiIsImV4cCI6MTY2Njg0MzcyOX0.Sb70pwKDy6xh6OY4CAznKDCgJBDhC_N4za46bYH56amRrpd_msS1XBTHbeJbALYC8I2pYIr-Ux0oPRpmpLZc2kaPA233jQiaTH3YledXvLKuPb4MXGW4RUJ6x0E05kbzaSi9fBs7c112A5MmZUgNOZp8OGiXRaRV9K364SrWknewj7jecfKJQBSPE4g4ys6isbPGNEG0bNuXw9NxmxRCJPB0xFvxBIt7IUQ5o7wEONwVHJgPCWaKOVfGEj-loOu5b8Mr3VoxSY81irkaye35xLFX74Q3IgjMsqA2TIglLVdQMJ2jU9rIVNQg21-4cfJS7U-XJ9wnwk-IpLamUp-Cg2njRONLeb9gASZQTsKdn5oJsjONBOLnglNKry6mwYYN4kxlULbGlF_sOBLxKbTt8rkpo-UjQIXLk-aEEbfK6YpqKN5T0gBabdG6NB5llptEv3L6f_OyasXYRj1PDuh_qfj_LhMW4epvfEsO9qtEpeEDPq5pd7L4C3XhMFTkJzzF"


class Test(unittest.TestCase):
    test_template = '2022-09-15 18:17:36.599787+0000'

    def test_debug(self):
        payload ={"context":{"securityToken":"eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJmaXJzdE5hbWUiOiJEZW1pZXRyaXVzIiwibGFzdE5hbWUiOiJIdWZmIiwibG9nb25UeXBlIjoiQ0EiLCJzdXBwbGllcklkIjoxMDAwLCJidXNpbmVzc0lkIjowLCJ1c2VySWQiOjI2MjIyNjg1LCJpc3MiOiJDaGFydGVyIGFuZCBHbyBhdXRoZW50aWNhdGlvbiIsImV4cCI6MTY2NTYzOTgxOH0.JCkzPLw_ZaK3LiqTuqYMBAkdDANk2IfXbtJ2WeuJFBUGc0lGOw8bY7F3mN7EB5dubAa6rPN4vtxLfYbdz4-QkzCquxjBHlGjdy24LSABzXbOBa2mJkHEAU61pCGkUJXtb1DfnmE5QZ8wbzpO0wX8TeK1XoQTx1CQAhC1z2CsGr1SnwVLWpt9QaFwTcAQEOVfZpMXYqfP0BgD71-EsHH5SbYSkE5QgEmF-0vGPvYDsAdEsvtjU4-Vj5lBJe2Shdvdw3u3ZdGhccc6I8H43o9MkBAxM5w-9O5VMc4hk_YBl9xv2TbokpmYxplynvQ1PDTgviwXfg-P4gjfIOfbylTL2PIB_XUoVjWNo39mN60sllxEFqpcNUF61vpDehH8zi-JKEMAIn1daN6n9zoD2eoRxRGY2p3CHiT4pBxOwm7nVrws0jLtq1YsIhO6yrXlu5p_x2kb2-wg8rZbVtych4lYQOm5fwfKHFonEPhZxiEkSFrH7Xtvw3y0J_OviOhmnu1_","domainName":"Crew","language":"EN","client":"CAG POS","transactionId":"0a1b4e5c-3778-4bf4-b886-bbf491300930"},"commonParms":{"action":"Read","view":"DEFAULT","version":"1.0.0"},"request":{"supplierId":7000,"businessProfileId":0}}
        import app
        ret = app.lambda_handler(payload, "")
        pass

    def test_get_token(self):
        from lambda_accessor import lambda_accessor
        try:
            path = "C:\\Users\\Demietrius\\PycharmProjects\\CNG_CREDENTIALS.json"
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
            return_code, body = lambda_accessor.call_lambda(payload, "SecurityMS-Dev")
            token = body["responseMessage"]["responseMessage"]["securityToken"]
            print(token)
            self.__class__.foo = token
        except Exception as details:
            print("failed to login")
            print(details)

    def test_2_template_create(self):
        import app
        payload = self.cert_template_create()
        ret = app.lambda_handler(payload, "")
        data = json.loads(ret["body"])

        assert ret["statusCode"] == '200'
        assert "standardResponse" in data
        assert data["standardResponse"]["returnCode"] == 0

    def test_3_template_read_all(self):
        import app
        payload = self.cert_template_read_all()
        ret = app.lambda_handler(payload, "")
        data = json.loads(ret["body"])

        assert ret["statusCode"] == '200'
        assert "standardResponse" in data
        assert data["standardResponse"]["returnCode"] == 0
        assert "templates" in data["responseMessage"]
        assert len(data["responseMessage"]["templates"]) > 0

    def test_4_template_read(self):
        import app
        payload = self.cert_template_read()
        ret = app.lambda_handler(payload, "")
        data = json.loads(ret["body"])

        assert ret["statusCode"] == '200'
        assert "standardResponse" in data
        assert data["standardResponse"]["returnCode"] == 0
        assert "template" in data["responseMessage"]
        assert data["responseMessage"]["template"] is not None
        test_template = data["responseMessage"]["template"]["certDetails"]["lastUpdatedDate"],
        print(test_template)

    def test_5_template_update(self):
        import app
        payload = self.cert_template_update(self.template_read())
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
        import app
        payload = self.cert_template_read()
        ret = app.lambda_handler(payload, "")
        data = json.loads(ret["body"])
        return data["responseMessage"]["template"]["certDetails"]["lastUpdatedDate"],

    # ************************* json structures below***********************

    def cert_template_read_all(self):
        id = str(uuid.uuid1())
        return {
            "context": {
                "securityToken": token,
                "domainName": "Crew",
                "language": "EN",
                "client": "CAG POS",
                "transactionId": id
            },
            "commonParms": {
                "action": "Read",
                "view": "DEFAULT",
                "version": "1.0.0"
            },
            "request": {
                "supplierId": 7000,
                "businessProfileId": 0,
            }
        }

    def cert_template_create(self):
        id = str(uuid.uuid1())
        return {
            "context": {
                "securityToken": token,
                "domainName": "Crew",
                "language": "EN",
                "client": "CAG POS",
                "transactionId": id
            },
            "commonParms": {
                "action": "createTemplate",
                "view": "DEFAULT",
                "version": "1.0.0"
            },
            "request": {
                "supplierId": 7000,
                "businessProfileId": 0,
                "certTemplate": {
                    "certDetails": {
                        "userId": 0,
                        "templateType": "CUSTOM",
                        "name": "Type Rating2",
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
                            "cycleValue": 1,
                            "cycleUnit": "YEARS",
                            "timeCondition": [
                                {
                                    "timeCondition": ">",
                                    "timeValue": 9,
                                    "timeUnit": "MONTHS",
                                    "status": "GOOD",
                                    "warning": "you have 3 months to hit your goal"
                                }
                            ],
                            "status": "GOOD",
                            "errorMessage": "you are exceeding the number of days without a landing",
                            "noWork": "Y"
                        },
                        {
                            "id": 2,
                            "trackingName": "PicHours",
                            "elementType": "INT",
                            "logicalCondition": ">",
                            "logicalValue": 120,
                            "logicalUnit": "MINUTES",
                            "startTime": " ",
                            "cycleCondition": ">",
                            "cycleValue": 30,
                            "cycleUnit": "DAYS",
                            "timeCondition": [],
                            "status": "GOOD",
                            "errorMessage": "this is a warning, you need more landings",
                            "noWork": "Y"
                        },
                        {
                            "id": 3,
                            "trackingName": " ",
                            "elementType": "",
                            "logicalCondition": " ",
                            "logicalValue": 0,
                            "logicalUnit": " ",
                            "startTime": "",
                            "cycleCondition": ">",
                            "cycleValue": 3,
                            "cycleUnit": "MONTHS",
                            "timeCondition": [],
                            "status": "GOOD",
                            "errorMessage": "this is expiring",
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
                            ],
                            "tripType": []
                        },
                    }
                }
            }
        }


    def cert_template_read(self):
        id = str(uuid.uuid1())
        return {
            "context": {
                "securityToken": token,
                "domainName": "Crew",
                "language": "EN",
                "client": "CAG POS",
                "transactionId": id
            },
            "commonParms": {
                "action": "Read",
                "view": "Name",
                "version": "1.0.0"
            },
            "request": {
                "supplierId": 7000,
                "businessProfileId": 0,
                "name": "testing"
            }
        }

    def cert_template_update(self, lastupdated):
        id = str(uuid.uuid1())
        return {
            "context": {
                "securityToken": self.__class__.foo,
                "domainName": "Crew",
                "language": "EN",
                "client": "CAG POS",
                "transactionId": id
            },
            "commonParms": {
                "action": "updateTemplate",
                "view": "DEFAULT",
                "version": "1.0.0"
            },
            "request": {
                "supplierId": 7000,
                "businessProfileId": 0,
                "certTemplate": {
                    "certDetails": {
                        "userId": 0,
                        "templateType": "CNG_DEFAULT",
                        "name": "TypeRating",
                        "description": "This is a default for a Typ Rating cert.",
                        "status": "ACT",
                        "elementType": "TypeRating",
                        "positions": "PILOT",
                        "role": "PIC",
                        "logicRules": "",
                        "createdDate": "",
                        "createdBy": 0,
                        "createdByIp": "",
                        "lastUpdatedDate": lastupdated[0],
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
                            "timeCondition": ">",
                            "timeValue": 7,
                            "timeUnit": "DAYS",
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
                            "timeCondition": ">",
                            "timeValue": 30,
                            "timeUnit": "DAYS",
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
                            "timeCondition": ">",
                            "timeValue": 3,
                            "timeUnit": "MONTHS",
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
                        },
                    }
                }
            }
        }

    def cert_template_delete(self):
        id = str(uuid.uuid1())
        return {
            "context": {
                "securityToken": token,
                "domainName": "Crew",
                "language": "EN",
                "client": "CAG POS",
                "transactionId": id
            },
            "commonParms": {
                "action": "Delete",
                "view": "Name",
                "version": "1.0.0"
            },
            "request": {
                "supplierId": 7000,
                "businessProfileId": 0,
                "name": "Type Rating"
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
