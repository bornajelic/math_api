#!/bin/bash
pytest .
gunicorn 'math_api.main:app' \
    --bind :${PORT:-81} \
    --workers ${WORKERS:-2} \
    --timeout ${WORKER_TIMEOUT:-120} \
    --keep-alive ${KEEP_ALIVE:-130} \
    ${ADDITIONAL_GUNICORN_OPTIONS} \
    --worker-class uvicorn.workers.UvicornWorker
