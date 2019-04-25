import requests, json, csv
from datetime import datetime
from bs4 import BeautifulSoup
from urllib import parse

START_URL = "https://www.coursera.org/about/partners/us"
FILENAME = "courses_cache.json"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
DEBUG = True


class Cache:
    def __init__(self, filename):
        """Load cache from disk, if present"""
        self.filename = filename
        try:
            with open(self.filename, 'r') as cache_file:
                cache_json = cache_file.read()
                self.cache_diction = json.loads(cache_json)
        except:
            self.cache_diction = {}

    def _save_to_disk(self):
        """Save cache to disk"""
        with open(self.filename, 'w') as cache_file:
            cache_json = json.dumps(self.cache_diction)
            cache_file.write(cache_json)

    def _has_entry_expired(self, timestamp_str, expire_in_days):
        now = datetime.now()
        cache_timestamp = datetime.strptime(timestamp_str, DATETIME_FORMAT)
        delta = now - cache_timestamp
        delta_in_days = delta.days
        if delta_in_days > expire_in_days:
            return True
        else:
            return False

    def get(self, identifier):
        identifier = identifier.upper() # Assuming none will differ with case sensitivity here
        if identifier in self.cache_diction:
            data_assoc_dict = self.cache_diction[identifier]
            if self._has_entry_expired(data_assoc_dict['timestamp'],data_assoc_dict['expire_in_days']):
                if DEBUG:
                    print("Cache has expired for {}".format(identifier))
                # also remove old copy from cache
                del self.cache_diction[identifier]
                self._save_to_disk()
                data = None
            else:
                data = data_assoc_dict['values']
        else:
            data = None
        return data

    def set(self, identifier, data, expire_in_days=7):
        """Add identifier and its associated values (literal data) to the cache, and save the cache as json"""
        identifier = identifier.upper() # make unique
        self.cache_diction[identifier] = {
            'values': data,
            'timestamp': datetime.now().strftime(DATETIME_FORMAT),
            'expire_in_days': expire_in_days
        }
        self._save_to_disk()


PROGRAM_CACHE = Cache(FILENAME)

data = {}
class Spider:
    def access_page_data(url):
        data = PROGRAM_CACHE.get(url)
        if not data:
            data = requests.get(url).text
            PROGRAM_CACHE.set(url, data)
        return data

    main_page = access_page_data(START_URL)
    main_soup = BeautifulSoup(main_page, features="html.parser")
    list_of_topics = main_soup.find('div', {'class':'rc-PartnerBoxes horizontal-box wrap'})
    all_links = list_of_topics.find_all('a')

    topics_pages = []
    new_urls = []
    for l in all_links:
        new_url = l['href']
        new_full_url = parse.urljoin(START_URL, new_url)
        new_urls.append(new_full_url)




    courses = []
    instructors = []
    cont = 0
    for url in new_urls:
        cont +=1
        courses = []
        instructors = []
        if url == 'https://www.coursera.org/learnquest':
            continue
        elif url =='https://www.cmu.edu/me/':
            continue
        elif url =='https://www.coursera.org/nyif':
            continue
        elif url == 'https://www.coursera.org/hubspot-academy':
            continue
        elif url == 'https://www.coursera.org/tufts':
            continue
        else:
            page = access_page_data(url)
            print(cont, url)
            soup = BeautifulSoup(page, features="html.parser")
            university_name = soup.find('h1', class_='display-4-text')
            if university_name == None:
                continue
            else:
                university_name = university_name.get_text()
                course_node = soup.find('div',{'class':'bt3-col-md-12'})
                all_courses = course_node.find_all('div',{'class':'name headline-1-text'})
                for c in all_courses:
                    course_name = c.get_text()
                    courses.append(course_name)

                all_instructors = soup.find_all('h4', {'class': 'instructorName headline-1-text'})
                for i in all_instructors:
                    name = i.get_text()
                    instructors.append(name)
                data[university_name]={'courses': courses, 'instructors':instructors}


with open("courses.json", "w", encoding='utf8', newline='') as fp:
    json.dump(data, fp)

