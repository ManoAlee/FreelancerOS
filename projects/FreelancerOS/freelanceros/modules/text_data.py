
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FreelancerOS: Text & Data Processing (50+ Tools)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import re
import json
import base64
import random
import string

def count_words(text): return len(text.split())
def count_chars(text): return len(text)
def count_chars_no_space(text): return len(text.replace(" ", ""))
def to_upper(text): return text.upper()
def to_lower(text): return text.lower()
def to_title(text): return text.title()
def to_sentence(text): return text.capitalize()
def reverse_text(text): return text[::-1]
def is_palindrome(text): return text == text[::-1]
def truncate(text, length=100): return text[:length] + "..." if len(text) > length else text
def slugify(text): return text.lower().replace(" ", "-").replace(".", "")
def snake_case(text): return text.lower().replace(" ", "_")
def camel_case(text): return ''.join(word.title() for word in text.split(' '))
def kebab_case(text): return text.lower().replace(" ", "-")
def strip_html(text): return re.sub('<[^<]+?>', '', text)
def extract_emails(text): return re.findall(r'[\w\.-]+@[\w\.-]+', text)
def extract_urls(text): return re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
def extract_hashtags(text): return re.findall(r'#(\w+)', text)
def extract_mentions(text): return re.findall(r'@(\w+)', text)
def extract_numbers(text): return re.findall(r'\d+', text)
def extract_phones(text): return re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text) # Basic US
def remove_punctuation(text): return re.sub(r'[^\w\s]', '', text)
def remove_numbers(text): return re.sub(r'\d+', '', text)
def remove_extra_spaces(text): return " ".join(text.split())
def replace_text(text, old, new): return text.replace(old, new)
def count_occurrences(text, sub): return text.count(sub)
def base64_encode(text): return base64.b64encode(text.encode()).decode()
def base64_decode(text): return base64.b64decode(text.encode()).decode()
def json_stringify(data): return json.dumps(data)
def json_parse(text): return json.loads(text)
def simple_encrypt(text, shift=1): return "".join([chr(ord(c)+shift) for c in text]) # Caesar
def simple_decrypt(text, shift=1): return "".join([chr(ord(c)-shift) for c in text])
def generate_password(length=12): return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
def generate_uuid(): import uuid; return str(uuid.uuid4())
def lorem_ipsum(words=10): return " ".join(["lorem", "ipsum", "dolor", "sit", "amet"] * (words // 5))
def format_currency(amount, symbol="$"): return f"{symbol}{amount:,.2f}"
def mask_email(email): return email[0] + "***" + email[email.find('@'):]
def mask_credit_card(cc): return "****-****-****-" + cc[-4:]
def get_file_extension(filename): return filename.split('.')[-1] if '.' in filename else ''
def get_filename_no_ext(filename): return filename.split('.')[0]
def sort_list_asc(lst): return sorted(lst)
def sort_list_desc(lst): return sorted(lst, reverse=True)
def remove_duplicates(lst): return list(set(lst))
def flatten_list(lst): return [item for sublist in lst for item in sublist]
def list_to_csv(lst): return ",".join(map(str, lst))
def csv_to_list(text): return text.split(",")
def chunks(lst, n): return [lst[i:i + n] for i in range(0, len(lst), n)]
def shuffle_list(lst): random.shuffle(lst); return lst
def random_item(lst): return random.choice(lst)
def text_similarity(a, b): return len(set(a) & set(b)) / len(set(a) | set(b)) * 100 # Jaccard
def rot13(text): return text.translate(str.maketrans("ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz", "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm"))
def count_lines(text): return len(text.splitlines())
