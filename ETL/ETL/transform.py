# Libraries
import pandas as pd
import numpy as np
from datetime import datetime

# Lists of the schema
"""
    Obtain the following information per article:
        _id
        web_url
        abstract
        print_section
        print_page
        main headline
        count of multimedia elements
        average of multimedia height elements
        median of multimedia width elements
        count of keywords elements
        document_type
        pub_date formatted as YYYY-MM-DD
        word_count
"""

ids = []
web_urls = []
abstracts = []
print_sections = []
print_pages = []
main_headlines = []
multimedia_counts = []
average_of_heights = []
median_of_widths = []
keywords_counts = []
document_types = []
pub_dates = []
word_counts = []


def extract_info_from_response_json(json_data):
    """
    :param json_data:
    :return: None
    process = extract each solicited item from the json
    result = appends the values to the lists of the schema
    """
    docs = json_data['response']['docs']

    for doc in docs:

        # /response/docs/n/_id
        id_ = doc["_id"] if "_id" in doc else None
        ids.append(id_)

        # web_url
        # /response/docs/n/web_url
        web_url = doc["web_url"] if "web_url" in doc else None
        web_urls.append(web_url)

        # abstract
        # /response/docs/n/abstract
        abstract = doc['abstract'] if 'abstract' in doc else None
        abstracts.append(abstract)

        # print_section
        # /response/docs/n/print_section
        print_section = doc['print_section'] if 'print_section' in doc else None
        print_sections.append(print_section)

        # print_page
        # /response/docs/n/print_page
        print_page = doc['print_page'] if 'print_page' in doc else None
        print_pages.append(print_page)

        # main headline
        # /response/docs/n/headline/main
        main_headline = doc['headline']['main'] if 'headline' in doc else None
        main_headlines.append(main_headline)

        # multimedia_count
        # /response/docs/n/multimedia
        if 'multimedia' in doc:
            multimedia = doc['multimedia']
            multimedia_count = len(multimedia)
            heights = []
            widths = []
            for m in multimedia:
                heights.append(m['height'])
                widths.append(m['width'])

            heights = np.array(heights)
            widths = np.array(widths)

            average_height = np.mean(heights) if len(heights) > 0 else None
            median_width = np.median(widths) if len(widths) > 0 else None

        else:
            multimedia_count = None
            average_height = None
            median_width = None

        multimedia_counts.append(multimedia_count)
        average_of_heights.append(average_height)
        median_of_widths.append(median_width)

        # keywords
        # /response/docs/n/keywords
        keywords_count = len(doc['keywords']) if 'keywords' in doc else None
        keywords_counts.append(keywords_count)

        # document_type
        # /response/docs/n/document_type
        document_type = doc['document_type'] if 'document_type' in doc else None
        document_types.append(document_type)

        # pub_date
        # /response/docs/n/pub_date
        # Example of input "2024-05-03T10:33:20+0000"
        if 'pub_date' in doc:
            pub_date = datetime.strptime(doc['pub_date'], "%Y-%m-%dT%H:%M:%S%z")
            pub_date = pub_date.strftime("%Y-%m-%d")
        else:
            pub_date = None
        pub_dates.append(pub_date)

        # word_count
        # /response/docs/n/word_count
        word_count = doc['word_count'] if 'word_count' in doc else None
        word_counts.append(word_count)


# Main function of transformation
def transform_data(jsons):

    # Iteration to scan each json
    for index, json_ in enumerate(jsons):

        # Applying the function to extract the data that I defined previously
        extract_info_from_response_json(json_)
        print(f'json number {index + 1} has been processed')

    # Transforming the lists to a dataframe using pandas
    df = pd.DataFrame(
        data={
            'id': ids,
            'web_url': web_urls,
            'abstract': abstracts,
            'print_sections': print_sections,
            'print_pages': print_pages,
            'main_headline': main_headlines,
            'multimedia_count': multimedia_counts,
            'average_of_height': average_of_heights,
            'median_of_width': median_of_widths,
            'keywords_count': keywords_counts,
            'document_type': document_types,
            'pub_date': pub_dates,
            'word_count': word_counts
        }
    )

    return df