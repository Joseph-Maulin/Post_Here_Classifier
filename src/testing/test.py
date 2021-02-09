

from flask import Flask, render_template, request
import json
from Load_Model_H5 import Model


model = Model()
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def test():
    try:
        a = request.get_json()
        predictions = [x[0] for x in model.make_prediction(a)]

        return json.dumps({"prediction": predictions})

    except:
        return "error"



if __name__ == "__main__":
    app.run(debug=True)
