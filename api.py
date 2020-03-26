import random
import uuid
import velha
import messages
import json
from flask import Flask, request, redirect, url_for, render_template, json, testing, Response, jsonify, make_response

app = Flask(__name__)
app.config["DEBUG"] = True

# Dicionário para guardar os objetos jogo da velha criados.
gameDict = {}

@app.route('/testGame', methods=['GET'])
# Método que trata a rota /testGame e testa POST - /game.
def testGame():
    with app.test_client() as c:
        return c.post('/game')

@app.route('/testMovement', methods=['GET'])
# Método que trata a rota /testMovement e testa POST - /game/{id}/movement.
def testMovement():
    with app.test_client() as c:
        id = request.args.get('id')
        player = request.args.get('player')
        x = request.args.get('x')
        y = request.args.get('y')
        return c.post('/game/' + id + '/movement', json={
            "id" : id,
            "player" : player,
            "position" : {
                "x" : x,
                "y" : y
            }
        })

@app.route('/game', methods=['GET', 'POST'])
# Método que trata a rota /game, cria um novo jogo e o adiciona no dicionário de jogos da velha.
def game():
    if request.method == 'POST':
        newGame = velha.Game()
        gameDict[newGame.id] = newGame
        return {
            "id" : newGame.id,
            "firstPlayer" : newGame.turno
        }
    else:
        return "<h1>A request tem que ser do tipo POST.</h1>"

@app.route("/game/<string:id>/movement", methods=['POST'])
# Método que trata a rota /game/{id}/movement, efetua mudanças no jogo de acordo com os parâmetros recebidos e retorna saídas de acordo.
def jogada(id):
    if request.method == 'POST':
        try:
            # Recupera os dados do json recebido.
            json_data = request.get_json()
            player = json_data["player"]
            x = int(json_data["position"]["x"])
            y = int(json_data["position"]["y"])

            # Se o id do jogo não existir no dicionário, retorna uma mensagem e código.
            if id not in gameDict:
                return make_response(jsonify(msg=messages.MSG_GameNotFound), 201)
            # Se o jogador recebido não for o jogador do turno, retorna uma mensagem e código.
            if player != gameDict[id].turno:
                return make_response(jsonify(msg=messages.MSG_NotPlayerTurn), 201)

            # Se o tabuleiro já possuir uma jogada nesta célula, retorna uma mensagem e código.
            if gameDict[id].tabuleiro[x][y] != None:
                return make_response(jsonify(msg=messages.MSG_AlreadyPlayed), 201)

            # Do contrário, registra a jogada e atualiza o próximo jogador.
            gameDict[id].tabuleiro[x][y] = player
            if(gameDict[id].turno == "X"):
                gameDict[id].turno = "O"
            else:
                gameDict[id].turno = "X"
            
            vencedor = velha.fimDoJogo(gameDict[id].tabuleiro)
            # Se houver vencedor, retorna mensagem, vencedor e código.
            if(vencedor[0] == True):
                gameDict[id].vencedor = True
                gameDict[id].turno = vencedor[1]
                return make_response(jsonify(msg=messages.MSG_GameFinished, winner=gameDict[id].turno), 200)
            
            # Se o jogo deu em velha, retorna mensagem correspondente e código.
            if(vencedor[0] == False and vencedor[1] == "velha"):
                gameDict[id].empate = True
                return make_response(jsonify(msg=messages.MSG_GameFinished, winner=messages.MSG_Draw), 200)

            # Se não houve vencedor ou velha ainda, retorna código 200.
            return Response(status=200)

        except:
            print(messages.MSG_GenericError)

app.run()