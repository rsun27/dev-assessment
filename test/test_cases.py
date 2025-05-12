valid_payload = {"pin": "26062070090000"}
invalid_payload = {"pin": "1113000180000"}

compound_interest = {
    2024: 1.0515, 
    2023: 1.1043904500000001, 
    2022: 1.12294420956, 
    2021: 1.1238425649276478
}

test_case_response_1 = {
    "26062070090000": {
        "assessed value": 29300,
        "sale date": "6/1/2003"
    },
    "26062070090001": {"assessed value": 31300},
    "26062070090002": {"assessed value": 26300},
    "26062070090003": {"assessed value": 27300},
    "26062070090004": {"assessed value": 28700},
    "26062070090005": {"assessed value": 24901},
}

test_case_response_2 = {
    "1234567890": {
        "assessed value": 25000,
        "sale date": "2/3/2021"
    },
    "1234567891": {"assessed value": 28000},
    "1234567892": {"assessed value": 29000},
    "1234567893": {"assessed value": 30000}
}

