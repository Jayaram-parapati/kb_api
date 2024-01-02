FROM python

WORKDIR /KB_API

# Print the contents of the current directory
RUN ls -la

COPY . .

# Print the contents of the directory after copying the file
RUN ls -la

CMD ["python", "test.py"]
