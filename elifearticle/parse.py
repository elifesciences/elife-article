from elifetools import parseJATS as parser
from elifetools import utils as eautils
from elifearticle import article as ea
from elifearticle import utils


def text_from_affiliation_elements(department, institution, city, country):
    """
    Given an author affiliation from
    """
    text = ""

    for element in (department, institution, city, country):
        if text != "":
            text += ", "

        if element:
            text += element

    return text


def build_contributors(authors, contrib_type):
    """
    Given a list of authors from the parser, instantiate contributors
    objects and build them
    """

    contributors = []

    for author in authors:
        contributor = None
        author_contrib_type = contrib_type

        surname = author.get("surname")
        given_name = author.get("given-names")
        collab = author.get("collab")

        # Small hack for on-behalf-of type when building authors
        #  use on-behalf-of as the contrib_type
        if author.get("type") and author.get("type") == "on-behalf-of":
            collab = author.get("on-behalf-of")
            author_contrib_type = "on-behalf-of"

        if surname or collab:
            contributor = ea.Contributor(author_contrib_type, surname, given_name, collab)

        contributor.group_author_key = author.get("group-author-key")
        contributor.orcid = author.get("orcid")
        if author.get("corresp"):
            contributor.corresp = True
        else:
            contributor.corresp = False

        # Affiliations, compile text for each
        department = []
        institution = []
        city = []
        country = []

        if author.get("affiliations"):
            for aff in author.get("affiliations"):
                department.append(aff.get("dept"))
                institution.append(aff.get("institution"))
                city.append(aff.get("city"))
                country.append(aff.get("country"))

        # Turn the set of lists into ContributorAffiliation
        for index in range(0, len(institution)):
            affiliation = ea.Affiliation()
            affiliation.department = department[index]
            affiliation.institution = institution[index]
            affiliation.city = city[index]
            affiliation.country = country[index]

            affiliation.text = text_from_affiliation_elements(
                affiliation.department,
                affiliation.institution,
                affiliation.city,
                affiliation.country)

            contributor.set_affiliation(affiliation)

        # Finally add the contributor to the list
        if contributor:
            contributors.append(contributor)

    return contributors


def build_funding(award_groups):
    """
    Given a funding data, format it
    """
    if not award_groups:
        return []

    funding_awards = []

    for award_group in award_groups:
        for id, award_group in award_group.iteritems():
            award = ea.FundingAward()

            if award_group.get('id-type') == "FundRef":
                award.institution_id = award_group.get('id')

            award.institution_name = award_group.get('institution')

            # TODO !!! Check for multiple award_id, if exists
            if award_group.get('award-id'):
                award.add_award_id(award_group.get('award-id'))

            funding_awards.append(award)

    return funding_awards


def build_ref_list(refs):
    """
    Given parsed references build a list of ref objects
    """
    ref_list = []

    for reference in refs:
        ref = ea.Citation()

        # Publcation Type
        if reference.get('publication-type'):
            ref.publication_type = reference.get('publication-type')

        # Article title
        if reference.get('full_article_title'):
            ref.article_title = reference.get('full_article_title')

        # Article title
        if reference.get('source'):
            ref.source = reference.get('source')

        # Volume
        if reference.get('volume'):
            ref.volume = reference.get('volume')

        # Issue
        if reference.get('issue'):
            ref.issue = reference.get('issue')

        # First page
        if reference.get('fpage'):
            ref.fpage = reference.get('fpage')

        # Last page
        if reference.get('lpage'):
            ref.lpage = reference.get('lpage')

        # DOI
        if reference.get('reference_id'):
            ref.doi = reference.get('reference_id')

        # Year
        if reference.get('year'):
            ref.year = reference.get('year')

        # elocation-id
        if reference.get('elocation-id'):
            ref.elocation_id = reference.get('elocation-id')

        # Authors
        if reference.get('authors'):
            for author in reference.get('authors'):
                ref_author = {}
                eautils.set_if_value(ref_author, 'group-type', author.get('group-type'))
                eautils.set_if_value(ref_author, 'surname', author.get('surname'))
                eautils.set_if_value(ref_author, 'given-names', author.get('given-names'))
                eautils.set_if_value(ref_author, 'collab', author.get('collab'))

                if len(ref_author) > 0:
                    ref.add_author(ref_author)

        ref_list.append(ref)

    return ref_list


