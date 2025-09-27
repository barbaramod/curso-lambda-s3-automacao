# curso-lambda-s3-automacao
Automação de infraestrutura na A# 🚀 AWS Lambda + S3 + DynamoDB

Projeto desenvolvido no curso **“Executando Tarefas Automatizadas com Lambda Function e S3”**.

Automação de infraestrutura na AWS com **CloudFormation**, **Lambda**, **S3** e **DynamoDB** para processamento de notas fiscais.

Este projeto implementa um sistema **serverless** onde:

1. Um arquivo JSON é enviado para o **Amazon S3**.
2. O upload aciona uma função **Lambda**.
3. A função valida os dados e grava no **DynamoDB**.
4. Os registros podem ser consultados via **API Gateway**.

---

## 📂 Estrutura do Repositório

```
📂 aws-lambda-s3-dynamodb
 ┣ 📂 src
 ┃ ┗ grava_db.py                # Código da função Lambda
 ┣ template-cloudformation.yaml # Template IaC (CloudFormation)
 ┣ README.md                    # Documentação
```

---

## 🛠️ Tecnologias e Serviços Utilizados

* **Amazon S3** → armazenamento de arquivos
* **AWS Lambda** → processamento serverless
* **Amazon DynamoDB** → banco NoSQL para persistência
* **IAM** → permissões e segurança
* **Amazon API Gateway** → exposição da API REST
* **AWS CloudFormation** → automação da infraestrutura

---

## 📜 Exemplo de JSON de Nota Fiscal

```json
{
  "id": "NF-10",
  "cliente": "João Silva",
  "valor": "3479.62",
  "data_emissao": "2025-01-27"
}
```

---

## ⚙️ Como Executar

### 1. Empacotar a função Lambda

Na pasta `src`, compacte o código em um `.zip`:

```bash
cd src
zip grava_db.zip grava_db.py
```

### 2. Enviar o pacote para o S3

Crie um bucket temporário para armazenar o código da Lambda e faça upload:

```bash
aws s3 mb s3://meu-bucket-lambda-codigo
aws s3 cp grava_db.zip s3://meu-bucket-lambda-codigo/lambda/grava_db.zip
```

⚠️ Atualize o nome do bucket no arquivo **`template-cloudformation.yaml`** na seção `ProcessaNotasLambda > Code > S3Bucket`.

---

### 3. Criar a Stack com CloudFormation

```bash
aws cloudformation create-stack \
  --stack-name notas-fiscais-stack \
  --template-body file://template-cloudformation.yaml \
  --capabilities CAPABILITY_IAM
```

---

### 4. Testar a solução

* Fazer upload de um JSON no bucket criado:

```bash
aws s3 cp exemplo.json s3://<NOME_DO_BUCKET>/
```

* Consultar dados no DynamoDB:

```bash
aws dynamodb scan --table-name NotasFiscais
```

* Testar API Gateway com **curl** ou Postman:

**Inserir nota fiscal:**

```bash
curl -X POST https://<API_GATEWAY_URL>/notas \
  -H "Content-Type: application/json" \
  -d '{"id":"NF-10","cliente":"João Silva","valor":"3479.62","data_emissao":"2025-01-27"}'
```

**Consultar nota fiscal:**

```bash
curl -X GET "https://<API_GATEWAY_URL>/notas?id=NF-10"
```

---

## ✅ Conclusão

Este desafio permitiu consolidar conhecimentos sobre **serverless na AWS** e **automação de infraestrutura com CloudFormation**, aplicando conceitos práticos de integração entre serviços em nuvem.
WS com CloudFormation, Lambda, S3 e DynamoDB para processamento de notas fiscais.
