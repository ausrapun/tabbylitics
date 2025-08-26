# this catalogue is used to define the questions and their types in the survey
# each individual survey will require a new catalogue

question_catalogue = {
    "What is your location?": {
        "type": "single_choice",
        "datatype": "string"
    },
    "What is your age?": {
        "type": "single_choice",
        "datatype": "string"   # age ranges like "25-34", "55+"
    },
    "What is your gender?": {
        "type": "single_choice",
        "datatype": "string"
    },
    "What is your role?": {
        "type": "single_choice",
        "datatype": "string"
    },
    "What is your industry?": {
        "type": "single_choice",
        "datatype": "string"
    },
    "Which AI tools do you prefer to use?": {
        "type": "multi_choice",
        "datatype": "string",
        "delimiter": "|"
    },
    "Which SaaS tools do you use within your role?": {
        "type": "multi_choice",
        "datatype": "string",
        "delimiter": "|"
    },
    "On a scale of 1-10, how satisfied are you with your role?": {
        "type": "scale",
        "datatype": "int"
    },
    "On a scale of 1-10, how useful is AI in your role?": {
        "type": "scale",
        "datatype": "int"
    },
    "Any comments you would like to leave about your role?": {
        "type": "free_text",
        "datatype": "string"
    }
}