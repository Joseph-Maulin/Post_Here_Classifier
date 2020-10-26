

import requests








response = requests.get("http://127.0.0.1:5000", json={"post_title":"hello",
                                          "post_text":"hello from me to you"})

print(response.text)
