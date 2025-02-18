FROM python:3.9-slim
# Copy the application code
COPY . /app/
# Set the working directory in the container
WORKDIR /app

RUN pip install nvidia-cublas-cu12===12.4.5.8

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Expose the ports for FastAPI (8000) and Streamlit (8501)
EXPOSE 8000
# Start both FastAPI and Streamlit servers
CMD ["sh", "-c", "uvicorn chatbot/model:app --host 0.0.0.0 --port 8000"]
