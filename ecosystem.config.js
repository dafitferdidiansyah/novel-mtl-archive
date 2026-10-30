module.exports = {
  apps: [
    {
      name: 'epub-backend',
      script: './backend/.venv/bin/gunicorn',
      args: 'config.wsgi:application --bind 0.0.0.0:8000 --workers 3',
      cwd: './backend',
      interpreter: 'none',
      restart_delay: 3000,
      max_restarts: 10,
      env: {
        DJANGO_SETTINGS_MODULE: 'config.settings',
        PYTHONUNBUFFERED: '1',
      },
    },
    {
      name: 'epub-ngrok',
      script: 'ngrok',
      args: 'http 8000',
      restart_delay: 5000,
      max_restarts: 10,
    },
  ],
};
