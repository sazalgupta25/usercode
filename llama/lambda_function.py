import boto3

# Create the required resource and client objects
s3 = boto3.resource('s3')
textract = boto3.client('textract')
comprehend = boto3.client('comprehend')

def lambda_handler(event, context):
    try:
        # Get the bucket and key from the S3 event
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        document_key = event['Records'][0]['s3']['object']['key']

        # Check if the file is in the input folder
        if not document_key.startswith('input/'):
            return

        # Extract text from the file using Textract
        response = textract.detect_document_text(Document={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': document_key
                }})
        extracted_text = '\n'.join(item['Text'] for item in response['Blocks'] if item['BlockType'] == 'LINE')
        
        # Process the extracted text using Comprehend
        pii_response = comprehend.detect_pii_entities(Text=extracted_text, LanguageCode='en')
        
        # Write the results to a txt file in the output folder
        entities = []
        for entity in pii_response['Entities']:
            entity_text = extracted_text[entity['BeginOffset']:entity['EndOffset']]
            entities.append(f'{entity_text}: {entity["Type"]}')
        output_bucket = s3.Bucket(bucket_name)
        output_key = f'output/{document_key.split("/")[-1].split(".")[0]}.txt'
        output_text = '\n'.join(entities)
        output_bucket.put_object(Key=output_key, Body=output_text)
    
    # Exception handling
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return