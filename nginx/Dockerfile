FROM nginx:1.21.5-alpine
ARG MODE
RUN rm /etc/nginx/conf.d/default.conf
WORKDIR /etc/nginx/templates
RUN if [ "$MODE" != "local" ] && [ "$MODE" != "production" ]; then \
		echo "Invalid MODE value: $MODE. Please specify either 'local' or 'production'." >&2; \
		exit 1; \
	fi
COPY ./config/nginx.conf.${MODE} nginx.conf.template