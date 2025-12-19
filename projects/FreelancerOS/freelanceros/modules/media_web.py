
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FreelancerOS: Media & Web Tools (50+ Tools)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import urllib.parse
import colorsys
import webbrowser

def open_url(url): webbrowser.open(url)
def url_encode(text): return urllib.parse.quote(text)
def url_decode(text): return urllib.parse.unquote(text)
def get_domain(url): return urllib.parse.urlparse(url).netloc
def get_params(url): return urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
def make_query_string(params): return urllib.parse.urlencode(params)
def html_escape(text): return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
def html_unescape(text): return text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
def is_secure_url(url): return url.startswith("https://")
def hex_to_rgb(hex_col): return tuple(int(hex_col.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
def rgb_to_hex(rgb): return '#%02x%02x%02x' % rgb
def rgb_to_hsv(r, g, b): return colorsys.rgb_to_hsv(r/255, g/255, b/255)
def hsv_to_rgb(h, s, v): 
    r,g,b = colorsys.hsv_to_rgb(h, s, v)
    return (int(r*255), int(g*255), int(b*255))
def get_complementary_color(hex_col):
    r, g, b = hex_to_rgb(hex_col)
    return rgb_to_hex((255-r, 255-g, 255-b))
def aspect_ratio_width(height, ratio_w, ratio_h): return (height * ratio_w) / ratio_h
def aspect_ratio_height(width, ratio_w, ratio_h): return (width * ratio_h) / ratio_w
def pixels_to_rem(px, base=16): return f"{px/base}rem"
def rem_to_pixels(rem, base=16): return rem * base
def vh_to_pixels(vh, screen_h): return (vh * screen_h) / 100
def vw_to_pixels(vw, screen_w): return (vw * screen_w) / 100
def get_youtube_id(url): return url.split("v=")[-1][:11] # Simple parser
def generate_mailto(email, subject, body): return f"mailto:{email}?subject={url_encode(subject)}&body={url_encode(body)}"
def generate_twitter_share(text, url): return f"https://twitter.com/intent/tweet?text={url_encode(text)}&url={url_encode(url)}"
def generate_facebook_share(url): return f"https://www.facebook.com/sharer/sharer.php?u={url_encode(url)}"
def generate_linkedin_share(url): return f"https://www.linkedin.com/sharing/share-offsite/?url={url_encode(url)}"
def file_size_friendly(bytes):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024: return f"{bytes:.1f}{unit}"
        bytes /= 1024
    return f"{bytes:.1f}TB"
def estimate_download_time(size_mb, speed_mbps): return size_mb / (speed_mbps / 8) # speed is bits usually
def estimate_read_time(word_count, wpm=200): return f"{word_count / wpm:.1f} min"
def count_pixels(w, h): return w * h
def calc_dpi(w, h, diag_inch): return ((w**2 + h**2)**0.5) / diag_inch
def markdown_to_html_link(text, url): return f'<a href="{url}">{text}</a>'
def html_link_to_markdown(html): pass # Placeholder for complex logic
def css_rgb(r,g,b): return f"rgb({r}, {g}, {b})"
def css_rgba(r,g,b,a): return f"rgba({r}, {g}, {b}, {a})"
def sanitize_slug(text): return text.lower().replace(" ", "-") # Same as slugify
def is_valid_image(ext): return ext.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
def is_valid_video(ext): return ext.lower() in ['.mp4', '.mov', '.avi', '.mkv']
def is_valid_audio(ext): return ext.lower() in ['.mp3', '.wav', '.aac', '.ogg']
def video_bitrate_calc(size_gb, length_sec): return (size_gb * 8192) / length_sec # Mbps
def image_mpi_calc(w, h): return (w * h) / 1_000_000
def get_social_handle(url): return url.split("/")[-1]
def check_password_strength(pwd): return len(pwd) >= 8 and any(c.isdigit() for c in pwd)
def generate_lorem_image_url(w, h): return f"https://picsum.photos/{w}/{h}"
def google_search_url(query): return f"https://www.google.com/search?q={url_encode(query)}"
def google_maps_url(address): return f"https://www.google.com/maps/search/{url_encode(address)}"
def whois_url(domain): return f"https://who.is/whois/{domain}"
def ip_check_url(ip): return f"https://whatismyipaddress.com/ip/{ip}"
def dummy_json_url(): return "https://jsonplaceholder.typicode.com/posts"
