# 1. Base image
FROM python:3.12.3

# 2. Set workdir
WORKDIR /app

# 3. Copy project files
COPY . /app

# 4. Install uv & sync
RUN pip install uv && uv sync --frozen

# 5. Expose port
EXPOSE 8000

# 6. Command to run app
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]