def component_title(component):
    """
    Label, title and caption
    Title is the label text plus the title text
    Title may contain italic tag, etc.
    """

    title = u''

    label_text = u''
    title_text = u''
    if component.get('label'):
        label_text = component.get('label')

    if component.get('title'):
        title_text = component.get('title')

    title = unicode(label_text)
    if label_text != '' and title_text != '':
        title += ' '
    title += unicode(title_text)

    if component.get('type') == 'abstract' and title == '':
        title = 'Abstract'

    return title


def build_components(components):
    """
    Given parsed components build a list of component objects
    """
    component_list = []

    for comp in components:
        component = ea.Component()

        # id
        component.id = comp.get('id')

        # type
        component.type = comp.get('type')

        # asset, if available
        component.asset = comp.get('asset')

        # DOI
        component.doi = comp.get('doi')

        if component_title(comp) != '':
            component.title = component_title(comp)

        # Subtitle
        if comp.get('type') in ['supplementary-material', 'fig']:

            if comp.get('full_caption'):
                subtitle = comp.get('full_caption')
                subtitle = clean_abstract(subtitle)
                component.subtitle = subtitle

        # Mime type
        if comp.get('type') in ['abstract', 'table-wrap', 'sub-article',
                                'chem-struct-wrap', 'boxed-text']:
            component.mime_type = 'text/plain'
        if comp.get('type') in ['fig']:
            component.mime_type = 'image/tiff'
        elif comp.get('type') in ['media', 'supplementary-material']:
            if comp.get('mimetype') and comp.get('mime-subtype'):
                component.mime_type = (comp.get('mimetype') + '/'
                                       + comp.get('mime-subtype'))

        # Permissions
        component.permissions = comp.get('permissions')

        # Append it to our list of components
        component_list.append(component)

    return component_list


def build_related_articles(related_articles):
    """
    Given parsed data build a list of related article objects
    """
    article_list = []

    for related_article in related_articles:
        article = ea.RelatedArticle()
        if related_article.get('xlink_href'):
            article.xlink_href = related_article.get('xlink_href')
        if related_article.get('related_article_type'):
            article.related_article_type = related_article.get('related_article_type')
        if related_article.get('ext_link_type'):
            article.ext_link_type = related_article.get('ext_link_type')

        # Append it to our list
        article_list.append(article)

    return article_list


def build_pub_dates(article, pub_dates):
    for pub_date in pub_dates:
        # always want a date type, take it from pub-type if must
        if pub_date.get('date-type'):
            date_instance = ea.ArticleDate(pub_date.get('date-type'),
                                           pub_date.get('date'))
        elif pub_date.get('pub-type'):
            date_instance = ea.ArticleDate(pub_date.get('pub-type'),
                                           pub_date.get('date'))
        # Set more values
        utils.set_attr_if_value(date_instance, 'pub_type', pub_date.get('pub-type'))
        utils.set_attr_if_value(date_instance, 'publication_format',
                                pub_date.get('publication-format'))
        utils.set_attr_if_value(date_instance, 'day', pub_date.get('day'))
        utils.set_attr_if_value(date_instance, 'month', pub_date.get('month'))
        utils.set_attr_if_value(date_instance, 'year', pub_date.get('year'))
        article.add_date(date_instance)


def clean_abstract(abstract):
    """
    Remove unwanted tags from abstract string,
    parsing it as HTML, then only keep the body paragraph contents
    """

    remove_tags = ['xref', 'ext-link', 'inline-formula', 'mml:*']
    for tag_name in remove_tags:
        abstract = utils.remove_tag(tag_name, abstract)

    return abstract


def build_part_check(part, build_parts):
    """
    check if only specific parts were specified to be build when parsing
    if the list build_parts is empty, then all parts will be parsed
    """
    if len(build_parts) == 0:
        return True
    else:
        if part in build_parts:
            return True
        else:
            return False


