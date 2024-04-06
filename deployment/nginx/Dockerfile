# Use the official NGINX image
FROM nginx:alpine

# Copy custom configuration file
COPY default.conf /etc/nginx/conf.d/default.conf

# Expose port 80 to the Docker host
EXPOSE 80

# Command to start NGINX
CMD ["nginx", "-g", "daemon off;"]
