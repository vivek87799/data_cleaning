# Data Cleaning: Consumer
Module to consume the data from kafka topic and clean the data

## Data Cleaning
- A kafka consumer module that gets the data from the topic and cleans the data

## To Run
- Use the docker file provided to set up the container and installing the package
- Configs are provided in config.py and message_publisher/config.py
```
python data_cleaning.py
```

## Requirements
- Requires that the kafka zookeeper is running and a producer module is publishing data to the topic