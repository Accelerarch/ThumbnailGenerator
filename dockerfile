# Use an AWS Lambda base image for your runtime (e.g., Python, Node.js, C++)

FROM --platform=linux/amd64 public.ecr.aws/lambda/python:3.13

# Copy application files
COPY requirements.txt .
COPY app.py /var/task/

# Install dependencies if needed
RUN pip install -r requirements.txt

# Command that Lambda will call
CMD ["app.lambda_handler"]