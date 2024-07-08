
# Configuração do Spark em um Único Nó no Docker

Esta é uma configuração do Apache Spark em um único nó para testar o Apache Spark e para fins de aprendizado. Esta é uma alternativa às máquinas virtuais que são grandes em volume e consomem muitos recursos.

Para construir a imagem Docker, execute o comando abaixo:
```
docker-compose --build
```

```bash
$ sudo docker-compose up --build
```

Para entrar dentro do terminal do container
```bash
$ sudo docker exec -it spark1n /bin/bash
```


Use a seguinte URL para acessar o Jupyter Notebook: [http://localhost:4041](http://localhost:4041)

Para lançar o `pyspark`, você precisa modificar o Dockerfile descomentando a linha `#CMD ["sh", "-c", "tail -f /dev/null"]` e comentando a última linha. Então você pode acessar o contêiner e digitar `pyspark` como mostrado abaixo:

![pyspark_terminal](resources/terminal.png)

Como alternativa ao passo acima, você pode iniciar o `spark-shell` (shell do Scala do Spark) sem modificações simplesmente acessando o contêiner e digitando `spark-shell`. A captura de tela está mostrada abaixo:

![spark-shell.png](resources/spark-shell.png)

### Jupyter Notebook:

Acesse a URL [http://localhost:4041](http://localhost:4041). Isso lançará o ambiente Jupyter como mostrado abaixo:

![jupyter_notebook.png](resources/jupyter_notebook.png)

Crie um novo notebook ou abra um existente, como `first_notebook.ipynb`:

![jupyter_new_file.png](resources/jupyter_new_file.png)

— Agora execute algum código básico em Python para garantir que Python e o Jupyter Notebook estejam configurados corretamente.

— Em seguida, execute o seguinte código para encontrar o Spark e criar uma sessão Spark:

```python
import findspark
findspark.init()
import pyspark
from pyspark.sql import SparkSession
import pyspark.sql.functions as f

# criar sessão Spark
spark = SparkSession.builder.appName("SparkSample").getOrCreate()

# ler arquivo de texto
df_text_file = spark.read.text("textfile.txt")
df_text_file.show()

df_total_words = df_text_file.withColumn('wordCount', f.size(f.split(f.col('value'), ' ')))
df_total_words.show()

# Exemplo de contagem de palavras
df_word_count = df_text_file.withColumn('word', f.explode(f.split(f.col('value'), ' '))).groupBy('word').count().sort('count', ascending=False)
df_word_count.show()
```

Captura de tela do notebook Jupyter executando código Spark:

![img.png](resources/jupyter_code.png)

Para acessar o SparkUI, vá para https://localhost:4040. A captura de tela do Spark UI está mostrada abaixo:

![img.png](resources/img.png)

### Para usuários do Spark-shell:

Teste se o Spark está configurado corretamente e funcionando conforme esperado executando o código abaixo ou qualquer outro de sua escolha:

```
import pyspark.sql.functions as f

textfile_df = spark.read.text("textfile.txt")
textfile_df.show()
df = textfile_df.withColumn('wordCount', f.size(f.split(f.col('value'), ' ')))
df.show()
wc_df = textfile_df.withColumn('word', f.explode(f.split(f.col('value'), ' '))).groupBy('word').count().sort('count', ascending=False).show()
wc_df.show()
```

![word_count](resources/word_count.png)

![word_frequency_count](resources/word_frequency_count.png)

Para acessar o SparkUI, vá para https://localhost:4040. A captura de tela do Spark UI está mostrada abaixo:

![spark_ui](resources/spark_ui.png)

### Iniciando o Contêiner usando start.sh:

Para usar o script, certifique-se de que ele tenha permissões executáveis (chmod +x start.sh). Em seguida, execute o script com o argumento da linha de comando desejado.

Exemplos:

```./start.sh build```: irá construir a imagem Docker usando `docker-compose build`.

```./start.sh run```: irá executar o contêiner usando `docker-compose up -d`.

```./start.sh build_and_run```: irá tanto construir a imagem Docker quanto executar o contêiner usando as funções respectivas.

### Iniciando o Contêiner usando start.bat (Windows):

```start.bat build```: Executa a função `:build` para construir a imagem Docker.

```start.bat run```: Executa a função `:run` para executar o contêiner.

```start.bat build_and_run```: Executa a função `:build_and_run` para construir a imagem e executar o contêiner.

### Em seguida, execute a imagem usando o comando `docker run`:

```bash
hostfolder="$(pwd)"
dockerfolder="/home/sam/app"
docker run --rm -it \
  --net="host" \
  -v ${hostfolder}/app:${dockerfolder} \
--entrypoint bash spark-in-docker:latest
```

Para executar em modo detached (desanexado) a partir da janela atual do terminal:

```bash
docker run -d --rm -it \
    -p 4040:4040 -v ${hostfolder}/app:${dockerfolder} \ 
    docker-spark-single-node:latest
```

Outra forma de entrar no contêiner e iniciar o Jupyter Notebook:

```
docker exec -it 1af493da8cebe92d917abc5efa34086013ebeb9e350cb5bf280c63dabc73330f /bin/sh
```

```
jupyter notebook --ip 0.0.0.0 --port 4041 --no-browser --allow-root --NotebookApp.token='' --NotebookApp.password=''
```

### Problemas Conhecidos:

O comando do Jupyter Notebook usado no Dockerfile não utiliza nenhum token ou senha. Portanto, não é seguro para produção. No entanto, você pode facilmente modificar o comando para definir uma senha.

Nota para Windows-1:

Observe que, no caso do Windows, o caminho começa com C:/, que é diferente do padrão de caminho universal. Portanto, se estiver executando a partir do Windows, verifique o caminho com mapeamento de volume.

Nota para Windows-2:

O driver de rede do host só funciona em hosts Linux e não é suportado no Docker Desktop para Mac, Docker Desktop para Windows ou Docker EE para Windows Server. Além disso, o Docker para Windows/Mac não avisará que não funciona - simplesmente executará o contêiner silenciosamente e NÃO se ligará a nenhuma porta local.

Nota-3:

Após migrar do Windows, o lançamento do `spark-shell` estava falhando com o erro `java.io.FileNotFoundException: /home/sam/app/spark_events/local-1695546124823.inprogress (Permission denied)`. O erro ocorreu devido ao acesso à pasta `spark_events` que foi usada como volume para a imagem do Spark. A solução foi alterar o acesso usando o comando `chmod`. `chmod 777 app/spark_events/`.

Nota-4:

Garanta que o diretorio "spark_events" exista em '/home/sam/app/spark_events'

Nota-5:

O novo notebook não conseguia salvar no diretório montado. Solução: atualizou o acesso para o diretório e subdiretórios montados para 777.