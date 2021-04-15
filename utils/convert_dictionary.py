def get_convert_dictionary():
    convert_dictionary = {
        # Lenght
        "m": {
            "m": 1,
            "in": 39.37,
            "ft": 3.28084,
            "mi": 6.2137e-4,
            "au": 6.6846e-12
        },
        "in": {
            "m": 0.0254,
            "in": 1,
            "ft": 0.0833,
            "mi": 1.5783e-5,
            "au": 1.6979e-13
        },
        "ft": {
            "m": 0.3048,
            "in": 12,
            "ft": 1,
            "mi": 1.8939e-3,
            "au": 2.0375e-12
        },
        "mi": {
            "m": 1609.34,
            "in": 63360,
            "ft": 5280,
            "mi": 1,
            "au": 2.0375e-12
        },
        "au": {
            "m": 1.496e11,
            "in": 5.89e12,
            "ft": 4.908e+11,
            "mi": 9.296e+7,
            "au": 1
        },
        # Weight
        "g": {
            "g": 1,
            "lbs": 0.0022
        },
        "lbs": {
            "g": 453.592,
            "lbs": 1
        },
        # Temperatures for compatibility reasons
        "c": {}, 
        "f": {},
        "k": {}
    }
    
    return convert_dictionary
    