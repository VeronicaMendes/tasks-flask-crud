from flask import Flask, request, jsonify
from models.task import Task

app = Flask(__name__)

# CRUD
# Create, Read, Update and Delete = Criar, Ler, Atualizar, Deletar
# Tabela: Tarefa

tasks = []
task_id_control = 1

"""Esse é um decorator que indica que essa função (create_task) será 
chamada quando o cliente fizer uma requisição POST para o endereço /tasks.
    @app.route(...) define uma rota, ou seja, uma URL que o servidor vai "escutar".
    methods=["POST"] diz que só aceita requisições POST (que geralmente são 
    usadas para criar dados)."""
@app.route('/tasks', methods=["POST"])
def create_task():
  global task_id_control
  #Aqui está pegando os dados enviados pelo cliente no corpo da requisição, no formato JSON.
  data = request.get_json()
  new_task = Task(id=task_id_control ,title=data['title'], description=data.get("description", ""))
  task_id_control += 1
  tasks.append(new_task)
  print(tasks)
  return jsonify({"mesagem": "Nova tarefa criada com sucesso"})

@app.route('/tasks', methods=['GET'])
def get_tasks():
  task_list = [task.to_dict() for task in tasks]

  output = {
      "tasks": task_list,
      "total_tasks": len(task_list)
  }
  return jsonify(output)

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
  task = None 
  for i in tasks:
    if i.id == id:
      return jsonify(i.to_dict())
    
  return jsonify({"message": "Não foi possivel encontrar a atividade"}), 404

@app.route('/tasks/<int:id>', methods=["PUT"])
def update_task(id):
  task = None
  for i in tasks:
    if i.id == id:
      task = i
      break
  print(task)

  if task == None:
    return jsonify({"message": "Não foi possivel encontrar a atividade"}), 404
  
  data = request.get_json()
  task.title = data['title']
  task.description = data['description']
  task.completed = data['completed']
  print(task)

  return jsonify({"message": "Tarefa atualizada com sucesso!"})

@app.route('/tasks/<int:id>', methods=["DELETE"])
def delete_task(id):
  task = None
  for i in tasks:
    print(i.to_dict)
    if i.id == id:
      task = i 
      break
  
  if not task:
    return jsonify({"message": "Não foi possivel encontrar a atividade!"}), 404
  
  tasks.remove(task)
  return jsonify({"message": "Tarefa deletada com sucesso!"})

if __name__ == "__main__":
  app.run(debug=True)