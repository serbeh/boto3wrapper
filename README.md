# Prerequirements

- set AWS credentials
- boto3

# Usage example

```python
import boto3wrapper

s3 = boto3wrapper.Boto3wrapper('bucket-name', default_path='./weights')
...

s3.list_objects(prefix='weights/project/')  # List all objects under 'weights/project/'
s3.get('path-to-file-in-this-bucket.h5')  # Get some model/weight
s3.get('path-to-file-in-this-bucket.zip')  # Get some dataset
s3.upload('./weights/best.pth', 'path/to/file/in/bucket/best.pth')  # Upload resulted weight
```
    