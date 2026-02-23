from flask import Flask, render_template, request
import requests


app = Flask(__name__)
# Sua chave da OpenWeather aqui
API_KEY = "apikey"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clima', methods=['POST'])
def clima():
    cidade = request.form.get('cidade')
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&lang=pt_br&units=metric"
    
    try:
        resposta = requests.get(url)
        dados = resposta.json()

        if dados.get("cod") == 200:
            # Organizando os dados para o frontend
            info = {
                "nome": dados["name"],
                "temp": round(dados["main"]["temp"]),
                "descricao": dados["weather"][0]["description"].capitalize(),
                "humidade": dados["main"]["humidity"],
                "clima_main": dados["weather"][0]["main"].lower() # Para mudar a cor depois
            }
            return render_template('index.html', clima=info)
        else:
            return render_template('index.html', erro="Cidade não encontrada!")
            
    except Exception as e:
        return render_template('index.html', erro="Falha na conexão com a API")

if __name__ == '__main__':
    app.run(debug=True)