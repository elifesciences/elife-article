# coding=utf-8

"""
CRediT taxonomy and functions
"""

# allowed values for CRediT roles
CREDIT_ROLES = [
    "Conceptualization",
    "Data curation",
    "Formal analysis",
    "Funding acquisition",
    "Investigation",
    "Methodology",
    "Project administration",
    "Resources",
    "Software",
    "Supervision",
    "Validation",
    "Visualization",
    "Writing - original draft",
    "Writing - review & editing",
]

# map of contribution text phrases mapped to CRediT roles
CREDIT_ROLE_MAP = {
    "Conceptualisation": ["Conceptualization"],
    "Conceptualization": ["Conceptualization"],
    "Data curation": ["Data curation"],
    "Formal analysis": ["Formal analysis"],
    "Funding acquisition": ["Funding acquisition"],
    "Investigation": ["Investigation"],
    "Methodology": ["Methodology"],
    "Project administration": ["Project administration"],
    "Resources": ["Resources"],
    "Software": ["Software"],
    "Supervision": ["Supervision"],
    "Validation": ["Validation"],
    "Visualization": ["Visualization"],
    "Writing - original draft": ["Writing - original draft"],
    "Writing - review & editing": ["Writing - review & editing"],
    "Writing - review and editing": ["Writing - review & editing"],
    "Writing – original draft": ["Writing - original draft"],
    "Writing – review & editing": ["Writing - review & editing"],
    "Writing – review and editing": ["Writing - review & editing"],
    "Writing — original draft": ["Writing - original draft"],
    "Writing — review & editing": ["Writing - review & editing"],
    "Writing — review and editing": ["Writing - review & editing"],
}


def parse_credit_roles(contribution_text):
    "from author contribution text, extract CRediT roles"
    credit_roles = set()
    for phrase in contribution_text.split(","):
        # match exact phrase including case sensitivity
        if phrase.strip() in CREDIT_ROLE_MAP:
            roles = CREDIT_ROLE_MAP.get(phrase.strip())
            credit_roles = credit_roles.union(set(roles))
    return credit_roles