def build_article_from_xml(article_xml_filename, detail="brief", build_parts=[]):
    """
    Parse JATS XML with elifetools parser, and populate an
    eLifePOA article object
    Basic data crossref needs: article_id, doi, title, contributors with names set
    detail="brief" is normally enough,
    detail="full" will populate all the contributor affiliations that are linked by xref tags
    """
    build_part = lambda part: build_part_check(part, build_parts)

    error_count = 0

    soup = parser.parse_document(article_xml_filename)

    # Get DOI
    doi = parser.doi(soup)

    # Create the article object
    article = ea.Article(doi, title=None)

    # journal title
    if build_part('basic'):
        article.journal_title = parser.journal_title(soup)

    # issn
    if build_part('basic'):
        article.journal_issn = parser.journal_issn(soup, "electronic")
        if article.journal_issn is None:
            article.journal_issn = parser.journal_issn(soup)

    # Related articles
    if build_part('related_articles'):
        article.related_articles = build_related_articles(parser.related_article(soup))

    # Get publisher_id and set object manuscript value
    if build_part('basic'):
        publisher_id = parser.publisher_id(soup)
        if not publisher_id and doi:
            # try to get it from the DOI
            publisher_id = doi.split('.')[-1]
        article.manuscript = publisher_id

    # Set the articleType
    if build_part('basic'):
        article_type = parser.article_type(soup)
        if article_type:
            article.articleType = article_type

    # title
    if build_part('basic'):
        article.title = parser.full_title(soup)
    #print article.title

    # abstract
    if build_part('abstract'):
        article.abstract = clean_abstract(parser.full_abstract(soup))

    # digest
    if build_part('abstract'):
        article.digest = clean_abstract(parser.full_digest(soup))

    # elocation-id
    if build_part('basic'):
        article.elocation_id = parser.elocation_id(soup)

    # contributors
    if build_part('contributors'):
        all_contributors = parser.contributors(soup, detail)
        author_contributors = filter(lambda con: con.get('type')
                                     in ['author', 'on-behalf-of'], all_contributors)
        contrib_type = "author"
        contributors = build_contributors(author_contributors, contrib_type)
    
        contrib_type = "author non-byline"
        authors = parser.authors_non_byline(soup, detail)
        contributors_non_byline = build_contributors(authors, contrib_type)
        article.contributors = contributors + contributors_non_byline

    # license href
    if build_part('license'):
        license = ea.License()
        license.href = parser.license_url(soup)
        article.license = license

    # article_category
    if build_part('categories'):
        article.article_categories = parser.category(soup)

    # keywords
    if build_part('keywords'):
        article.author_keywords = parser.keywords(soup)

    # research organisms
    if build_part('research_organisms'):
        article.research_organisms = parser.research_organism(soup)

    # funding awards
    if build_part('funding'):
        article.funding_awards = build_funding(parser.full_award_groups(soup))

    # references or citations
    if build_part('references'):
        article.ref_list = build_ref_list(parser.refs(soup))

    # components with component DOI
    if build_part('components'):
        article.component_list = build_components(parser.components(soup))

    # History dates
    if build_part('history'):
        date_types = ["received", "accepted"]
        for date_type in date_types:
            history_date = parser.history_date(soup, date_type)
            if history_date:
                date_instance = ea.ArticleDate(date_type, history_date)
                article.add_date(date_instance)

    # Pub date
    if build_part('pub_dates'):
        build_pub_dates(article, parser.pub_dates(soup))

    # Set the volume if present
    if build_part('volume'):
        volume = parser.volume(soup)
        if volume:
            article.volume = volume

    if build_part('is_poa'):
        article.is_poa = parser.is_poa(soup)

    return article, error_count


def build_articles_from_article_xmls(article_xmls, detail="full", build_parts=[]):
    """
    Given a list of article XML filenames, convert to article objects
    """

    poa_articles = []

    for article_xml in article_xmls:
        print "working on ", article_xml
        article, error_count = build_article_from_xml(article_xml, detail, build_parts)
        if error_count == 0:
            poa_articles.append(article)

    return poa_articles
