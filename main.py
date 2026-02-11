import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/renomear', methods=['POST'])
def renomear_arquivos():
    # O FlutterFlow enviará o 'caminho' no corpo da requisição JSON
    data = request.get_json()
    pasta = data.get('caminho')
    
    if not pasta or not os.path.exists(pasta):
        return jsonify({"erro": "Caminho inválido ou não encontrado"}), 400

    resultados = []
    for nome_arquivo in os.listdir(pasta):
        caminho_antigo = os.path.join(pasta, nome_arquivo)
        
        # Evita renomear o que já foi renomeado
        if not nome_arquivo.startswith("novo_"):
            novo_nome = "novo_" + nome_arquivo
            caminho_novo = os.path.join(pasta, novo_nome)
            
            try:
                os.rename(caminho_antigo, caminho_novo)
                resultados.append(f"Sucesso: {nome_arquivo} -> {novo_nome}")
            except Exception as e:
                resultados.append(f"Erro em {nome_arquivo}: {str(e)}")

    return jsonify({"status": "processado", "detalhes": resultados})

if __name__ == "__main__":
    # O Render define a porta automaticamente via variável de ambiente
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
