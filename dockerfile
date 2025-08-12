FROM python:3.10-slim
# Создаем пользователя и группу
RUN groupadd -r appuser && useradd -r -g appuser appuser
WORKDIR /app
COPY --chown=appuser:appuser . .
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p /app/logs && chown appuser:appuser /app/logs
USER appuser
ENTRYPOINT ["python", "bot.py"]