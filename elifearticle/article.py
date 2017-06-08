
class Article():
    """
    We include some boiler plate in the init, namely articleType
    """
    contributors = []

    def __init__(self, doi=None, title=None):
        self.article_type = "research-article"
        self.display_channel = None
        self.doi = doi
        self.contributors = []
        self.title = title
        self.abstract = ""
        self.research_organisms = []
        self.manuscript = None
        self.dates = None
        self.license = None
        self.article_categories = []
        self.conflict_default = None
        self.ethics = []
        self.author_keywords = []
        self.funding_awards = []
        self.ref_list = []
        self.component_list = []
        # For PubMed function a hook to specify if article was ever through PoA pipeline
        self.was_ever_poa = None
        self.is_poa = None
        self.volume = None
        self.elocation_id = None
        self.related_articles = []
        self.version = None
        self.datasets = []
        self.funding_awards = []
        self.funding_note = None

    def add_contributor(self, contributor):
        self.contributors.append(contributor)

    def add_research_organism(self, research_organism):
        self.research_organisms.append(research_organism)

    def add_date(self, date):
        if not self.dates:
            self.dates = {}
        self.dates[date.date_type] = date

    def get_date(self, date_type):
        try:
            return self.dates[date_type]
        except (KeyError, TypeError):
            return None

    def get_display_channel(self):
        # display-channel string partly relates to the articleType
        return self.display_channel

    def add_article_category(self, article_category):
        self.article_categories.append(article_category)

    def has_contributor_conflict(self):
        # Return True if any contributors have a conflict
        for contributor in self.contributors:
            if contributor.conflict:
                return True
        return False

    def add_ethic(self, ethic):
        self.ethics.append(ethic)

    def add_author_keyword(self, author_keyword):
        self.author_keywords.append(author_keyword)

    def add_dataset(self, dataset):
        self.datasets.append(dataset)

    def get_datasets(self, dataset_type=None):
        if dataset_type:
            return filter(lambda d: str(d.dataset_type) == dataset_type, self.datasets)
        else:
            return self.datasets

    def add_funding_award(self, funding_award):
        self.funding_awards.append(funding_award)


class ArticleDate():
    """
    A struct_time date and a date_type
    """

    def __init__(self, date_type, date):
        self.date_type = date_type
        # Date as a time.struct_time
        self.date = date


class Contributor():
    """
    Currently we are not sure that we can get an auth_id for
    all contributors, so this attribute remains an optional attribute.
    """

    corresp = False
    equal_contrib = False

    auth_id = None
    orcid = None
    collab = None
    conflict = None
    group_author_key = None

    def __init__(self, contrib_type, surname, given_name, collab=None):
        self.contrib_type = contrib_type
        self.surname = surname
        self.given_name = given_name
        self.affiliations = []
        self.collab = collab

    def set_affiliation(self, affiliation):
        self.affiliations.append(affiliation)

    def set_conflict(self, conflict):
        self.conflict = conflict


class Affiliation():
    phone = None
    fax = None
    email = None

    department = None
    institution = None
    city = None
    country = None

    text = None


class Dataset():
    """
    Article component representing a dataset
    """
    def __init__(self):
        self.dataset_type = None
        self.authors = []
        self.source_id = None
        self.year = None
        self.title = None
        self.license_info = None

    def add_author(self, author):
        self.authors.append(author)


class FundingAward():
    """
    An award group as part of a funding group
    """
    def __init__(self):
        self.award_ids = []
        self.institution_name = None
        self.institution_id = None
        self.principal_award_recipients = []

    def add_award_id(self, award_id):
        self.award_ids.append(award_id)

    def add_principal_award_recipient(self, contributor):
        # Accepts an instance of Contributor
        self.principal_award_recipients.append(contributor)

    def get_funder_identifier(self):
        # Funder identifier is the unique id found in the institution_id DOI
        try:
            return self.institution_id.split('/')[-1]
        except:
            return None

    def get_funder_name(self):
        # Alias for institution_name parsed from the XML
        return self.institution_name
