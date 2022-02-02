from flask import Flask, render_template, url_for, request
import pickle
import numpy as np

# Implementation du model
with open("pickle_model.pkl", 'rb') as file:
    pickle_model = pickle.load(file)

# initialisation de l'application flask
app = Flask(__name__)


def isValid(input):
    # on verifie la data en essayant de la transformer en float
    try:

        res = [float(e) for e in input]
        return True
    except:
        return False

# configuration du premeir endpoint


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        '''
        si on a reçu une requêtte post on va d'abord verfier que les donnes sont bien des nombre
        puis on va prédire en utilisant notre classifieur
        '''
        data = request.form.to_dict()
        name = data['name']
        del data['name']  # on aura pas besion pour faire la prédiction
        data_values = list(data.values())
        print(data_values)
        if isValid(data_values):
            # transformer les valeurs text en float
            values = list(map(lambda x: float(x), data_values))
            # convertir en format(1,) pour pouvoire prédire avec le model
            values = np.array(values).reshape(1, -1)

            result = int(pickle_model.predict(values)[0])  # prédiction ....
            if result == 1:
                outcome = "  vaut le coup d'investir sur lui car il va durer plus de 5 ans en NBA"
            if result == 0:
                outcome = "  NE vaut PAS le coup d'investir sur lui car il va durer plus de 5 ans en NBA"
            # affichage du résulta
            return render_template('result.html', outcome=outcome, name=name)
        else:
            outcome = 'les données que vous avez mis ne sont pas corrects !'
            return render_template('index.html', outcome=outcome, name='')

    if request.method == 'GET':
        outcome = 'pas de prediction encore !'
        return render_template('index.html', outcome=outcome, name='')

# si on va dans un endpoint qui n'existe pas


@app.errorhandler(404)
def notFound(error):
    return render_template('notFound.html')


if __name__ == "__main__":
    app.run(debug=True)
