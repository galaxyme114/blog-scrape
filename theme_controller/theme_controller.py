import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def get_key_by_value(dictionary, provided_value):
    for key, value in dictionary.items():    # for name, age in dictionary.iteritems():  (for Python 2.x)
        if value == provided_value:
            return key


class ThemeGeneralCSSController:
    def __init__(self):
        self.soup = None
        self.elements = None
        self.classes = None
        self.classes_and_elements = None
        self.groupings = None
        self.attributes = None
        self.attribute_values = None
        self.input_html = None
        self.output_html_file = None
        self.output_css_file = None
        self.css_string = None
        self.df = None

    def read_html(self):
        # get groupings
        self.groupings = list(self.attribute_values.keys())
        # get soup
        self.soup = BeautifulSoup(self.input_html, features="html.parser")
        # get tags
        self.elements = list(set([str(tag.name) for tag in self.soup.find('body').findChildren()]))
        # get classes
        self.classes = [str('.' + value)
                   for element in self.soup.find_all(class_=True)
                   for value in element["class"] if value
                   ]
        # put classes and tags together
        self.classes_and_elements = self.elements + self.classes

        # find the groupings that we need to address
        relevent_groupings = []
        processed_classes_and_elements = []
        for eachitem in self.classes_and_elements:
            if eachitem.replace(".", " ") not in processed_classes_and_elements:
                for grouping in self.groupings:
                    if eachitem.replace(".", "") in grouping.replace(":", " ").replace(".", " ").split():
                        relevent_groupings.append(grouping)
                        processed_classes_and_elements.extend(grouping.replace(":", " ").replace(".", " ").split())

        # keep only the groupings which are in attributes json
        self.relevant_groupings = []
        groupings_in_attribute_values = list(set(self.attribute_values))
        for relevent_grouping in relevent_groupings:
            if relevent_grouping in groupings_in_attribute_values:
                if relevent_grouping not in self.relevant_groupings:
                    self.relevant_groupings.append(relevent_grouping)


        # get the attributes for relevant groupings
        attributes = []
        for grouping in relevent_groupings:
            if grouping in self.attribute_values:
                grouping_attributes = [attribute for attribute in self.attribute_values[grouping]]
                attributes.extend(grouping_attributes)
        self.attributes = list(set(attributes))


    def get_df(self):
        self.df = pd.DataFrame(
            np.zeros((len(self.attributes), len(self.relevant_groupings)), dtype=int),
            index=self.attributes,
            columns=self.relevant_groupings
        )

    def get_df_json(self):
        return self.df.to_json()

    def set_json_df(self, df_json):
        self.df = pd.read_json(df_json)

    def sync_css(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--privileged')

        # driver = webdriver.ChromeOptions()
        driver = webdriver.Chrome(executable_path=os.path.dirname(os.path.abspath(__file__)) + '/chromedriver', chrome_options=chrome_options)
        driver.get("data:text/html;charset=utf-8," + self.input_html)  # Length limitations: 65535 characters

        for element in self.elements:
            drivers_element = driver.find_elements_by_tag_name(element)
            for driver_element in drivers_element:
                for attribute in self.attributes:
                    attribute_value = driver_element.value_of_css_property(attribute)
                    for grouping in self.groupings:
                        if element in grouping.replace(":", " ").replace(".", " ").split():
                            if attribute in self.attribute_values[grouping]:
                                property_values = self.attribute_values[grouping][attribute]
                                value_index = get_key_by_value(property_values, str(attribute_value))
                                self.df.at[attribute, grouping] = value_index
                            else:
                                print(attribute + " not found in attribute_values dictionary.")

        for eachclass in self.classes:
            drivers_eachclass = driver.find_elements_by_class_name(eachclass.replace(".", ""))
            for driver_eachclass in drivers_eachclass:
                for attribute in self.attributes:
                    attribute_value = driver_eachclass.value_of_css_property(attribute)
                    for grouping in self.groupings:
                        if eachclass.replace(".", "") in grouping.replace(":", " ").replace(".", " ").split():
                            if attribute in self.attribute_values[grouping]:
                                property_values = self.attribute_values[grouping][attribute]
                                value_index = get_key_by_value(property_values, str(attribute_value))
                                self.df.at[attribute, grouping] = value_index
                            else:
                                print(attribute + " not found in attribute_values dictionary.")

        driver.quit()

    def generate_output(self):
        css_string = ""
        for grouping in self.relevant_groupings:
            if grouping in self.attribute_values:
                css_string = css_string + " " + grouping + " { \n"
                for attribute in self.attribute_values[grouping]:
                    df_value = self.df.iloc[self.attributes.index(attribute)][grouping]
                    import math
                    import logging
                    logging.error("df_value")
                    logging.error(df_value)
                    if not math.isnan(df_value): # If we don't have that value in dictionary DIC, we don't include that in our CSS.
                        css_string = css_string + attribute + " : " + self.attribute_values[grouping][attribute][
                            df_value] + "; \n"
                css_string = css_string + " }\n"

        self.css_string = css_string

        # print css into a style tag
        new_css_tag = '<style>\n' + css_string + '</style>\n'

        # remove old style tag

        style_tags = self.soup.find('head').find_all("style")
        if style_tags:
            self.soup.find('head').find_all("style")[-1].extract()

        # attach style tag into the head of page
        new_css_tag = BeautifulSoup(
            new_css_tag, features="html.parser"
        )
        self.soup.head.insert(0, new_css_tag)

        # Output the page source
        return str(self.soup)




def calculate_euclidean_norm(vector):
    """Return the Euclidean Vector Norm."""
    return (sum([x ** 2 for x in vector])) ** 0.5


def get_euclidean_norm_rgb(rgb):
    rgb = rgb.replace('rgb(', '')
    rgb = rgb.replace(')', '')
    rgb = rgb.split(',')
    rgb_int = []
    for item in rgb:
        rgb_int.append(int(item))
    return calculate_euclidean_norm(rgb_int)

rgb_dict = {
    0: 'rgb(1,2,3)',
    1: 'rgb(1,2,4)',
    2: 'rgb(1,2,5)'
}


def find_nearest_color(rgb, rgb_dict):
    rgb_euclidean_norm = get_euclidean_norm_rgb(rgb)
    distance_dict = {}
    for item in rgb_dict.items():
        item_euclidean_norm = get_euclidean_norm_rgb(item[1])
        distance_dict[item[1]] = item_euclidean_norm - rgb_euclidean_norm

    min_distance_item = min(distance_dict.keys(), key=(lambda k: distance_dict[k]))
    return(min_distance_item)

number_dict = {
    0: '12px',
    1: '14px',
    2: '25px'
}
def find_nearest_by_number(number, number_dict):
    number = number.replace('%', '')
    number = number.replace('px', '')
    number_int = int(number)

    distance_dict = {}
    for item in number_dict.items():
        item_modified = item[1].replace('%', '')
        item_modified = item_modified.replace('px', '')
        item_int = int(item_modified)

        distance_dict[item[1]] = item_int - number_int
    min_distance_item = min(distance_dict.keys(), key=(lambda k: distance_dict[k]))
    return min_distance_item






if __name__ == "__main__":
    general_css_controlller = ThemeGeneralCSSController()
    general_css_controlller.input_html = '<head><style>.class1 { background-color: green; }</style></head><body><h1 class="class1">Hello</h1><p><a href="">Hi</a></p></body>'
    general_css_controlller.groupings = [
                ".class1 .class10 div",
                ".class2 .class3",
                "p > a:hover"
            ]
    general_css_controlller.attribute_values = {
        "p > a:hover": {
            "background-color": {
                0: "black",
                1: "green",
                2: "rgba(0, 0, 0, 0)",
            }
        },
        ".class1 .class10 div": {
            "background-color": {
                0: "black",
                1: "green",
                2: "rgba(0, 0, 0, 0)",
                3.0: "rgb(0, 128, 0)"
            }
        }
    }
    general_css_controlller.read_html()
    general_css_controlller.get_df()
    general_css_controlller.sync_css()
    print(general_css_controlller.df.to_json())
    print(general_css_controlller.generate_output())
    print(find_nearest_color('rgb(1,2,3)', rgb_dict))
    print(find_nearest_by_number('10px', number_dict))
