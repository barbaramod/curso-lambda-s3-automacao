```python
import boto3
import json
import os

# Conectar ao DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('NotasFiscais')

def validar_registro(registro):
    """Valida se o registro contém os campos obrigatórios"""
    campos = ["id", "cliente", "valor", "data_emissao"]
    return all(campo in registro for campo in campos)

def inserir_registros(event):
    """Insere registros no DynamoDB"""
    try:
        body = event.get("body")
        if body:
            registro = json.loads(body)
        else:
            registro = event  # caso seja disparado pelo S3

        if not validar_registro(registro):
            return {"statusCode": 400, "body": json.dumps({"erro": "Registro inválido"})}

        table.put_item(Item=registro)
        return {"statusCode": 200, "body": json.dumps({"mensagem": "Registro inserido com sucesso"})}

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"erro": str(e)})}

def consultar_registro(event):
    """Consulta registros no DynamoDB"""
    try:
        params = event.get("queryStringParameters", {})
        if not params or "id" not in params:
            return {"statusCode": 400, "body": json.dumps({"erro": "Informe o parâmetro id"})}

        response = table.get_item(Key={"id": params["id"]})
        if "Item" not in response:
            return {"statusCode": 404, "body": json.dumps({"erro": "Registro não encontrado"})}

        return {"statusCode": 200, "body": json.dumps(response["Item"])}

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"erro": str(e)})}

def lambda_handler(event, context):
    """Função principal que roteia os eventos do API Gateway e do S3"""
    print("Evento recebido:", json.dumps(event))

    # Se o evento vier do API Gateway
    if "httpMethod" in event:
        method = event["httpMethod"]
        if method == "POST":
            return inserir_registros(event)
        elif method == "GET":
            return consultar_registro(event)

    # Se o evento vier do S3
    if "Records" in event and event["Records"][0]["eventSource"] == "aws:s3":
        # Exemplo: aqui você pode ler o arquivo do S3 e processar
        s3 = boto3.client("s3")
        bucket = event["Records"][0]["s3"]["bucket"]["name"]
        key = event["Records"][0]["s3"]["object"]["key"]

        obj = s3.get_object(Bucket=bucket, Key=key)
        registro = json.loads(obj["Body"].read().decode("utf-8"))

        return inserir_registros(registro)

    return {"statusCode": 400, "body": json.dumps({"erro": "Evento não suportado"})}
```
