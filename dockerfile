FROM public.ecr.aws/lambda/python:3.12

# Install dependencies
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt

COPY . ${LAMBDA_TASK_ROOT}

CMD [ "main.handler" ]