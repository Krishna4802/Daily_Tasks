

### Save as docker file 

    FROM openjdk:8-jdk
     
    # Set Spark version
    ARG SPARK_VERSION=3.4.1
     
    # Download and extract Spark
    RUN wget -qO- https://dlcdn.apache.org/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop3.tgz | tar xvz -C /opt/
     
    # Set environment variables
    ENV SPARK_HOME=/opt/spark-$SPARK_VERSION-bin-hadoop3
    ENV PATH=$PATH:$SPARK_HOME/bin
     
    # Spark master and worker ports
    EXPOSE 7077 8080 8081
     
    # Start Spark Master by default
    CMD ["spark-class", "org.apache.spark.deploy.master.Master"]

### Then execute the following commands

    * docker build -t spark-image .
    
    * docker network create spark-network
    
    * docker run -d --name spark-master --network spark-network -p 7077:7077 -p 8080:8080 -p 8081:8081 -p 8888:8888 spark-image:latest spark-class org.apache.spark.deploy.master.Master
    
    * docker run -d --name spark-worker-1 --network spark-network spark-image:latest spark-class org.apache.spark.deploy.worker.Worker spark://spark-master:7077
    
    * docker run -d --name spark-worker-2 --network spark-network spark-image:latest spark-class org.apache.spark.deploy.worker.Worker spark://spark-master:7077


### For installing jupyter nuotebook 
    
    Go inside spark container -> go to terminal
    
    * apt update
    * apt install python3
    * apt install pip 
    * pip install Jupyter
    * jupyter-notebook --allow-root --ip=0.0.0.0
  
