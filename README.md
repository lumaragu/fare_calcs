### Installation

```bash
git clone https://github.com/lumaragu/beat_test
```

### Build & Launch

```bash
docker-compose up -d --build
```

This will expose the Flask application's endpoints on port `5001` as well as a Flower server for monitoring workers on port `5555`


To shut down:

```bash
docker-compose down
```

### Usage via Docker-Compose

After all the containers are up and running using docker-compose, the following endpoints are available:

Monitoring the service
```bash
http://127.0.0.1:5001/
```
Calculate Fare (Explanation below)
```bash
http://127.0.0.1:5001/calculate_fare
```
Check for task status
```bash
http://127.0.0.1:5001/check/<task_id>
```
Flower Monitor
```bash
http://127.0.0.1:5555
```

When accessing the `/calculate_fare` endpoint, a task will be triggered to do the calculations of the fares of the different rides contained in the `paths.csv` file. This endpoint returns a `task_id` that can be consulted later to know its status and verify the results.

In the background, the task is processed asynchronously using `Celery` as Task Queue and `Redis` as Broker.

When the task finishes, the result is stored into a csv file named `results.csv` and also is displayed when accessing the endpoint of the task result.

### Usage via console

Using `Python3.9`, it is necessary to execute the following to obtain the `results.csv` file.

```bash
cd queue
python calculation.py
``` 

### Tests

Using `Python3.9` and `pytest` the tests are executed to verify that all the calculation methods are working properly.

```bash
pytest
``` 